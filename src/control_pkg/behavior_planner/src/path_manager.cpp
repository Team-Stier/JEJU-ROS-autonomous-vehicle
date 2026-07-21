#include "behavior_planner/path_manager.h"
#include <fstream>
#include <sstream>

namespace behavior_planner {

PathManager::PathManager() : last_search_index_(0) {}

PathManager::~PathManager() { clear(); }

void PathManager::clear() {
  path_points_.clear();
  last_search_index_ = 0;
}

bool PathManager::loadPath(const std::string &file_path) {
  file_path_ = file_path;
  std::ifstream file(file_path);
  if (!file.is_open()) {
    ROS_ERROR("PathManager: Cannot open file %s", file_path.c_str());
    return false;
  }

  clear();
  std::string line;
  while (std::getline(file, line)) {
    if (line.empty()) continue;
    std::stringstream ss(line);
    double x, y, extra;
    if (ss >> x >> y) {
      path_points_.push_back({x, y});
    }
  }
  file.close();

  ROS_INFO("PathManager: Loaded %zu points from %s", path_points_.size(),
           file_path.c_str());
  return !path_points_.empty();
}

size_t PathManager::getCount() const { return path_points_.size(); }

Point PathManager::getPoint(size_t idx) const {
  if (idx >= path_points_.size()) {
    return {0.0, 0.0};
  }
  return path_points_[idx];
}

std::string PathManager::getFilePath() const { return file_path_; }

int PathManager::findNearestIndex(double x, double y) {
  if (path_points_.empty())
    return -1;

  int nearest_idx = last_search_index_;
  double min_dist_sq = 1e18;

  // If it's the first time or we might be lost, do a full search
  bool full_search = (last_search_index_ == 0);
  
  if (!full_search) {
    // Check distance at last index
    double dx = x - path_points_[last_search_index_].x;
    double dy = y - path_points_[last_search_index_].y;
    double dist_sq = dx * dx + dy * dy;
    if (dist_sq > 100.0 * 100.0) { // If more than 100m away, maybe we jumped
        full_search = true;
    }
  }

  int start_idx, end_idx;
  if (full_search) {
    start_idx = 0;
    end_idx = (int)path_points_.size() - 1;
  } else {
    start_idx = std::max(0, last_search_index_ - 100);
    end_idx = std::min((int)path_points_.size() - 1, last_search_index_ + 200);
  }

  for (int i = start_idx; i <= end_idx; ++i) {
    double dx = x - path_points_[i].x;
    double dy = y - path_points_[i].y;
    double dist_sq = dx * dx + dy * dy;

    if (dist_sq < min_dist_sq) {
      min_dist_sq = dist_sq;
      nearest_idx = i;
    }
  }

  last_search_index_ = nearest_idx;
  return nearest_idx;
}

int PathManager::findLookaheadIndex(double x, double y,
                                    double lookahead_distance) {
  int current_idx = findNearestIndex(x, y);
  if (current_idx < 0)
    return -1;

  double lookahead_sq = lookahead_distance * lookahead_distance;

  // Search forward from current index
  for (size_t i = current_idx; i < path_points_.size(); ++i) {
    double dx = x - path_points_[i].x;
    double dy = y - path_points_[i].y;
    double dist_sq = dx * dx + dy * dy;

    if (dist_sq >= lookahead_sq) {
      return i;
    }
  }

  return path_points_.size() - 1; // Return last point if no point is far enough
}

double PathManager::calculateHeading(size_t idx) const {
  if (path_points_.size() < 2)
    return 0.0;

  // Clamp index
  size_t prev_idx = (idx == 0) ? 0 : idx - 1;
  size_t next_idx =
      (idx >= path_points_.size() - 1) ? path_points_.size() - 1 : idx + 1;

  if (prev_idx == next_idx)
    return 0.0; // Should not happen with size >= 2 check unless logic error

  double dx = path_points_[next_idx].x - path_points_[prev_idx].x;
  double dy = path_points_[next_idx].y - path_points_[prev_idx].y;

  return std::atan2(dy, dx);
}

double PathManager::getDistanceSquared(double x, double y, size_t idx) const {
  if (idx >= path_points_.size())
    return -1.0;
  double dx = x - path_points_[idx].x;
  double dy = y - path_points_[idx].y;
  return dx * dx + dy * dy;
}

} // namespace behavior_planner
