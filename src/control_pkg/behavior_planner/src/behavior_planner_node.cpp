#include "behavior_planner/behavior_planner_node.h"

using namespace std;
using namespace ros;

namespace behavior_planner {

BehaviorPlannerNode::BehaviorPlannerNode()
    : pnh_("~"), traffic_manager_(nh_) {
  
  // Parameters
  nh_.param<string>("/rddf_file", rddf_file_, "test.txt");
  nh_.param<string>("/routing_mode", routing_mode_, "gps");
  
  std::string ld_param = "/stier_params/lookahead_distance";
  std::string speed_param = "/stier_params/gps_speed";
  std::string speed_test_param = "/stier_params/vision_speed";
  std::string speed_fallback_param = "/stier_params/vision_fallback_speed";
  std::string ld_test_param = "/stier_params/vision_lookahead";
  std::string lidar_speed_param = "/stier_params/lidar_speed";
  std::string lidar_ld_param = "/stier_params/lidar_lookahead";

  nh_.param<double>(ld_param, lookahead_distance_, 8.0);
  nh_.param<double>(speed_param, target_speed_, 15.0);
  nh_.param<double>(speed_test_param, vision_speed_, 5.0);
  nh_.param<double>(speed_fallback_param, vision_fallback_speed_, 3.0);
  nh_.param<double>(ld_test_param, vision_lookahead_, 5.0);
  nh_.param<double>(lidar_speed_param, lidar_speed_, 3.0);
  nh_.param<double>(lidar_ld_param, lidar_lookahead_, 4.0);
  nh_.param<double>("/stier_params/speed_min",           speed_min_,           5.0);
  nh_.param<double>("/stier_params/speed_max",           speed_max_,           6.0);
  nh_.param<double>("/stier_params/speed_steer_max_deg", speed_steer_max_deg_, 20.0);

  // Load Path
  string package_path = package::getPath("stier_bringup"); 
  string full_path = package_path + "/paths/" + rddf_file_;

  if (!path_manager_.loadPath(full_path)) {
    ROS_WARN("Failed to load path from %s. Using default/empty.", full_path.c_str());
  }

  // Subscribers
  sub_utm_         = nh_.subscribe("/utm", 1, &BehaviorPlannerNode::utmCallback, this);
  sub_navpvt_      = nh_.subscribe("/ublox_position_receiver/navpvt", 1, &BehaviorPlannerNode::navpvtCallback, this);
  sub_vision_path_ = nh_.subscribe("/vision/lane_path", 1, &BehaviorPlannerNode::visionPathCallback, this);
  sub_lidar_path_  = nh_.subscribe("/lidar_path", 1, &BehaviorPlannerNode::lidarPathCallback, this);
  sub_feedback_    = nh_.subscribe("/erp42_serial/feedback", 1, &BehaviorPlannerNode::feedbackCallback, this);


  // Publishers
  pub_target_path_ = nh_.advertise<nav_msgs::Path>("/target_path", 1);
  pub_global_path_ = nh_.advertise<nav_msgs::Path>("/global_path", 1, true); // Latched
  pub_path_marker_ = nh_.advertise<visualization_msgs::Marker>("/behavior_planner/path_marker", 1);
  pub_local_gps_path_ = nh_.advertise<nav_msgs::Path>("/local_gps_path", 1);
  pub_current_idx_ = nh_.advertise<std_msgs::Int32>("/current_idx", 1);

  // Timer
  planning_timer_ = nh_.createTimer(ros::Duration(1.0 / 20.0), &BehaviorPlannerNode::planningLoop, this);

  ROS_INFO("BehaviorPlannerNode initialized with rddf: %s", rddf_file_.c_str());
}

void BehaviorPlannerNode::run() { ros::spin(); }

void BehaviorPlannerNode::utmCallback(const geometry_msgs::PoseStamped::ConstPtr &msg) {
  double current_x = msg->pose.position.x;
  double current_y = msg->pose.position.y;

  // 이동 경로 기반 헤딩(Velocity Heading) 계산
  double dx = current_x - last_gps_x_;
  double dy = current_y - last_gps_y_;
  double dist = std::hypot(dx, dy);

  if (dist > 0.5) { // 0.5m 이상 이동했을 때만 헤딩 갱신
    double new_v_heading = std::atan2(dx, dy); // North=0, CW+ (GPS Nav 기준 맞춤: atan2(dx, dy))
    
    if (!velocity_heading_initialized_) {
      velocity_heading_ = new_v_heading;
      velocity_heading_initialized_ = true;
    } else {
      // 강한 필터 적용 (0.1)
      double diff = new_v_heading - velocity_heading_;
      while (diff > M_PI) diff -= 2 * M_PI;
      while (diff < -M_PI) diff += 2 * M_PI;
      velocity_heading_ += 0.1 * diff;
    }
    last_gps_x_ = current_x;
    last_gps_y_ = current_y;
  }

  car_.x = current_x;
  car_.y = current_y;
  has_utm_ = true;
  last_utm_time_ = ros::Time::now();
}

void BehaviorPlannerNode::navpvtCallback(const ublox_msgs::NavPVT::ConstPtr &msg) {
  double heading_deg = msg->heading * 1e-5;
  car_.heading = heading_deg * M_PI / 180.0;
}

void BehaviorPlannerNode::visionPathCallback(const nav_msgs::Path::ConstPtr &msg) {
  vision_path_ = *msg;
  has_vision_path_ = true;
  last_vision_time_ = ros::Time::now();
}

void BehaviorPlannerNode::lidarPathCallback(const nav_msgs::Path::ConstPtr &msg) {
  lidar_path_ = *msg;
  has_lidar_path_ = true;
  last_lidar_time_ = ros::Time::now();
}



void BehaviorPlannerNode::planningLoop(const ros::TimerEvent &event) {
  // 1. Refresh Dynamic Parameters
  nh_.getParam("/routing_mode", routing_mode_);

  std::string ld_param = "/stier_params/lookahead_distance";
  std::string speed_param = "/stier_params/gps_speed";
  std::string speed_test_param = "/stier_params/vision_speed";
  std::string speed_fallback_param = "/stier_params/vision_fallback_speed";
  std::string ld_test_param = "/stier_params/vision_lookahead";
  std::string lidar_speed_param = "/stier_params/lidar_speed";
  std::string lidar_ld_param = "/stier_params/lidar_lookahead";

  nh_.getParam(ld_param, lookahead_distance_);
  nh_.getParam(speed_param, target_speed_);
  nh_.getParam(speed_test_param, vision_speed_);
  nh_.getParam(speed_fallback_param, vision_fallback_speed_);
  nh_.getParam(ld_test_param, vision_lookahead_);
  nh_.getParam(lidar_speed_param, lidar_speed_);
  nh_.getParam(lidar_ld_param, lidar_lookahead_);
  nh_.getParam("/stier_params/speed_min",           speed_min_);
  nh_.getParam("/stier_params/speed_max",           speed_max_);
  nh_.getParam("/stier_params/speed_steer_max_deg", speed_steer_max_deg_);

  // 2. Process Traffic Rules
  traffic_manager_.process();
  DriveMode drive_mode = traffic_manager_.getDriveMode();

  // 3. Find Location on Global Path
  int current_idx = path_manager_.findNearestIndex(car_.x, car_.y);

  // 3.5. Calculate Local GPS Path (only for Lidar/Vision fallback or external apps)
  nav_msgs::Path local_gps_path; // Local frame (stier)
  nav_msgs::Path utm_sub_path;   // Global frame (utm)
  
  local_gps_path.header.stamp = ros::Time::now();
  local_gps_path.header.frame_id = "stier";
  utm_sub_path.header.stamp = ros::Time::now();
  utm_sub_path.header.frame_id = "utm";
  
  bool utm_fresh = has_utm_ && ((ros::Time::now() - last_utm_time_).toSec() < 1.0);

  if (utm_fresh) {
    // 좌표 변환용 ENU Yaw 계산
    double effective_heading = car_.heading;
    if (routing_mode_ != "vision" && velocity_heading_initialized_) {
        effective_heading = velocity_heading_;
    }
    double car_enu_yaw = M_PI / 2.0 - effective_heading;

    double max_search_dist = lookahead_distance_ + 10.0;
    double max_search_dist_sq = max_search_dist * max_search_dist;

    if (current_idx >= 0 && path_manager_.getCount() > 0) {
      for (int i = 0; i < 200; ++i) {
        int idx = current_idx + i;
        if (idx >= (int)path_manager_.getCount()) break;

        Point p = path_manager_.getPoint(idx);
        double dx = p.x - car_.x;
        double dy = p.y - car_.y;
        double d_sq = dx * dx + dy * dy;

        // [1] UTM Sub Path (어긋남 없는 원본 좌표)
        geometry_msgs::PoseStamped utm_pose;
        utm_pose.pose.position.x = p.x;
        utm_pose.pose.position.y = p.y;
        utm_pose.pose.orientation.w = 1.0;
        utm_sub_path.poses.push_back(utm_pose);

        // [2] Local Frame Path (참고용 로컬 변환)
        double lx = dx * std::cos(car_enu_yaw) + dy * std::sin(car_enu_yaw);
        double ly = -dx * std::sin(car_enu_yaw) + dy * std::cos(car_enu_yaw);

        if (lx > -2.0) { // 약간 뒤쪽 점부터 포함
          geometry_msgs::PoseStamped local_pose;
          local_pose.pose.position.x = lx;
          local_pose.pose.position.y = ly;
          local_pose.pose.orientation.w = 1.0;
          local_gps_path.poses.push_back(local_pose);
        }
        if (d_sq > max_search_dist_sq) break;
      }
    }
    
    if (!local_gps_path.poses.empty()) {
      pub_local_gps_path_.publish(local_gps_path);
    }
  } else {
    ROS_WARN_THROTTLE(2.0, "[BehaviorPlanner] GPS Data Stale (has_utm=%d, time_diff=%.2f)", has_utm_, (ros::Time::now() - last_utm_time_).toSec());
  }

  // 4. Determine Active Routing Logic
  nav_msgs::Path target_path;
  target_path.header.stamp = ros::Time::now();

  bool vision_available = (has_vision_path_ && !vision_path_.poses.empty());
  bool vision_fresh     = ((ros::Time::now() - last_vision_time_) < ros::Duration(0.5));
  bool use_vision       = vision_available && vision_fresh;

  bool lidar_available = (has_lidar_path_ && !lidar_path_.poses.empty());
  bool lidar_fresh     = ((ros::Time::now() - last_lidar_time_) < ros::Duration(0.5));
  bool use_lidar       = lidar_available && lidar_fresh;

  double active_speed;
  double active_ld;

  if (routing_mode_ == "lidar") {
    // ── 디버그 전용: lidar 경로만 사용 ──────────────────────────────
    active_ld    = lidar_lookahead_;
    active_speed = steerAdaptiveSpeed(lidar_speed_);
    if (use_lidar) {
      target_path = lidar_path_;
      target_path.header.frame_id = "velodyne";
      nh_.setParam("/routing_mode_active", "lidar");
    } else {
      // 경로 없으면 직진 폴백
      target_path.header.frame_id = "velodyne";
      geometry_msgs::PoseStamped p1, p2;
      p1.pose.position.x = 0; p1.pose.position.y = 0;
      p2.pose.position.x = 5; p2.pose.position.y = 0;
      target_path.poses.push_back(p1);
      target_path.poses.push_back(p2);
      nh_.setParam("/routing_mode_active", "lidar_fallback");
      ROS_WARN_THROTTLE(2.0, "[Lidar Mode] No lidar path - Driving Straight");
    }
  } else if (routing_mode_ == "vision") {
    // ── Vision Only Test 모드 ────────────────────────────────────────
    active_speed = steerAdaptiveSpeed(vision_speed_);
    active_ld    = vision_lookahead_;
    if (use_vision) {
      target_path = vision_path_;
      target_path.header.frame_id = "stier";
      nh_.setParam("/routing_mode_active", "vision");
    } else {
      active_speed = vision_fallback_speed_;
      target_path.header.frame_id = "stier";
      geometry_msgs::PoseStamped p1, p2;
      p1.pose.position.x = 0; p1.pose.position.y = 0;
      p2.pose.position.x = 20; p2.pose.position.y = 0;
      target_path.poses.push_back(p1);
      target_path.poses.push_back(p2);
      nh_.setParam("/routing_mode_active", "straight_fallback");
      ROS_INFO_THROTTLE(2.0, "[Vision Mode] Lane Lost - Driving Straight (Spd: %.1f)", active_speed);
    }
  } else {
    // ── 표준 Hybrid 모드: 우선순위 lidar > 차선(vision) > GPS ────────
    active_ld = lookahead_distance_;

    if (use_lidar) {
      // 1순위: lidar RRT* 회피 경로
      active_speed = steerAdaptiveSpeed(lidar_speed_);
      active_ld    = lidar_lookahead_;
      target_path  = lidar_path_;
      target_path.header.frame_id = "velodyne";
      nh_.setParam("/routing_mode_active", "lidar");
      ROS_INFO_THROTTLE(2.0, "[Hybrid] Using LIDAR avoidance path");
    } else if (use_vision) {
      // 2순위: 차선 인식 경로
      active_speed = steerAdaptiveSpeed(vision_speed_);
      active_ld    = vision_lookahead_;
      target_path  = vision_path_;
      target_path.header.frame_id = "stier";
      nh_.setParam("/routing_mode_active", "vision");
    } else {
      // 3순위: GPS 경로 (UTM 직접 타겟팅을 통한 정렬 최적화)
      active_speed = steerAdaptiveSpeed(target_speed_);
      nh_.setParam("/routing_mode_active", "gps");

      if (!utm_sub_path.poses.empty()) {
        target_path = utm_sub_path;
      } else {
        target_path.header.frame_id = "utm"; // Empty path fallback
      }
    }
  }

  // Common: Status and Publish
  nh_.setParam("/active_target_speed", active_speed);
  nh_.setParam("/active_lookahead", active_ld);

  publishGlobalPath();
  if (!target_path.poses.empty()) {
    pub_target_path_.publish(target_path);

  }

  std_msgs::Int32 idx_msg;
  idx_msg.data = current_idx;
  pub_current_idx_.publish(idx_msg);
}


// ──────────────────────────────────────────────────────────────
// 조향각 기반 1차함수 선형 속도 보간
// speed = speed_max - (speed_max - speed_min) * clamp(|steer| / steer_max, 0, 1)
// base_speed는 각 모드 설정 속도 대비 비율 보정에 사용
// ──────────────────────────────────────────────────────────────
double BehaviorPlannerNode::steerAdaptiveSpeed(double base_speed) const {
  if (speed_steer_max_deg_ <= 0.0) return base_speed;

  // |조향각| / 기준 최대 조향각  (0.0 ~ 1.0으로 정규화 후 클램프)
  double ratio = std::fabs(current_steer_deg_) / speed_steer_max_deg_;
  ratio = std::max(0.0, std::min(1.0, ratio));

  // 1차 선형 보간: 직진→speed_max, 최대 조향→speed_min
  double adaptive = speed_max_ - (speed_max_ - speed_min_) * ratio;

  // base_speed가 speed_max보다 낮은 모드(예: fallback)이면 그대로 반환
  return std::min(adaptive, base_speed);
}

void BehaviorPlannerNode::feedbackCallback(const erp42_msgs::SerialFeedBack::ConstPtr &msg) {
  current_steer_deg_ = std::fabs(static_cast<double>(msg->steer));
}

void BehaviorPlannerNode::publishGlobalPath() {
  if (global_path_published_) return; // 1회 발행 후 중단 (지연 해소 핵심)

  nav_msgs::Path global_path_msg;
  global_path_msg.header.stamp = ros::Time::now();
  global_path_msg.header.frame_id = "utm";
  for (size_t i = 0; i < path_manager_.getCount(); ++i) {
    Point p = path_manager_.getPoint(i);
    geometry_msgs::PoseStamped pose;
    pose.pose.position.x = p.x;
    pose.pose.position.y = p.y;
    pose.pose.orientation.w = 1.0;
    global_path_msg.poses.push_back(pose);
  }
  pub_global_path_.publish(global_path_msg);
  global_path_published_ = true;
  ROS_INFO("[BehaviorPlanner] Global path published once to reduce lag.");
}

} // namespace behavior_planner
