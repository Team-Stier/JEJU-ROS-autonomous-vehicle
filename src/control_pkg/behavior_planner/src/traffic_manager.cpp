#include "behavior_planner/traffic_manager.h"
#include <iostream>

namespace behavior_planner {

using namespace std;

TrafficManager::TrafficManager(ros::NodeHandle &nh)
    : nh_(nh) { // Initialize ref instead of internal NH
  // Subscribers
  sub_mission_interrupt_ = nh_.subscribe("/mission_interrupt", 1, &TrafficManager::interruptCallback, this);

  // Publishers
  pub_drive_state_ = nh_.advertise<std_msgs::Int32>("/drive_state", 1);

  // Initialize state
  drive_mode_ = DriveMode::PURE_PURSUIT;
  dynamic_obstacle_detected_ = false;

  ROS_INFO("TrafficManager initialized for dynamic obstacles ONLY.");
}

void TrafficManager::process() {
  processTrafficRules();
  publishDriveState();
  printInfo();
}

DriveMode TrafficManager::getDriveMode() const { return drive_mode_; }

// Callbacks
void TrafficManager::interruptCallback(const std_msgs::Bool::ConstPtr &msg) {
  dynamic_obstacle_detected_ = msg->data;
}

// Logic
void TrafficManager::processTrafficRules() {
  if (dynamic_obstacle_detected_) {
    drive_mode_ = DriveMode::STOP;
  } else {
    drive_mode_ = DriveMode::PURE_PURSUIT;
  }
}

void TrafficManager::publishDriveState() {
  static ros::Time last_pub_time = ros::Time(0);
  double interval = 0.1; // 10Hz (상태 판단은 20Hz로 하되 발행은 10Hz로 제한)

  if ((ros::Time::now() - last_pub_time).toSec() >= interval) {
    std_msgs::Int32 msg;
    msg.data = static_cast<int>(drive_mode_);
    pub_drive_state_.publish(msg);
    last_pub_time = ros::Time::now();
  }
}

void TrafficManager::printInfo() {
  static ros::Time last_print = ros::Time(0);
  if ((ros::Time::now() - last_print).toSec() > 0.5) {
    // Determine driving mode string or use routing mode equivalent if needed.
    // The user requested: "주행모드도 lane, gps 등으로 해주고 obstacle 말고 estop o,x로"
    // To get "lane, gps" we need to read from the parameter server just like behavior_planner_node does
    // since routing mode is managed there. For now, we will fetch "/routing_mode_active" parameter.
    
    std::string active_mode = "unknown";
    nh_.getParam("/routing_mode_active", active_mode);

    std::string estop_str = dynamic_obstacle_detected_ ? "O" : "X";

    std::cout << "Traffic | Mode: " << active_mode 
              << " | Estop: " << estop_str << std::endl;
    last_print = ros::Time::now();
  }
}

} // namespace behavior_planner
