#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import numpy as np
import math as m
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from lidar_interfaces.msg import ObjectInfo

def wrap_to_pi(a: float) -> float:
    return (a + m.pi) % (2 * m.pi) - m.pi

class Node:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.parent = None
        self.cost = 0.0
        self.theta = 0.0
        self.clearance = 1e9

class RRTStarPlanner:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.dist_to_connect = 0.8
        self.num_of_cand_node = 9
        self.path_len = 9
        self.arrive = 0.5
        self.angle = m.radians(25)
        self.beam_width = 10
        
        # 가중치 설정
        self.w_goal = 2.0
        self.w_smooth = 5.0
        self.w_clear = 25.0
        
        self.obs_xy = np.empty((0, 2), dtype=np.float32)
        self.r_infl = 0.7 

    def update_obstacles(self, obs_list):
        self.obs_xy = np.array(obs_list)

    def _dist(self, n1, n2):
        return m.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

    def _score(self, parent, child):
        d_goal = m.sqrt((child.x - self.goal.x)**2 + (child.y - self.goal.y)**2)
        d_smooth = abs(wrap_to_pi(child.theta - parent.theta))
        d_clear = 1.0 / (child.clearance + 0.001)
        return self.w_goal * d_goal + self.w_smooth * d_smooth + self.w_clear * d_clear

    def _segment_is_safe(self, p1, p2):
        if len(self.obs_xy) == 0: return True, 1e9
        steps = 8
        min_clear = 1e9
        for i in range(steps + 1):
            curr_x = p1.x + (p2.x - p1.x) * (i / steps)
            curr_y = p1.y + (p2.y - p1.y) * (i / steps)
            dists = np.sqrt(np.sum((self.obs_xy - [curr_x, curr_y])**2, axis=1))
            min_d = np.min(dists)
            
            dynamic_r = self.r_infl
            if curr_x < 1.0:
                dynamic_r = self.r_infl * max(0.5, curr_x)

            if min_d < dynamic_r:
                return False, 0
            if min_d < min_clear:
                min_clear = min_d
        return True, min_clear

    def find_path(self):
        root = self.start
        root.theta = 0.0
        curr_nodes = [root]
        for _ in range(self.path_len):
            all_next = []
            for parent in curr_nodes:
                for i in range(self.num_of_cand_node):
                    cand_theta = parent.theta + (i - (self.num_of_cand_node//2)) * (self.angle / (self.num_of_cand_node//2))
                    q = Node(parent.x + self.dist_to_connect * m.cos(cand_theta),
                             parent.y + self.dist_to_connect * m.sin(cand_theta))
                    q.parent = parent
                    q.theta = cand_theta
                    safe, clear = self._segment_is_safe(parent, q)
                    if safe:
                        q.clearance = clear
                        q.cost = parent.cost + self.dist_to_connect
                        all_next.append((self._score(parent, q), q))
            if not all_next: break
            all_next.sort(key=lambda x: x[0])
            curr_nodes = [item[1] for item in all_next[:self.beam_width]]
            for n in curr_nodes:
                if self._dist(n, self.goal) < self.arrive:
                    return self._reconstruct_path(n)
        if not curr_nodes: return None
        return self._reconstruct_path(curr_nodes[0])

    def _reconstruct_path(self, node):
        path = []
        while node:
            path.append((node.x, node.y))
            node = node.parent
        return path[::-1]

class DynamicGoalNode:
    def __init__(self):
        rospy.init_node('rrt_dynamic_goal_node')
        
        # 기본 목표점 (5, 0)
        self.default_goal_x = 3.0
        self.default_goal_y = 0.0
        # 목표점 EMA 필터 파라미터 (0.1: 매우 부드러움, 0.5: 중간, 0.9: 민감)
        self.goal_ema_alpha = 0.3
        self.last_goal_y = 0.0
        
        # 이전 경로 저장 (보간/필터용)
        self.last_path = None
        
        # 플래너 초기화
        self.planner = RRTStarPlanner(Node(0,0), Node(self.default_goal_x, self.default_goal_y)) 
        
        self.pub_path = rospy.Publisher('/lidar_path', Path, queue_size=1)
        self.sub_obs = rospy.Subscriber('/voxel_info', ObjectInfo, self.obs_callback)
        rospy.loginfo("RRT* with Goal filtering Node Started!")

    def find_best_gap_goal(self, obs_xy):
        """
        [2번 전략] 장애물들 사이의 가장 큰 틈새를 찾아 목표점으로 설정
        전방 4~6m 사이의 영역에서 장애물 간격이 넓은 곳의 중앙을 찾음
        """
        # 전방에 있는 장애물들 필터링
        front_obs = obs_xy[(obs_xy[:,0] > 1.0) & (obs_xy[:,0] < 8.0)]
        
        if len(front_obs) < 2:
            return self.default_goal_x, self.default_goal_y

        # Y좌표 정렬
        sorted_obs = front_obs[front_obs[:, 1].argsort()]
        
        max_gap = 0
        best_y = 0.0
        
        # 장애물 사이 간격 계산
        for i in range(len(sorted_obs) - 1):
            gap = sorted_obs[i+1, 1] - sorted_obs[i, 1]
            if gap > max_gap:
                max_gap = gap
                best_y = (sorted_obs[i+1, 1] + sorted_obs[i, 1]) / 2.0
        
        # 만약 가장 큰 틈이 너무 좁거나 중앙에서 너무 멀다면 기본값 사용 고려
        if max_gap < 1.5: # 1.5m 미만의 틈은 무시하고 직진 시도 가능
             return self.default_goal_x, self.default_goal_y
             
        # y축 이동을 제한 (급회전 방지)
        best_y = np.clip(best_y, -3.0, 3.0)
        
        return self.default_goal_x, best_y

    def obs_callback(self, msg):
        if msg.objectCounts == 0:
            return

        centers = []
        obstacles_in_2m = 0
        for i in range(msg.objectCounts):
            cx, cy = msg.centerX[i], msg.centerY[i]
            centers.append([cx, cy])
            d_sq = cx**2 + cy**2
            if d_sq <= 12.0:  # 2^2
                obstacles_in_2m += 1
        
        # 2미터 반경 내에 장애물이 3개 이상 들어오는 경우에만 작동
        if obstacles_in_2m < 8:
            # 2m 반경 내 클러스터 개수가 3개 미만이면 무시 (Path 발행 안 함)
            return

        obs_xy = np.array(centers)
        
        # [2번 전략 구현] 다이내믹 목표지점 선정
        gx, gy_raw = self.find_best_gap_goal(obs_xy)
        
        # [필터링 추가] Goal Y좌표 EMA 필터링 (튀는 현상 방지)
        gy = self.goal_ema_alpha * gy_raw + (1.0 - self.goal_ema_alpha) * self.last_goal_y
        self.last_goal_y = gy
        
        self.planner.goal = Node(gx, gy)
        
        self.planner.update_obstacles(centers)
        raw_path = self.planner.find_path()
        
        if not raw_path or len(raw_path) < 2:
            return

        # 경로 전체를 x축(전방) 30cm 오프셋
        OFFSET_X = 0.3
        offset_path = [(p[0] + OFFSET_X, p[1]) for p in raw_path]

        # 원점(0, 0)에서 오프셋된 경로까지 이어지도록 맨 앞에 원점 삽입
        final_path = [(0.0, 0.0)] + offset_path

        path_msg = Path()
        path_msg.header.frame_id = "velodyne"
        path_msg.header.stamp = rospy.Time.now()
        for p in final_path:
            ps = PoseStamped()
            ps.pose.position.x, ps.pose.position.y = p[0], p[1]
            path_msg.poses.append(ps)
        self.pub_path.publish(path_msg)

if __name__ == '__main__':
    try:
        node = DynamicGoalNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
