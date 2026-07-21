#ifndef PURE_PURSUIT_NODE_H
#define PURE_PURSUIT_NODE_H

#include <erp42_msgs/DriveCmd.h>
#include <erp42_msgs/SerialFeedBack.h>
#include <geometry_msgs/PoseStamped.h>
#include <nav_msgs/Path.h>
#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Bool.h>
#include <ublox_msgs/NavPVT.h>
#include <visualization_msgs/Marker.h>



#include "pure_pursuit/pure_pursuit.h"

namespace pure_pursuit {

class PurePursuitNode {
public:
  PurePursuitNode();
  void run();

private:
  ros::NodeHandle nh_;
  ros::NodeHandle pnh_;

  // Components
  PurePursuit pure_pursuit_;

  // Subscribers
  ros::Subscriber sub_target_path_;
  ros::Subscriber sub_utm_;
  ros::Subscriber sub_navpvt_;
  ros::Subscriber sub_feedback_;
  ros::Subscriber sub_drive_state_;

  // Publishers
  ros::Publisher pub_drive_cmd_;
  ros::Publisher pub_vehicle_marker_;
  ros::Publisher pub_target_marker_;

  std::string routing_mode_;

  // State
  struct VehicleState {
    double x = 0;
    double y = 0;
    double heading = 0;
    double speed = 0;
    int steer_feedback = 0;
  } car_;

  nav_msgs::Path target_path_;
  bool has_target_path_ = false;
  bool estop_active_ = false; // traffic_manager의 STOP 명령 수신 여부

  // GPS 헤딩 필터링
  bool heading_initialized_ = false;     // 첫 헤딩 수신 여부
  double heading_ema_alpha_ = 0.15;      // EMA 계수 (0.1=강한필터, 0.3=빠른반응)
  double min_speed_for_heading_update_ = 2.0; // 헤딩 갱신 최소 속도 (kph)



  // Config
  double lookahead_distance_;
  double target_speed_;

  // Callbacks
  void targetPathCallback(const nav_msgs::Path::ConstPtr &msg);
  void utmCallback(const geometry_msgs::PoseStamped::ConstPtr &msg);
  void navpvtCallback(const ublox_msgs::NavPVT::ConstPtr &msg);
  void feedbackCallback(const erp42_msgs::SerialFeedBack::ConstPtr &msg);
  void driveStateCallback(const std_msgs::Int32::ConstPtr &msg);

  // Control Loop
  void controlLoop(const ros::TimerEvent &event);

  ros::Timer control_timer_;
};

} // namespace pure_pursuit

#endif // PURE_PURSUIT_NODE_H
