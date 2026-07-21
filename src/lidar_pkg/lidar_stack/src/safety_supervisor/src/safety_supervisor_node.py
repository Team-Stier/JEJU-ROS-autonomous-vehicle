#!/usr/bin/env python3



import rospy
from dynamic_reconfigure.server import Server
from std_msgs.msg import Bool, Float32, Int32
from nav_msgs.msg import Path
from lidar_interfaces.msg import ObjectInfo
from erp42_msgs.msg import SerialFeedBack


try:
    from safety_supervisor.cfg import SafetySupervisorParametersConfig
except ImportError:
    SafetySupervisorParametersConfig = None


class SafetySupervisor:
    def __init__(self):
        # ---- 튜닝 파라미터 ----
        self.path_width_margin = 0.5          # 경로 코리도어 반폭 마진
        self.estop_hold_time = 3.0            # E-STOP 상태 유지 시간 (초)
        self.max_check_distance = 10.0        # roi max
        self.min_check_distance = 2.0         # roi min
        self.lookahead_time = 3               # roi 전방 시간거리
        self.roi_speed_curve = 0.0            # ROI 속도 민감도 곡률 (-: 저속 민감, +: 고속 민감)
        self.detect_count_threshold = 2       # 디바운스: N회 연속 검출 시 인터럽트 ON
        self.clear_count_threshold = 4        # 히스테리시스: M회 연속 미검출 시 인터럽트 OFF
        self.stale_clear_count_threshold = 2  # 입력 stale N회 연속 시 인터럽트 OFF
        self.data_timeout_sec = 0.5           # 입력 데이터 신선도 타임아웃
        self.path_step = 0.2                  # 공유 경로 점 간격(m)
        self.path_count = 10                  # 공유 경로 점 개수
        self.margin_step = 0.05               # 점마다 경로 코리도어 마진 감소량 (m)

        # ---- 런타임 캐시 ----
        self.path_points = []                 # [(x, y), ...]
        self.path_stamp = None
        self.obstacles = []                   # [box dict, ...]
        self.ob_stamp = None
        self.speed = 0.0
        self.speed_stamp = None
        self.interrupt_active = False
        self.last_estop_time = None           # 마지막 E-STOP 발동 시점
        self.detect_count = 0
        self.clear_count = 0
        self.stale_clear_count = 0
        self.collision_check_path_point_count = 0
        self.predicted_path_step_param = "/safety_supervisor/predicted_path_parameters/path_step"
        self.predicted_path_count_param = "/safety_supervisor/predicted_path_parameters/path_count"
        self.safety_path_width_margin_param = "/safety_supervisor/safety_supervisor_parameters/path_width_margin"
        self.safety_max_check_distance_param = "/safety_supervisor/safety_supervisor_parameters/max_check_distance"
        self.safety_min_check_distance_param = "/safety_supervisor/safety_supervisor_parameters/min_check_distance"
        self.safety_lookahead_time_param = "/safety_supervisor/safety_supervisor_parameters/lookahead_time"
        self.safety_roi_speed_curve_param = "/safety_supervisor/safety_supervisor_parameters/roi_speed_curve"
        self.safety_detect_count_threshold_param = "/safety_supervisor/safety_supervisor_parameters/detect_count_threshold"
        self.safety_clear_count_threshold_param = "/safety_supervisor/safety_supervisor_parameters/clear_count_threshold"
        self.safety_stale_clear_count_threshold_param = "/safety_supervisor/safety_supervisor_parameters/stale_clear_count_threshold"
        self.safety_data_timeout_sec_param = "/safety_supervisor/safety_supervisor_parameters/data_timeout_sec"
        self.safety_margin_step_param = "/safety_supervisor/safety_supervisor_parameters/margin_step"
        self._syncing_safety_supervisor_parameters = False

        # ---- ROS I/O ----
        rospy.Subscriber("/predicted_path", Path, self.callback_path)       # 조향각, 속도 -> 차량 예상 궤적(/predicted_path) 발행하는 노드를 만들자.
        rospy.Subscriber("/voxel_info", ObjectInfo, self.callback_obstacle)
        # TODO : 속도 구독
        self.feedback_sub = rospy.Subscriber("/erp42_serial/feedback", SerialFeedBack, self.callback_feedback)
        self.interrupt_pub = rospy.Publisher("/mission_interrupt", Bool, queue_size=1)
        self.collision_check_path_point_count_pub = rospy.Publisher(
            "/collision_check_path_point_count",
            Int32,
            queue_size=1,
        )
        self.load_predicted_path_parameters()
        self.load_safety_supervisor_parameters()
        self.safety_supervisor_parameters_server = None
        if SafetySupervisorParametersConfig is None:
            rospy.logwarn(
                "safety_supervisor.cfg.SafetySupervisorParametersConfig import failed. "
                "Run catkin_make and source devel/setup.bash to enable rqt_reconfigure."
            )
        else:
            self.safety_supervisor_parameters_server = Server(
                SafetySupervisorParametersConfig,
                self.safety_supervisor_parameters_reconfigure_callback,
            )
            self.sync_safety_supervisor_parameters(force=True)

    def run(self):
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            self.sync_predicted_path_parameters()
            self.sync_safety_supervisor_parameters()
            active_path_points = self.get_active_path_points()
            if self.is_data_ready():
                self.stale_clear_count = 0
                self.collision_check_path_point_count = self.get_collision_check_path_point_count(active_path_points)
                hazard = self.is_collision_risk_on_path(active_path_points)
                self.update_interrupt_state(hazard)
            else:
                self.collision_check_path_point_count = 0
                self.update_stale_clear_state()

            self.publish_collision_check_path_point_count()
            self.publish_interrupt()
            rate.sleep()


    # ======================
    # callbacks
    # ======================

    def callback_path(self, msg):
        self.path_points = [
            (pose.pose.position.x, pose.pose.position.y)
            for pose in msg.poses
        ]
        self.path_stamp = rospy.Time.now()

    # 구독한 /object_info를 box딕셔너리로 변환 후 저장.
    def callback_obstacle(self, msg):
        boxes = []
        n = int(msg.objectCounts)
        n = max(0, min(n, len(msg.centerX), len(msg.centerY), len(msg.lengthX), len(msg.lengthY)))
        for i in range(n):
            cx = msg.centerX[i]
            cy = msg.centerY[i]
            hx = msg.lengthX[i] * 0.5
            hy = msg.lengthY[i] * 0.5

            box = {
                "cx": cx,
                "cy": cy,
                "min_x": cx - hx,
                "max_x": cx + hx,
                "min_y": cy - hy,
                "max_y": cy + hy,
            }
            boxes.append(box)

        self.obstacles = boxes
        self.ob_stamp = rospy.Time.now()

    # speed업데이트
    # 속도 단위에 따라 더 처리해야 할 수도 잇음

    def callback_feedback(self, msg):
        """ 아두이노에서 오는 실전 데이터를 받는 함수 """
        self.speed = msg.speed
        self.speed_stamp = rospy.Time.now()


    # ======================
    # Parameter Sync
    # ======================
    def load_predicted_path_parameters(self):
        self.path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        self.path_count = int(rospy.get_param(self.predicted_path_count_param, self.path_count))

    def sync_predicted_path_parameters(self):
        self.path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        self.path_count = int(rospy.get_param(self.predicted_path_count_param, self.path_count))

    # ======================
    # Safety Parameter Sync
    # ======================
    def load_safety_supervisor_parameters(self):
        self.path_width_margin = float(rospy.get_param(self.safety_path_width_margin_param, self.path_width_margin))
        self.max_check_distance = float(rospy.get_param(self.safety_max_check_distance_param, self.max_check_distance))
        self.min_check_distance = float(rospy.get_param(self.safety_min_check_distance_param, self.min_check_distance))
        self.lookahead_time = float(rospy.get_param(self.safety_lookahead_time_param, self.lookahead_time))
        self.roi_speed_curve = float(rospy.get_param(self.safety_roi_speed_curve_param, self.roi_speed_curve))
        self.detect_count_threshold = int(
            rospy.get_param(self.safety_detect_count_threshold_param, self.detect_count_threshold)
        )
        self.clear_count_threshold = int(
            rospy.get_param(self.safety_clear_count_threshold_param, self.clear_count_threshold)
        )
        self.stale_clear_count_threshold = int(
            rospy.get_param(self.safety_stale_clear_count_threshold_param, self.stale_clear_count_threshold)
        )
        self.data_timeout_sec = float(rospy.get_param(self.safety_data_timeout_sec_param, self.data_timeout_sec))
        self.margin_step = float(rospy.get_param(self.safety_margin_step_param, self.margin_step))
        rospy.set_param(self.safety_path_width_margin_param, self.path_width_margin)
        rospy.set_param(self.safety_max_check_distance_param, self.max_check_distance)
        rospy.set_param(self.safety_min_check_distance_param, self.min_check_distance)
        rospy.set_param(self.safety_lookahead_time_param, self.lookahead_time)
        rospy.set_param(self.safety_roi_speed_curve_param, self.roi_speed_curve)
        rospy.set_param(self.safety_detect_count_threshold_param, self.detect_count_threshold)
        rospy.set_param(self.safety_clear_count_threshold_param, self.clear_count_threshold)
        rospy.set_param(self.safety_stale_clear_count_threshold_param, self.stale_clear_count_threshold)
        rospy.set_param(self.safety_data_timeout_sec_param, self.data_timeout_sec)
        rospy.set_param(self.safety_margin_step_param, self.margin_step)

    def safety_supervisor_parameters_reconfigure_callback(self, config, level):
        self.path_width_margin = float(config.path_width_margin)
        self.max_check_distance = float(config.max_check_distance)
        self.min_check_distance = float(config.min_check_distance)
        self.lookahead_time = float(config.lookahead_time)
        self.roi_speed_curve = float(config.roi_speed_curve)
        self.detect_count_threshold = int(config.detect_count_threshold)
        self.clear_count_threshold = int(config.clear_count_threshold)
        self.stale_clear_count_threshold = int(config.stale_clear_count_threshold)
        self.data_timeout_sec = float(config.data_timeout_sec)
        self.margin_step = float(config.margin_step)
        if not self._syncing_safety_supervisor_parameters:
            rospy.set_param(self.safety_path_width_margin_param, self.path_width_margin)
            rospy.set_param(self.safety_max_check_distance_param, self.max_check_distance)
            rospy.set_param(self.safety_min_check_distance_param, self.min_check_distance)
            rospy.set_param(self.safety_lookahead_time_param, self.lookahead_time)
            rospy.set_param(self.safety_roi_speed_curve_param, self.roi_speed_curve)
            rospy.set_param(self.safety_detect_count_threshold_param, self.detect_count_threshold)
            rospy.set_param(self.safety_clear_count_threshold_param, self.clear_count_threshold)
            rospy.set_param(self.safety_stale_clear_count_threshold_param, self.stale_clear_count_threshold)
            rospy.set_param(self.safety_data_timeout_sec_param, self.data_timeout_sec)
            rospy.set_param(self.safety_margin_step_param, self.margin_step)
        return config

    def sync_safety_supervisor_parameters(self, force=False):
        if self.safety_supervisor_parameters_server is None:
            self.load_safety_supervisor_parameters()
            return

        configured_path_width_margin = float(rospy.get_param(self.safety_path_width_margin_param, self.path_width_margin))
        configured_max_check_distance = float(
            rospy.get_param(self.safety_max_check_distance_param, self.max_check_distance)
        )
        configured_min_check_distance = float(
            rospy.get_param(self.safety_min_check_distance_param, self.min_check_distance)
        )
        configured_lookahead_time = float(rospy.get_param(self.safety_lookahead_time_param, self.lookahead_time))
        configured_roi_speed_curve = float(
            rospy.get_param(self.safety_roi_speed_curve_param, self.roi_speed_curve)
        )
        configured_detect_count_threshold = int(
            rospy.get_param(self.safety_detect_count_threshold_param, self.detect_count_threshold)
        )
        configured_clear_count_threshold = int(
            rospy.get_param(self.safety_clear_count_threshold_param, self.clear_count_threshold)
        )
        configured_stale_clear_count_threshold = int(
            rospy.get_param(self.safety_stale_clear_count_threshold_param, self.stale_clear_count_threshold)
        )
        configured_data_timeout_sec = float(rospy.get_param(self.safety_data_timeout_sec_param, self.data_timeout_sec))
        configured_margin_step = float(rospy.get_param(self.safety_margin_step_param, self.margin_step))

        if (
            not force
            and abs(configured_path_width_margin - self.path_width_margin) <= 1e-9
            and abs(configured_max_check_distance - self.max_check_distance) <= 1e-9
            and abs(configured_min_check_distance - self.min_check_distance) <= 1e-9
            and abs(configured_lookahead_time - self.lookahead_time) <= 1e-9
            and abs(configured_roi_speed_curve - self.roi_speed_curve) <= 1e-9
            and configured_detect_count_threshold == self.detect_count_threshold
            and configured_clear_count_threshold == self.clear_count_threshold
            and configured_stale_clear_count_threshold == self.stale_clear_count_threshold
            and abs(configured_data_timeout_sec - self.data_timeout_sec) <= 1e-9
            and abs(configured_margin_step - self.margin_step) <= 1e-9
        ):
            return

        self._syncing_safety_supervisor_parameters = True
        try:
            self.safety_supervisor_parameters_server.update_configuration(
                {
                    "path_width_margin": configured_path_width_margin,
                    "max_check_distance": configured_max_check_distance,
                    "min_check_distance": configured_min_check_distance,
                    "lookahead_time": configured_lookahead_time,
                    "roi_speed_curve": configured_roi_speed_curve,
                    "detect_count_threshold": configured_detect_count_threshold,
                    "clear_count_threshold": configured_clear_count_threshold,
                    "stale_clear_count_threshold": configured_stale_clear_count_threshold,
                    "data_timeout_sec": configured_data_timeout_sec,
                    "margin_step": configured_margin_step,
                }
            )
        finally:
            self._syncing_safety_supervisor_parameters = False

    # ======================
    # Safety Helpers
    # ======================
    # 토픽 입력의 존재, 신선도 확인
    def is_data_ready(self):
        now = rospy.Time.now()
        obstacle_is_fresh = (
            self.ob_stamp is not None
            and (now - self.ob_stamp).to_sec() <= self.data_timeout_sec
        )
        if not obstacle_is_fresh:
            return False
        return True

    def get_active_path_points(self):
        path_is_fresh = (
            self.path_stamp is not None
            and self.path_points
            and (rospy.Time.now() - self.path_stamp).to_sec() <= self.data_timeout_sec
        )
        if not path_is_fresh:
            return []
        return self.path_points[:self.path_count]

    # 경로 코리도어만큼 확장한 장애물 박스와 겹치는지 판정
    def point_in_expanded_box(self, px, py, box, expand):
        return (
            (box["min_x"] - expand) <= px <= (box["max_x"] + expand)
            and (box["min_y"] - expand) <= py <= (box["max_y"] + expand)
        )
    
    # roi 범위 계산
    def get_roi_distance(self):
        distance_span = max(0.0, self.max_check_distance - self.min_check_distance)
        if distance_span <= 1e-9:
            return self.min_check_distance

        linear_distance = max(0.0, self.speed * self.lookahead_time)
        normalized_distance = (linear_distance - self.min_check_distance) / distance_span
        normalized_distance = max(0.0, min(1.0, normalized_distance))

        curve = max(-1.0, min(1.0, self.roi_speed_curve))
        shaped_distance = normalized_distance + curve * (
            (normalized_distance * normalized_distance) - normalized_distance
        )

        return self.min_check_distance + (distance_span * shaped_distance)

    def get_collision_check_path_point_count(self, active_path_points):
        if self.path_step <= 0.0 or not active_path_points:
            return 0
        roi_distance = self.get_roi_distance()
        check_count = int(roi_distance / self.path_step) + 1
        return max(0, min(len(active_path_points), check_count))

    def is_collision_risk_on_path(self, active_path_points):
        if not active_path_points:
            return False
        margin_step = 0.0
        for px, py in active_path_points[:self.collision_check_path_point_count]:
            if px < 0.0:
                continue
            for box in self.obstacles:
                if self.point_in_expanded_box(px, py, box, self.path_width_margin - margin_step):
                    return True
            if margin_step != self.path_width_margin:
                margin_step += self.margin_step
        return False

    # 방어코드
    def update_interrupt_state(self, hazard_detected):
        if hazard_detected:
            self.detect_count += 1
            self.clear_count = 0
            if self.detect_count >= self.detect_count_threshold:
                self.interrupt_active = True
                self.last_estop_time = rospy.Time.now()  # E-STOP 발동 시간 기록
        else:
            self.clear_count += 1
            self.detect_count = 0
            if self.clear_count >= self.clear_count_threshold:
                self.interrupt_active = False

    def update_stale_clear_state(self):
        self.stale_clear_count += 1
        if self.stale_clear_count >= self.stale_clear_count_threshold:
            self.detect_count = 0
            self.clear_count = 0
            self.interrupt_active = False

    def publish_collision_check_path_point_count(self):
        self.collision_check_path_point_count_pub.publish(self.collision_check_path_point_count)

    def publish_interrupt(self):
        is_estop = self.interrupt_active
        # 마지막 E-STOP 기록이 있고, 현재 시각과의 차이가 estop_hold_time(3초) 미만이면 계속 정지 유지
        if not is_estop and self.last_estop_time is not None:
            if (rospy.Time.now() - self.last_estop_time).to_sec() < self.estop_hold_time:
                is_estop = True

        self.interrupt_pub.publish(is_estop)









if __name__ == "__main__":
    rospy.init_node("safety_supervisor", anonymous=False)
    node = SafetySupervisor()
    node.run()
