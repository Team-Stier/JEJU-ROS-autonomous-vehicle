#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m

import rospy
from visualization_msgs.msg import Marker, MarkerArray

from lidar_interfaces.msg import ObjectInfo


class VoxelVisualizer:
    def __init__(self):
        # ---- 시각화 파라미터 ----
        self.frame_id = rospy.get_param('~frame_id', 'velodyne')
        self.marker_topic = rospy.get_param('~marker_topic', '/voxel_visualization_marker_array')
        self.alpha = rospy.get_param('~alpha', 0.8)
        self.min_scale = rospy.get_param('~min_scale', 0.05)
        self.color_r = rospy.get_param('~color_r', 0.0)
        self.color_g = rospy.get_param('~color_g', 0.8)
        self.color_b = rospy.get_param('~color_b', 1.0)
        self.merge_threshold = rospy.get_param('~merge_threshold', 0.3)
        self.detection_range_x = (
            rospy.get_param('~range_x_min', 0.0),
            rospy.get_param('~range_x_max', 10.0),
        )
        self.detection_range_y = (
            rospy.get_param('~range_y_min', -5.0),
            rospy.get_param('~range_y_max', 5.0),
        )

        # ---- 런타임 캐시 ----
        self.voxels = []
        self.current_detected_voxels = set()

        rospy.init_node('voxel_visualizer')

        # ---- ROS I/O ----
        rospy.Subscriber('/voxel_info', ObjectInfo, self.callback_voxel)
        self.marker_pub = rospy.Publisher(self.marker_topic, MarkerArray, queue_size=10)

        self.rate = rospy.Rate(20)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

    # ======================
    # callbacks
    # ======================

    def callback_voxel(self, msg):
        self.current_detected_voxels.clear()

        voxel_count = max(
            0,
            min(
                int(msg.objectCounts),
                len(msg.centerX),
                len(msg.centerY),
                len(msg.centerZ),
                len(msg.lengthX),
                len(msg.lengthY),
                len(msg.lengthZ),
            ),
        )

        for i in range(voxel_count):
            self.update_voxel_list(
                msg.centerX[i],
                msg.centerY[i],
                msg.centerZ[i],
                max(msg.lengthX[i], self.min_scale),
                max(msg.lengthY[i], self.min_scale),
                max(msg.lengthZ[i], self.min_scale),
            )

        self.update_voxels()
        self.publish_voxel_markers()

    # ======================
    # Voxel Helpers
    # ======================
    def is_in_detection_range(self, x, y):
        return (
            self.detection_range_x[0] <= x <= self.detection_range_x[1]
            and self.detection_range_y[0] <= y <= self.detection_range_y[1]
        )

    def update_voxel_list(self, x, y, z, scale_x, scale_y, scale_z):
        if not self.is_in_detection_range(x, y):
            return

        merged = False
        for voxel in self.voxels:
            distance = m.sqrt((x - voxel['x']) ** 2 + (y - voxel['y']) ** 2)
            if distance < self.merge_threshold:
                voxel['x'] = x
                voxel['y'] = y
                voxel['z'] = z
                voxel['scale_x'] = scale_x
                voxel['scale_y'] = scale_y
                voxel['scale_z'] = scale_z
                voxel['confidence'] = min(1.0, voxel['confidence'] + 0.2)
                self.current_detected_voxels.add(id(voxel))
                merged = True
                break

        if not merged:
            new_voxel = {
                'x': x,
                'y': y,
                'z': z,
                'scale_x': scale_x,
                'scale_y': scale_y,
                'scale_z': scale_z,
                'confidence': 0.5,
            }
            self.voxels.append(new_voxel)
            self.current_detected_voxels.add(id(new_voxel))

    def update_voxels(self):
        for voxel in self.voxels:
            if id(voxel) not in self.current_detected_voxels:
                voxel['confidence'] = max(0.0, voxel['confidence'] - 0.4)

        self.voxels = [voxel for voxel in self.voxels if voxel['confidence'] > 0.05]

    # ======================
    # Publish Helpers
    # ======================
    def publish_voxel_markers(self):
        marker_array = MarkerArray()
        for i, voxel in enumerate(self.voxels):
            marker_array.markers.append(self.create_voxel_marker(i, voxel))
        self.marker_pub.publish(marker_array)

    def create_voxel_marker(self, marker_id, voxel):
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = rospy.Time.now()
        marker.ns = 'voxels'
        marker.id = marker_id
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.x = voxel['x']
        marker.pose.position.y = voxel['y']
        marker.pose.position.z = voxel['z']
        marker.pose.orientation.w = 1.0
        marker.scale.x = voxel['scale_x']
        marker.scale.y = voxel['scale_y']
        marker.scale.z = voxel['scale_z']
        marker.color.a = self.alpha
        marker.color.r = self.color_r
        marker.color.g = self.color_g
        marker.color.b = self.color_b
        marker.lifetime = rospy.Duration(0.5)
        return marker

if __name__ == '__main__':
    visualizer = VoxelVisualizer()
    visualizer.run()
