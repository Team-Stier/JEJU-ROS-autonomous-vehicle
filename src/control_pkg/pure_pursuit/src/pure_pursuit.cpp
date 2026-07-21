#include "pure_pursuit/pure_pursuit.h"

namespace pure_pursuit {

PurePursuit::PurePursuit() {
  // Default configuration (from pp.cpp)
  config_.wheelbase = 0.73;
  config_.max_steer_deg = 25.0;
}

void PurePursuit::setConfiguration(const VehicleConfig &config) {
  config_ = config;
}

double PurePursuit::calculateSteer(double current_x, double current_y,
                                   double current_heading, double target_x,
                                   double target_y) {

  // Distance to target
  double dx = target_x - current_x;
  double dy = target_y - current_y;
  double lookahead_dist = std::sqrt(dx * dx + dy * dy);

  // Angle to target 
  // Reverting to Original Coordinate Math (North = 0, CW+)
  double alpha = std::atan2(dx, dy);
  // Wait, typical atan2 is (y, x). Standard frame: x=East?
  // The original code: float alpha = ((float(atan2(dx,dy))));
  // This is angle from Y-axis (North?)

  // Let's preserve original math exactly to ensure identical behavior

  // Current Heading seems to be also 0 at North? or East?
  // pp.cpp main: cog = msg->heading... -> car.heading = cog (radians)
  // ublox navpvt heading is degrees. 0 is North.
  // So current_heading is radians from North, CW. (Standard Nav)

  // Logic:
  double temp_alpha = alpha - current_heading;

  // Standard normalization to [-PI, PI]
  while (temp_alpha > M_PI) temp_alpha -= 2.0 * M_PI;
  while (temp_alpha < -M_PI) temp_alpha += 2.0 * M_PI;

  // Steering Calc
  double steering_rad = std::atan2(
      2.0 * config_.wheelbase * std::sin(temp_alpha) / lookahead_dist, 1.0);

  double steering_deg = steering_rad * 180.0 / M_PI;

  // Clamp (without any sign inversion, perfectly matching pp.cpp)
  steering_deg = std::max(-config_.max_steer_deg,
                          std::min(config_.max_steer_deg, steering_deg));

  return steering_deg;
}

} // namespace pure_pursuit
