#include "pure_pursuit/pure_pursuit_node.h"

#include <cmath>

using namespace std;
using namespace ros;

namespace pure_pursuit {

PurePursuitNode::PurePursuitNode() : pnh_("~") {
  // Parameters
  std::string ld_param = "/stier_params/lookahead_distance";
  std::string speed_param = "/stier_params/gps_speed";

  nh_.param<double>(ld_param, lookahead_distance_, 5.0);
  nh_.param<double>(speed_param, target_speed_, 5.0);
  nh_.param<std::string>("/routing_mode", routing_mode_, "gps");

  // Subscribers
  sub_target_path_ = nh_.subscribe("/target_path", 1, &PurePursuitNode::targetPathCallback, this);
  sub_utm_ = nh_.subscribe("/utm", 1, &PurePursuitNode::utmCallback, this);
  sub_navpvt_ = nh_.subscribe("/ublox_position_receiver/navpvt", 1, &PurePursuitNode::navpvtCallback, this);
  sub_feedback_ = nh_.subscribe("/erp42_serial/feedback", 1, &PurePursuitNode::feedbackCallback, this);
  sub_drive_state_ = nh_.subscribe("/drive_state", 1, &PurePursuitNode::driveStateCallback, this);

  // Publishers
  pub_drive_cmd_ = nh_.advertise<erp42_msgs::DriveCmd>("/pure_pursuit/raw_drive", 1);
  pub_vehicle_marker_ = nh_.advertise<visualization_msgs::Marker>("/vehicle_viz", 1);
  pub_target_marker_ = nh_.advertise<visualization_msgs::Marker>("/pf_target", 1);

  // Timer
  // Run control loop at 20Hz
  control_timer_ = nh_.createTimer(ros::Duration(1.0 / 5.0), &PurePursuitNode::controlLoop, this);

  ROS_INFO("=================================================");
  ROS_INFO(" PurePursuitNode Initialized");

  ROS_INFO(" - Routing Mode: %s", routing_mode_.c_str());
  ROS_INFO(" - L.Distance : %.1f m", lookahead_distance_);
  ROS_INFO(" - Target Speed: %.1f kph", target_speed_);
  ROS_INFO("=================================================");
}

void PurePursuitNode::run() { ros::spin(); }

void PurePursuitNode::targetPathCallback(const nav_msgs::Path::ConstPtr &msg) {
  target_path_ = *msg;
  has_target_path_ = true;
}

void PurePursuitNode::utmCallback(const geometry_msgs::PoseStamped::ConstPtr &msg) {
  car_.x = msg->pose.position.x;
  car_.y = msg->pose.position.y;
}

void PurePursuitNode::navpvtCallback(const ublox_msgs::NavPVT::ConstPtr &msg) {
  // Speed mm/s -> kph (항상 업데이트)
  car_.speed = msg->gSpeed * 0.0036;

  // Heading in degrees 1e-5 (North=0, CW+)
  double heading_deg = msg->heading * 1e-5;
  car_.heading = heading_deg * M_PI / 180.0;
}

void PurePursuitNode::feedbackCallback(const erp42_msgs::SerialFeedBack::ConstPtr &msg) {
  car_.steer_feedback = msg->steer;
}

void PurePursuitNode::driveStateCallback(const std_msgs::Int32::ConstPtr &msg) {
  // DriveMode::STOP = 1
  estop_active_ = (msg->data == 1);
}



void PurePursuitNode::controlLoop(const ros::TimerEvent &event) {
  // 0. 동적 장애물 Estop 최우선 처리 (아래 최종 명령단에서 처리하도록 이동됨)
  // Update modes dynamically
  nh_.getParam("/routing_mode", routing_mode_); // Test Mode or Hybrid Mode
  
  std::string active_mode;
  nh_.getParam("/routing_mode_active", active_mode); // vision or gps

  // Prioritize active parameters from planner
  bool has_active_speed = nh_.getParam("/active_target_speed", target_speed_);
  bool has_active_ld = nh_.getParam("/active_lookahead", lookahead_distance_);

  if (!has_active_speed || !has_active_ld || (target_speed_ == 0.0 && routing_mode_ != "vision")) {
      // Fallback to YAML for standard GPS mode if planner is not providing valid speed
      std::string ld_param = "/stier_params/lookahead_distance";
      nh_.getParam(ld_param, lookahead_distance_);
      
      std::string sp_param = "/stier_params/gps_speed";
      nh_.getParam(sp_param, target_speed_);
  }
  visualization_msgs::Marker vehicle_marker;
  vehicle_marker.header.stamp = ros::Time::now();
  vehicle_marker.ns = "vehicle";
  vehicle_marker.id = 0;
  vehicle_marker.type = visualization_msgs::Marker::CUBE;
  vehicle_marker.action = visualization_msgs::Marker::ADD;

  if (routing_mode_ == "vision") {
      vehicle_marker.header.frame_id = "stier";
      vehicle_marker.pose.position.x = 0.0;
      vehicle_marker.pose.position.y = 0.0;
      vehicle_marker.pose.position.z = 0.1;
      vehicle_marker.pose.orientation.x = 0.0;
      vehicle_marker.pose.orientation.y = 0.0;
      vehicle_marker.pose.orientation.z = 0.0;
      vehicle_marker.pose.orientation.w = 1.0;
  } else {
      vehicle_marker.header.frame_id = "utm";
      vehicle_marker.pose.position.x = car_.x;
      vehicle_marker.pose.position.y = car_.y;
      vehicle_marker.pose.position.z = 0.1;
      
      double enu_yaw = M_PI / 2.0 - car_.heading;
      vehicle_marker.pose.orientation.x = 0.0;
      vehicle_marker.pose.orientation.y = 0.0;
      vehicle_marker.pose.orientation.z = std::sin(enu_yaw / 2.0);
      vehicle_marker.pose.orientation.w = std::cos(enu_yaw / 2.0);
  }
  vehicle_marker.scale.x = 1.6;
  vehicle_marker.scale.y = 1.1;
  vehicle_marker.scale.z = 0.5;
  vehicle_marker.color.a = 0.7;
  vehicle_marker.color.r = 0.0;
  vehicle_marker.color.g = 0.5;
  vehicle_marker.color.b = 1.0;
  pub_vehicle_marker_.publish(vehicle_marker);

  // 2. Control Logic
  if (!has_target_path_ || target_path_.poses.empty()) {
    erp42_msgs::DriveCmd stop_cmd;
    stop_cmd.KPH = 0;
    stop_cmd.Deg = static_cast<int>(car_.steer_feedback);
    stop_cmd.brake = 1;
    pub_drive_cmd_.publish(stop_cmd);
    return;
  }

  nav_msgs::Path *active_path = &target_path_;
  bool found_target = false;
  double target_x = 0;
  double target_y = 0;
  size_t target_idx = 0;

  bool is_local_frame = (active_path->header.frame_id == "stier" || active_path->header.frame_id == "velodyne");
  
  // Effective car state for control
  double v_x = is_local_frame ? 0.0 : car_.x;
  double v_y = is_local_frame ? 0.0 : car_.y;
  double v_h = is_local_frame ? 0.0 : car_.heading;

  for (size_t i = 0; i < active_path->poses.size(); ++i) {
    double px = active_path->poses[i].pose.position.x;
    double py = active_path->poses[i].pose.position.y;
    double dist = std::hypot(px - v_x, py - v_y);

    if (dist >= lookahead_distance_) {
      target_x = px;
      target_y = py;
      target_idx = i;
      found_target = true;
      break;
    }
  }

  if (!found_target && !active_path->poses.empty()) {
    target_idx = active_path->poses.size() - 1;
    target_x = active_path->poses[target_idx].pose.position.x;
    target_y = active_path->poses[target_idx].pose.position.y;
    found_target = true;
  }

  if (found_target) {
    double steer_deg = 0;
    if (active_path->header.frame_id == "velodyne") {
      // velodyne 프레임 (전방 X축, 왼쪽 Y축)
      steer_deg = pure_pursuit_.calculateSteer(0, 0, 0, -target_y, target_x);
    } else if (active_path->header.frame_id == "stier") {
      // stier 프레임도 전방 X, 좌측 Y
      steer_deg = pure_pursuit_.calculateSteer(0, 0, 0, -target_y, target_x);
    } else {
      // GPS 모드 (utm 프레임)
      steer_deg = pure_pursuit_.calculateSteer(car_.x, car_.y, car_.heading, target_x, target_y);
    }


    erp42_msgs::DriveCmd drive_cmd;

    if (estop_active_) {
      drive_cmd.KPH = 0;
      drive_cmd.Deg = static_cast<int>(steer_deg);
      drive_cmd.brake = 1;
      ROS_WARN_THROTTLE(1.0, "[PurePursuit] ESTOP ACTIVE - Vehicle stopped but steering updating");
    } else {
      drive_cmd.KPH = static_cast<int>(target_speed_);
      drive_cmd.Deg = static_cast<int>(steer_deg);
      drive_cmd.brake = 0;
    }
    pub_drive_cmd_.publish(drive_cmd);

    ROS_INFO_THROTTLE(1.0, "[%s] Control Active - Spd: %.1f, Steer: %.1f, LD: %.1f, PathSize: %zu, Frame: %s", 
        active_mode.c_str(), target_speed_, steer_deg, lookahead_distance_, active_path->poses.size(), active_path->header.frame_id.c_str());

    // Visualization Markers
    visualization_msgs::Marker target_marker;
    target_marker.header.frame_id = active_path->header.frame_id;
    target_marker.header.stamp = ros::Time::now();
    target_marker.ns = "target";
    target_marker.id = 1;
    target_marker.type = visualization_msgs::Marker::SPHERE;
    target_marker.pose.position.x = target_x;
    target_marker.pose.position.y = target_y;
    target_marker.pose.position.z = 0.0;
    target_marker.pose.orientation.w = 1.0;
    target_marker.scale.x = 0.5; target_marker.scale.y = 0.5; target_marker.scale.z = 0.5;
    target_marker.color.a = 1.0; target_marker.color.r = 1.0; target_marker.color.g = 0.0; target_marker.color.b = 0.0;
    pub_target_marker_.publish(target_marker);

    pub_target_marker_.publish(target_marker);

    // Pure Pursuit logic continues...
  } else {
    erp42_msgs::DriveCmd real_cmd;
    real_cmd.KPH = 0;
    real_cmd.Deg = static_cast<int>(car_.steer_feedback);
    real_cmd.brake = 1;
    pub_drive_cmd_.publish(real_cmd);
  }
}

} // namespace pure_pursuit
