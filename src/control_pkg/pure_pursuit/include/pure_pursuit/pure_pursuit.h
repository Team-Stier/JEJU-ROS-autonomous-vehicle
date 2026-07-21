#ifndef STIER_SYSTEM_PURE_PURSUIT_H
#define STIER_SYSTEM_PURE_PURSUIT_H

#include <algorithm>
#include <cmath>

namespace pure_pursuit {

struct VehicleConfig {
  double wheelbase;
  double max_steer_deg;
};

class PurePursuit {
public:
  PurePursuit();

  void setConfiguration(const VehicleConfig &config);

  // Original pp.cpp calculate_steer_using_pure_pursuit
  // Returns steering angle in DEGREES
  double calculateSteer(double current_x, double current_y,
                        double current_heading, double target_x,
                        double target_y);

private:
  VehicleConfig config_;
};

} // namespace pure_pursuit

#endif // STIER_SYSTEM_PURE_PURSUIT_H
