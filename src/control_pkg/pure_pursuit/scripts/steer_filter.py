#!/usr/bin/env python3

import rospy
from erp42_msgs.msg import DriveCmd
import math

class SteerFilterNode:
    def __init__(self):
        rospy.init_node('steer_filter')
        
        # Parameters
        self.ema_alpha = rospy.get_param('~ema_alpha', 0.8)
        self.max_steer_delta = rospy.get_param('/stier_params/common/max_steer_delta', 8.0)

        # 조향각 오프셋 ******** 매우 중요 ********* -> 양수면 왼쪽으로 오프셋 (정방향), 음수면 오른쪽으로 오프셋 (역방향)
        self.steer_offset = rospy.get_param('~steer_offset', 0)
        
        # State
        self.last_steer_deg = 0.0
        self.initialized = False
        
        # Pub/Sub
        self.sub_raw = rospy.Subscriber('/pure_pursuit/raw_drive', DriveCmd, self.raw_drive_cb)
        self.pub_filtered = rospy.Publisher('/erp42_serial/drive', DriveCmd, queue_size=1)
        
        rospy.loginfo("SteerFilterNode initialized. alpha=%.2f, max_delta=%.1f", 
                      self.ema_alpha, self.max_steer_delta)

    def raw_drive_cb(self, msg):
        # 1. 장애물 정지 등 긴급 제동의 경우 필터 패스
        if msg.brake == 1 or msg.KPH == 0:
            self.pub_filtered.publish(msg)
            return
            
        # 2. 차선 경로(vision) 모드일 경우 필터 패스 (사용자 요청)
        # 단, 모드 전환 시 튀는 현상을 막기 위해 last_steer_deg는 업데이트함
        active_mode = rospy.get_param("/routing_mode_active", "gps")
        if active_mode == "vision":
            self.last_steer_deg = float(msg.Deg)
            self.initialized = True
            self.pub_filtered.publish(msg)
            return
            
        raw_steer = float(msg.Deg)
        
        # 첫 조향값은 필터 없이 바로 적용
        if not self.initialized:
            self.last_steer_deg = raw_steer
            self.initialized = True
            self.pub_filtered.publish(msg)
            return

        # 2. EMA 필터링 (부드러운 조향)
        filtered_steer = self.ema_alpha * raw_steer + (1.0 - self.ema_alpha) * self.last_steer_deg
        
        # 3. Slew Rate Limit (최대 변화량 제한)
        steer_diff = filtered_steer - self.last_steer_deg
        if abs(steer_diff) > self.max_steer_delta:
            filtered_steer = self.last_steer_deg + math.copysign(self.max_steer_delta, steer_diff)
            
        self.last_steer_deg = filtered_steer
        
        # Update msg
        msg.Deg = int(filtered_steer)
        msg.Deg -= self.steer_offset
        self.pub_filtered.publish(msg)

if __name__ == '__main__':
    try:
        SteerFilterNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
