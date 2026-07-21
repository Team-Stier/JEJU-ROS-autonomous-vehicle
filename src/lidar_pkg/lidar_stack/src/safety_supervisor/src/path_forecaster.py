#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import math
from dynamic_reconfigure.server import Server
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker

#  통합 메시지 타입 (패키지명: lidar_interfaces)
try:
    from erp42_msgs.msg import SerialFeedBack
except ImportError:
    rospy.logerr("Could not import SerialFeedBack. Please run catkin_make first.")

# dynamic_reconfigure 설정
try:
    from safety_supervisor.cfg import PredictedPathParametersConfig
except ImportError:
    PredictedPathParametersConfig = None


class PathForecaster:
    def __init__(self):
        # ---- 1. 튜닝 파라미터 ----
        self.publish_hz = 20.0
        self.path_step = 0.2                  # 경로 점 간격(m)
        self.path_count = 10                  # 경로 점 개수 (총 2m 예측)
        self.path_frame_id = "velodyne"
        self.wheelbase = 0.75              # 수정 필요함

        # ---- 2. 실시간 데이터 변수 ----
        self.current_speed = 0.0              # 속도 (m/s)
        self.current_steer = 0.0              # 조향각 (Radian)

        # ---- 3. 런타임 캐시 및 파라미터 서버 설정 ----
        self.path_points = []
        self.predicted_path_step_param = "/safety_supervisor/predicted_path_parameters/path_step"
        self.predicted_path_count_param = "/safety_supervisor/predicted_path_parameters/path_count"
        self._syncing_predicted_path_parameters = False

        # ---- 4. ROS I/O 설정 ----
        # 궤적 발행용 Publisher
        self.path_pub = rospy.Publisher("/predicted_path", Path, queue_size=1)
        self.speed_hud_pub = rospy.Publisher("/speed_hud_marker", Marker, queue_size=1)
        
        # [핵심] 아두이노 통합 데이터 구독 
        self.feedback_sub = rospy.Subscriber("/erp42_serial/feedback", SerialFeedBack, self.callback_feedback)

        # Dynamic Reconfigure 설정
        self.load_predicted_path_parameters()
        self.predicted_path_parameters_server = None
        
        if PredictedPathParametersConfig is None:
            rospy.logwarn("safety_supervisor.cfg import failed. rqt_reconfigure disabled.")
        else:
            self.predicted_path_parameters_server = Server(
                PredictedPathParametersConfig,
                self.predicted_path_parameters_reconfigure_callback,
            )
            self.sync_predicted_path_parameters(force=True)

    # ======================
    # Callbacks & Main Loop
    # ======================
    def callback_feedback(self, msg):
        """ 아두이노에서 오는 실전 데이터를 받는 함수 """
        self.current_speed = msg.speed
        self.current_steer = math.radians(-msg.steer) # Degree -> Radian 변환 (부호 반전)

    def run(self):
        """ 20Hz 주기로 실행되는 메인 루프 """
        rate = rospy.Rate(self.publish_hz)
        while not rospy.is_shutdown():
            self.sync_predicted_path_parameters()
            
            # [수학 엔진 가동] 실시간 데이터로 궤적 계산
            self.path_points = self.generate_path_from_speed_steer(self.current_speed, self.current_steer)
            
            # RViz에 발행
            self.path_pub.publish(self.build_path_msg(self.path_points))
            self.speed_hud_pub.publish(self.build_speed_hud_marker())
            rate.sleep()

    # ======================
    # Path Engine (수학 공식)
    # ======================
    def generate_path_from_speed_steer(self, speed, steer):
        """ 
        재준님의 삼각함수 로직: 자전거 모델(Kinematic Bicycle Model)
        """
        points = []
        x, y, yaw = 0.0, 0.0, 0.0

        # 차량이 멈춰있으면 직진 fallback 경로 표시
        # if abs(speed) < 0.05:
        #    return self.generate_fallback_path()

        for i in range(self.path_count):
            points.append((x, y))
            
            # 다음 점의 위치 예측 ($ds = path\_step$)
            x += self.path_step * math.cos(yaw)
            y += self.path_step * math.sin(yaw)
            
            # 조향각에 따른 방향 변화량 계산 ($d\psi = \frac{ds \cdot \tan(\delta)}{L}$)
            yaw += (self.path_step * math.tan(steer)) / self.wheelbase

        return points

    def generate_fallback_path(self):
        """ 정지 상태일 때의 기본 경로 """
        return [(i * self.path_step, 0.0) for i in range(self.path_count)]

    def build_path_msg(self, points):
        """ 계산된 좌표 리스트를 ROS Path 메시지로 변환 """
        stamp = rospy.Time.now()
        msg = Path()
        msg.header.frame_id = self.path_frame_id
        msg.header.stamp = stamp
        for px, py in points:
            pose = PoseStamped()
            pose.header.frame_id = self.path_frame_id
            pose.header.stamp = stamp
            pose.pose.position.x = px
            pose.pose.position.y = py
            pose.pose.orientation.w = 1.0
            msg.poses.append(pose)
        return msg

    def build_speed_hud_marker(self):
        """ RViz에서 차량 기준으로 고정되어 보이는 속도 텍스트 """
        marker = Marker()
        marker.header.frame_id = "stier"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "speed_hud"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.frame_locked = True
        marker.pose.position.x = 2.5
        marker.pose.position.y = -1.2
        marker.pose.position.z = 1.6
        marker.pose.orientation.w = 1.0
        marker.scale.z = 0.9
        marker.color = ColorRGBA(1.0, 1.0, 1.0, 0.95)
        marker.lifetime = rospy.Duration(0.3)
        marker.text = "Speed\n{:.1f}".format(self.current_speed)
        return marker

    # ======================
    # Parameter Sync 
    # ======================
    def load_predicted_path_parameters(self):
        self.path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        self.path_count = int(rospy.get_param(self.predicted_path_count_param, self.path_count))
        rospy.set_param(self.predicted_path_step_param, self.path_step)
        rospy.set_param(self.predicted_path_count_param, self.path_count)

    def predicted_path_parameters_reconfigure_callback(self, config, level):
        self.path_step = float(config.path_step)
        self.path_count = int(config.path_count)
        if not self._syncing_predicted_path_parameters:
            rospy.set_param(self.predicted_path_step_param, self.path_step)
            rospy.set_param(self.predicted_path_count_param, self.path_count)
        return config

    def sync_predicted_path_parameters(self, force=False):
        if self.predicted_path_parameters_server is None:
            self.load_predicted_path_parameters()
            return
        configured_path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        configured_path_count = int(rospy.get_param(self.predicted_path_count_param, self.path_count))
        if not force and abs(configured_path_step - self.path_step) <= 1e-9 and configured_path_count == self.path_count:
            return
        self._syncing_predicted_path_parameters = True
        try:
            self.predicted_path_parameters_server.update_configuration({
                "path_step": configured_path_step,
                "path_count": configured_path_count,
            })
        finally:
            self._syncing_predicted_path_parameters = False


if __name__ == "__main__":
    rospy.init_node("path_forecaster", anonymous=False)
    node = PathForecaster()
    node.run()
