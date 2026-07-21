#!/usr/bin/env python3

import rospy
from erp42_msgs.msg import DriveCmd
from std_msgs.msg import Int32
import os

class ControlLogger:
    def __init__(self):
        rospy.init_node('control_logger')

        self.estop = False
        self.mode = "UNKNOWN"
        self.speed_cmd = 0.0
        self.steer_cmd = 0.0
        self.ld = 0.0

        # Subscribers
        rospy.Subscriber('/drive_state', Int32, self.estop_cb)
        rospy.Subscriber('/erp42_serial/drive', DriveCmd, self.drive_cb)

        # Timer for UI update (10Hz)
        self.timer = rospy.Timer(rospy.Duration(0.1), self.update_ui)

    def estop_cb(self, msg):
        self.estop = (msg.data == 1)

    def drive_cb(self, msg):
        self.speed_cmd = msg.KPH
        self.steer_cmd = msg.Deg

    def update_ui(self, event):
        # Fetch status from parameters
        self.mode = rospy.get_param('/routing_mode_active', 'N/A')
        self.ld = rospy.get_param('/active_lookahead', 0.0)

        # Clear screen
        os.system('clear')

        print("======================================================")
        print("          STIER CONTROL SYSTEM MONITOR                ")
        print("======================================================")
        print("")

        # E-Stop Status (ANSI Color)
        estop_str = "\033[91m [!] EMERGENCY STOP ACTIVE \033[0m" if self.estop else "\033[92m [ ] NORMAL OPERATION \033[0m"
        print(f" STATUS : {estop_str}")
        print("")

        # Mode Display
        mode_color = "\033[94m" # Blue default
        if self.mode == "gps": mode_color = "\033[92m" # Green
        elif self.mode == "vision": mode_color = "\033[93m" # Yellow
        elif self.mode == "lidar": mode_color = "\033[95m" # Purple
        
        print(f" DRIVE MODE : {mode_color}{self.mode.upper()}\033[0m")
        print("")

        print(f" TARGET SPEED : {self.speed_cmd:>5} KPH")
        print(f" STEER ANGLE  : {self.steer_cmd:>5} DEG (Input)")
        print(f" LOOKAHEAD(LD): {self.ld:>5.1f} M")
        print("")
        print("======================================================")
        print(" [CTRL+C] to close this monitor window.")

if __name__ == '__main__':
    try:
        logger = ControlLogger()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
