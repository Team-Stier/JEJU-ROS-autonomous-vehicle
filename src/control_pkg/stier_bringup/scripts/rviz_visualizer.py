#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA

class RvizVisualizer(object):
    def __init__(self):
        rospy.init_node('rviz_visualizer', anonymous=True)
        
        # Publishers
        self.pub_lidar = rospy.Publisher('/behavior_planner/lidar_marker', Marker, queue_size=1)
        self.pub_vision = rospy.Publisher('/behavior_planner/vision_marker', Marker, queue_size=1)
        self.pub_gps = rospy.Publisher('/behavior_planner/gps_marker', Marker, queue_size=1)
        self.pub_target = rospy.Publisher('/behavior_planner/path_marker', Marker, queue_size=1)
        
        # Subscribers
        rospy.Subscriber('/lidar_path', Path, self.lidar_cb, queue_size=1)
        rospy.Subscriber('/vision/lane_path', Path, self.vision_cb, queue_size=1)
        rospy.Subscriber('/local_gps_path', Path, self.gps_cb, queue_size=1)
        rospy.Subscriber('/target_path', Path, self.target_cb, queue_size=1)
        
        rospy.loginfo("RViz Visualizer node started.")

    def create_marker(self, path_msg, ns, r, g, b, a, scale_x):
        marker = Marker()
        # Keep original frame_id so RViz can auto-transform to 'stier' fixed frame
        marker.header = path_msg.header
        marker.ns = ns
        marker.id = 0
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.scale.x = scale_x
        
        marker.color = ColorRGBA(r, g, b, a)
        
        for pose_stamped in path_msg.poses:
            marker.points.append(pose_stamped.pose.position)
            
        return marker

    def lidar_cb(self, msg):
        if not msg.poses: return
        # Red, thin (0.05)
        marker = self.create_marker(msg, "lidar_path", 1.0, 0.0, 0.0, 0.8, 0.05)
        self.pub_lidar.publish(marker)

    def vision_cb(self, msg):
        if not msg.poses: return
        # Blue, thin (0.05)
        marker = self.create_marker(msg, "vision_path", 0.0, 0.0, 1.0, 0.8, 0.05)
        self.pub_vision.publish(marker)

    def gps_cb(self, msg):
        if not msg.poses: return
        # Green, thin (0.05)
        marker = self.create_marker(msg, "gps_path", 0.0, 1.0, 0.0, 0.8, 0.05)
        self.pub_gps.publish(marker)

    def target_cb(self, msg):
        if not msg.poses: return
        
        route_mode = rospy.get_param("/routing_mode_active", "gps")
        
        # Default yellow for thick line
        r, g, b = 1.0, 1.0, 0.0
        
        if route_mode == "lidar":
            r, g, b = 1.0, 0.0, 0.0 # Red
        elif route_mode == "vision":
            r, g, b = 0.0, 0.0, 1.0 # Blue
        elif route_mode == "gps":
            r, g, b = 0.0, 1.0, 0.0 # Green
            
        # Thick marker (0.2)
        marker = self.create_marker(msg, "thick_target_path", r, g, b, 0.8, 0.2)
        self.pub_target.publish(marker)

if __name__ == '__main__':
    try:
        viz = RvizVisualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
