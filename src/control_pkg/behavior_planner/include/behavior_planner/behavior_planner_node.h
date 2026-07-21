#ifndef BEHAVIOR_PLANNER_NODE_H
#define BEHAVIOR_PLANNER_NODE_H

#include <cmath>
#include <geometry_msgs/PoseStamped.h>
#include <visualization_msgs/Marker.h>
#include <nav_msgs/Path.h>
#include <ros/package.h>
#include <ros/ros.h>
#include <std_msgs/Int32.h>
#include <ublox_msgs/NavPVT.h>
#include <erp42_msgs/SerialFeedBack.h>
#include <vector>

#include "behavior_planner/path_manager.h"
#include "behavior_planner/traffic_manager.h"

namespace behavior_planner {

class BehaviorPlannerNode {
public:
  BehaviorPlannerNode();
  void run();

private:
  ros::NodeHandle nh_;
  ros::NodeHandle pnh_;

  // Components
  PathManager path_manager_;
  TrafficManager traffic_manager_;

  // Subscribers
  ros::Subscriber sub_utm_;
  ros::Subscriber sub_navpvt_;
  ros::Subscriber sub_vision_path_;
  ros::Subscriber sub_lidar_path_;
  ros::Subscriber sub_feedback_;


  // Publishers
  ros::Publisher pub_target_path_;
  ros::Publisher pub_global_path_;
  ros::Publisher pub_path_marker_;
  ros::Publisher pub_local_gps_path_;

  ros::Publisher pub_current_idx_;

  // State
  struct VehicleState {
    double x = 0;
    double y = 0;
    double heading = 0;
  } car_;
  
  bool has_utm_ = false;
  ros::Time last_utm_time_;
  double last_gps_x_ = 0;
  double last_gps_y_ = 0;
  double velocity_heading_ = 0;
  bool velocity_heading_initialized_ = false;
  bool global_path_published_ = false;



  // Config
  std::string driving_mode_;
  std::string rddf_file_;
  std::string routing_mode_;
  double lookahead_distance_ = 8.0;
  double target_speed_ = 15.0;
  double vision_speed_ = 5.0;
  double vision_fallback_speed_ = 3.0;
  double vision_lookahead_ = 5.0;
  
  nav_msgs::Path vision_path_;
  bool has_vision_path_ = false;
  ros::Time last_vision_time_;

  nav_msgs::Path lidar_path_;
  bool has_lidar_path_ = false;
  ros::Time last_lidar_time_;
  double lidar_speed_    = 5.0;
  double lidar_lookahead_ = 5.0;

  // Steer-adaptive speed
  double current_steer_deg_ = 0.0;   // 현재 실제 조향각 (EMA 필터 적용, 도)
  double steer_ema_alpha_    = 0.2;  // 조향각 EMA 필터 계수 (0=고정, 1=raw)
  double speed_min_          = 5.0;  // 최대 조향 시 최소 속도
  double speed_max_          = 6.0;  // 직진 시 최대 속도
  double speed_steer_max_deg_ = 20.0; // 이 조향각 이상이면 speed_min 적용

  // Helpers
  double steerAdaptiveSpeed(double base_speed) const;

  // Callbacks
  void utmCallback(const geometry_msgs::PoseStamped::ConstPtr &msg);
  void navpvtCallback(const ublox_msgs::NavPVT::ConstPtr &msg);
  void visionPathCallback(const nav_msgs::Path::ConstPtr &msg);
  void lidarPathCallback(const nav_msgs::Path::ConstPtr &msg);
  void feedbackCallback(const erp42_msgs::SerialFeedBack::ConstPtr &msg);


  // Control Loop
  void planningLoop(const ros::TimerEvent &event);
  void publishGlobalPath();

  ros::Timer planning_timer_;
};

} // namespace behavior_planner

#endif // BEHAVIOR_PLANNER_NODE_H
