#!/usr/bin/env python3
import rospy
import tf
from geometry_msgs.msg import PoseStamped
from ublox_msgs.msg import NavPVT
import math

class UtmTfBroadcaster:
    def __init__(self):
        rospy.init_node('utm_tf_broadcaster')
        self.br = tf.TransformBroadcaster()
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        
        rospy.Subscriber('/utm', PoseStamped, self.utm_cb)
        rospy.Subscriber('/ublox_position_receiver/navpvt', NavPVT, self.navpvt_cb)
        
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            self.broadcast()
            rate.sleep()
            
    def utm_cb(self, msg):
        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        
    def navpvt_cb(self, msg):
        # ublox heading is 1e-5 degrees
        heading_deg = msg.heading * 1e-5
        # ENU yaw: East=0, North=90, CCW+
        # GPS heading: North=0, East=90, CW+
        # yaw = 90 - heading
        self.heading = math.radians(90.0 - heading_deg)
        
    def broadcast(self):
        quaternion = tf.transformations.quaternion_from_euler(0, 0, self.heading)
        self.br.sendTransform(
            (self.x, self.y, 0),
            quaternion,
            rospy.Time.now(),
            "stier", # child
            "utm" # parent
        )

if __name__ == '__main__':
    UtmTfBroadcaster()
