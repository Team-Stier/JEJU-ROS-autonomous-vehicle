#ifndef STIER_SYSTEM_PATH_MANAGER_H
#define STIER_SYSTEM_PATH_MANAGER_H

#include <algorithm>
#include <cmath>
#include <iostream>
#include <ros/ros.h>
#include <string>
#include <vector>

namespace behavior_planner {

struct Point {
  double x;
  double y;
};

class PathManager {
public:
  PathManager();
  ~PathManager();

  bool loadPath(const std::string &file_path);
  void clear();

  // Query methods
  size_t getCount() const;
  Point getPoint(size_t idx) const;
  std::string getFilePath() const;

  // Calculation methods
  int findNearestIndex(double x, double y);
  int findLookaheadIndex(double x, double y, double lookahead_distance);

  // Returns heading in radians [-PI, PI] at specific index
  double calculateHeading(size_t idx) const;

  // Returns squared distance from point to path node
  double getDistanceSquared(double x, double y, size_t idx) const;

private:
  std::vector<Point> path_points_;
  std::string file_path_;

  // For optimization
  int last_search_index_;
};

} // namespace behavior_planner

#endif // STIER_SYSTEM_PATH_MANAGER_H
