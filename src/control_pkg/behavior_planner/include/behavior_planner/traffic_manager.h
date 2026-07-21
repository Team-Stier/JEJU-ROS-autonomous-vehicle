#ifndef STIER_SYSTEM_TRAFFIC_MANAGER_H
#define STIER_SYSTEM_TRAFFIC_MANAGER_H

#include <ros/ros.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Int32.h>
#include <string>

namespace behavior_planner {

enum class DriveMode {
  PURE_PURSUIT = 0,
  STOP = 1,
  SLOW_DOWN = 2,
  SLOW_DOWN_2 = 3
};

class TrafficManager {
public:
  TrafficManager(ros::NodeHandle &nh);

  // Process current state and return the drive mode decision
  void process();

  DriveMode getDriveMode() const;

private:
  // Logic state
  DriveMode drive_mode_;
  bool dynamic_obstacle_detected_;

  // Data members (현재 사용 없음)

  // ROS interfaces
  ros::NodeHandle nh_;
  ros::Subscriber sub_mission_interrupt_;
  ros::Publisher pub_drive_state_;

  // Callbacks
  void interruptCallback(const std_msgs::Bool::ConstPtr &msg);

  // Helpers
  void processTrafficRules();
  void publishDriveState();
  void printInfo();
};

} // namespace behavior_planner

#endif // STIER_SYSTEM_TRAFFIC_MANAGER_H
