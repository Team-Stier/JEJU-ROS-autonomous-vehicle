#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from std_msgs.msg import Bool, Int32
from visualization_msgs.msg import Marker, MarkerArray


class PredictedPathVisualizer:
    def __init__(self):
        rospy.init_node("predicted_path_visualizer", anonymous=False)

        self.default_frame_id = "velodyne"
        self.marker_topic = "/predicted_path_marker_array"
        self.marker_specs = (
            (0, "predicted_path_max_range"),
            (1, "predicted_path_checked"),
            (2, "predicted_path_corridor_max_left"),
            (3, "predicted_path_corridor_max_right"),
            (4, "predicted_path_corridor_checked_left"),
            (5, "predicted_path_corridor_checked_right"),
            (6, "predicted_path_remaining"),
            (7, "predicted_path_checked_distance"),
        )
        self.path_timeout_sec = 0.5
        self.line_width = 0.08
        self.corridor_line_width = 0.04
        self.distance_text_scale = 1
        self.distance_text_position_x = 0.0
        self.distance_text_position_y = -2.0
        self.distance_text_position_z = 0.85
        self.path_width_margin = 0.5
        self.margin_step = 0.05
        self.path_step = 0.2
        self.max_check_distance = 10.0
        self.predicted_path_step_param = "/safety_supervisor/predicted_path_parameters/path_step"
        self.safety_path_width_margin_param = "/safety_supervisor/safety_supervisor_parameters/path_width_margin"
        self.safety_max_check_distance_param = "/safety_supervisor/safety_supervisor_parameters/max_check_distance"
        self.safety_data_timeout_sec_param = "/safety_supervisor/safety_supervisor_parameters/data_timeout_sec"
        self.safety_margin_step_param = "/safety_supervisor/safety_supervisor_parameters/margin_step"

        self.path_points = []
        self.path_frame_id = self.default_frame_id
        self.path_stamp = None
        self.collision_check_path_point_count = 0
        self.mission_interrupt = False

        rospy.Subscriber("/predicted_path", Path, self.callback_path)
        rospy.Subscriber("/collision_check_path_point_count", Int32, self.callback_check_count)
        rospy.Subscriber("/mission_interrupt", Bool, self.callback_interrupt)
        self.marker_pub = rospy.Publisher(self.marker_topic, MarkerArray, queue_size=1)

        self.load_safety_supervisor_parameters()
        self.rate = rospy.Rate(20)

    def run(self):
        while not rospy.is_shutdown():
            self.sync_safety_supervisor_parameters()
            self.publish_path_markers()
            self.rate.sleep()

    # ======================
    # Callbacks
    # ======================
    def callback_path(self, msg):
        self.path_points = [
            (pose.pose.position.x, pose.pose.position.y)
            for pose in msg.poses
        ]
        self.path_frame_id = msg.header.frame_id or self.default_frame_id
        self.path_stamp = rospy.Time.now()

    def callback_check_count(self, msg):
        self.collision_check_path_point_count = max(0, int(msg.data))

    def callback_interrupt(self, msg):
        self.mission_interrupt = bool(msg.data)

    # ======================
    # Parameter Sync
    # ======================
    def load_safety_supervisor_parameters(self):
        self.path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        self.path_width_margin = float(rospy.get_param(self.safety_path_width_margin_param, self.path_width_margin))
        self.max_check_distance = float(rospy.get_param(self.safety_max_check_distance_param, self.max_check_distance))
        self.path_timeout_sec = float(rospy.get_param(self.safety_data_timeout_sec_param, self.path_timeout_sec))
        self.margin_step = float(rospy.get_param(self.safety_margin_step_param, self.margin_step))

    def sync_safety_supervisor_parameters(self):
        self.path_step = float(rospy.get_param(self.predicted_path_step_param, self.path_step))
        self.path_width_margin = float(rospy.get_param(self.safety_path_width_margin_param, self.path_width_margin))
        self.max_check_distance = float(rospy.get_param(self.safety_max_check_distance_param, self.max_check_distance))
        self.path_timeout_sec = float(rospy.get_param(self.safety_data_timeout_sec_param, self.path_timeout_sec))
        self.margin_step = float(rospy.get_param(self.safety_margin_step_param, self.margin_step))

    # ======================
    # Marker Helpers
    # ======================
    def has_fresh_path(self):
        if self.path_stamp is None or not self.path_points:
            return False
        return (rospy.Time.now() - self.path_stamp).to_sec() <= self.path_timeout_sec

    def create_delete_marker(self, marker_id, ns):
        marker = Marker()
        marker.header.frame_id = self.path_frame_id
        marker.header.stamp = rospy.Time.now()
        marker.ns = ns
        marker.id = marker_id
        marker.action = Marker.DELETE
        return marker

    def create_line_strip_marker(self, marker_id, ns, points, color):
        marker = Marker()
        marker.header.frame_id = self.path_frame_id
        marker.header.stamp = rospy.Time.now()
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.scale.x = self.line_width
        marker.color.a = 1.0
        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.lifetime = rospy.Duration(0.0)

        for px, py in points:
            point = Point()
            point.x = px
            point.y = py
            point.z = 0.0
            marker.points.append(point)

        return marker

    def create_corridor_marker(self, marker_id, ns, points, color):
        marker = self.create_line_strip_marker(marker_id, ns, points, color)
        marker.scale.x = self.corridor_line_width
        return marker

    def create_distance_text_marker(self, marker_id, ns, distance_m):
        marker = Marker()
        marker.header.frame_id = self.path_frame_id
        marker.header.stamp = rospy.Time.now()
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.frame_locked = True
        marker.pose.position.x = self.distance_text_position_x
        marker.pose.position.y = self.distance_text_position_y
        marker.pose.position.z = self.distance_text_position_z
        marker.pose.orientation.w = 1.0
        marker.scale.z = self.distance_text_scale
        marker.color.a = 1.0
        if self.mission_interrupt:
            marker.color.r = 1.0
            marker.color.g = 0.25
            marker.color.b = 0.25
        else:
            marker.color.r = 1.0
            marker.color.g = 1.0
            marker.color.b = 1.0
        marker.lifetime = rospy.Duration(0.0)
        marker.text = "{:.2f} m".format(distance_m)
        return marker

    def build_clear_marker_array(self):
        marker_array = MarkerArray()
        for marker_id, ns in self.marker_specs:
            marker_array.markers.append(self.create_delete_marker(marker_id, ns))
        return marker_array

    def get_max_check_path_point_count(self):
        if self.path_step <= 0.0 or not self.path_points:
            return 0
        max_count = int(self.max_check_distance / self.path_step) + 1
        return max(0, min(len(self.path_points), max_count))

    def get_path_colors(self):
        if self.mission_interrupt:
            return {
                "checked_path": (1.0, 0.1, 0.1),
                "checked_corridor": (1.0, 0.3, 0.3),
                "max_range_path": (1.0, 0.6, 0.2),
                "max_range_corridor": (1.0, 0.75, 0.45),
                "remaining_path": (1.0, 0.6, 0.6),
            }
        return {
            "checked_path": (1.0, 0.7, 0.0),
            "checked_corridor": (1.0, 1.0, 0.3),
            "max_range_path": (0.0, 0.8, 1.0),
            "max_range_corridor": (0.4, 0.95, 1.0),
            "remaining_path": (0.7, 0.7, 0.7),
        }

    def build_indexed_segment(self, start_index, end_index):
        point_count = len(self.path_points)
        start_index = max(0, min(start_index, point_count))
        end_index = max(0, min(end_index, point_count))
        if end_index <= start_index:
            return []

        first_index = start_index if start_index == 0 else start_index - 1
        return [
            (path_index, self.path_points[path_index])
            for path_index in range(first_index, end_index)
        ]

    def extract_points(self, indexed_points):
        return [point for _, point in indexed_points]

    def get_point_margin(self, path_index):
        return max(0.0, self.path_width_margin - (path_index * self.margin_step))

    def compute_offset_path(self, indexed_points, side_sign):
        if len(indexed_points) < 2:
            return []

        offset_points = []
        for index, (path_index, (px, py)) in enumerate(indexed_points):
            if index == 0:
                ref_prev = indexed_points[index][1]
                ref_next = indexed_points[index + 1][1]
            elif index == len(indexed_points) - 1:
                ref_prev = indexed_points[index - 1][1]
                ref_next = indexed_points[index][1]
            else:
                ref_prev = indexed_points[index - 1][1]
                ref_next = indexed_points[index + 1][1]

            tangent_x = ref_next[0] - ref_prev[0]
            tangent_y = ref_next[1] - ref_prev[1]
            tangent_norm = (tangent_x ** 2 + tangent_y ** 2) ** 0.5
            if tangent_norm <= 1e-9:
                normal_x, normal_y = 0.0, 0.0
            else:
                normal_x = -tangent_y / tangent_norm
                normal_y = tangent_x / tangent_norm

            offset = side_sign * self.get_point_margin(path_index)
            offset_points.append((px + normal_x * offset, py + normal_y * offset))

        return offset_points

    def publish_path_markers(self):
        if not self.has_fresh_path():
            self.marker_pub.publish(self.build_clear_marker_array())
            return

        marker_array = MarkerArray()
        max_check_count = self.get_max_check_path_point_count()
        checked_count = max(0, min(self.collision_check_path_point_count, max_check_count))

        # Split the path into non-overlapping segments to avoid RViz z-fighting.
        checked_segment = self.build_indexed_segment(0, checked_count)
        max_range_segment = self.build_indexed_segment(checked_count, max_check_count)
        remaining_segment = self.build_indexed_segment(max_check_count, len(self.path_points))
        checked_distance_m = checked_count * self.path_step
        colors = self.get_path_colors()

        if max_range_segment:
            marker_array.markers.append(
                self.create_line_strip_marker(
                    0,
                    "predicted_path_max_range",
                    self.extract_points(max_range_segment),
                    colors["max_range_path"],
                )
            )
            left_corridor = self.compute_offset_path(max_range_segment, 1.0)
            right_corridor = self.compute_offset_path(max_range_segment, -1.0)
            if left_corridor:
                marker_array.markers.append(
                    self.create_corridor_marker(
                        2,
                        "predicted_path_corridor_max_left",
                        left_corridor,
                        colors["max_range_corridor"],
                    )
                )
            else:
                marker_array.markers.append(
                    self.create_delete_marker(2, "predicted_path_corridor_max_left")
                )
            if right_corridor:
                marker_array.markers.append(
                    self.create_corridor_marker(
                        3,
                        "predicted_path_corridor_max_right",
                        right_corridor,
                        colors["max_range_corridor"],
                    )
                )
            else:
                marker_array.markers.append(
                    self.create_delete_marker(3, "predicted_path_corridor_max_right")
                )
        else:
            marker_array.markers.append(self.create_delete_marker(0, "predicted_path_max_range"))
            marker_array.markers.append(self.create_delete_marker(2, "predicted_path_corridor_max_left"))
            marker_array.markers.append(self.create_delete_marker(3, "predicted_path_corridor_max_right"))

        if checked_segment:
            marker_array.markers.append(
                self.create_line_strip_marker(
                    1,
                    "predicted_path_checked",
                    self.extract_points(checked_segment),
                    colors["checked_path"],
                )
            )
            left_corridor = self.compute_offset_path(checked_segment, 1.0)
            right_corridor = self.compute_offset_path(checked_segment, -1.0)
            if left_corridor:
                marker_array.markers.append(
                    self.create_corridor_marker(
                        4,
                        "predicted_path_corridor_checked_left",
                        left_corridor,
                        colors["checked_corridor"],
                    )
                )
            else:
                marker_array.markers.append(
                    self.create_delete_marker(4, "predicted_path_corridor_checked_left")
                )
            if right_corridor:
                marker_array.markers.append(
                    self.create_corridor_marker(
                        5,
                        "predicted_path_corridor_checked_right",
                        right_corridor,
                        colors["checked_corridor"],
                    )
                )
            else:
                marker_array.markers.append(
                    self.create_delete_marker(5, "predicted_path_corridor_checked_right")
                )
        else:
            marker_array.markers.append(self.create_delete_marker(1, "predicted_path_checked"))
            marker_array.markers.append(self.create_delete_marker(4, "predicted_path_corridor_checked_left"))
            marker_array.markers.append(self.create_delete_marker(5, "predicted_path_corridor_checked_right"))

        if remaining_segment:
            marker_array.markers.append(
                self.create_line_strip_marker(
                    6,
                    "predicted_path_remaining",
                    self.extract_points(remaining_segment),
                    colors["remaining_path"],
                )
            )
        else:
            marker_array.markers.append(self.create_delete_marker(6, "predicted_path_remaining"))

        marker_array.markers.append(
            self.create_distance_text_marker(
                7,
                "predicted_path_checked_distance",
                checked_distance_m,
            )
        )

        self.marker_pub.publish(marker_array)


if __name__ == "__main__":
    node = PredictedPathVisualizer()
    node.run()
