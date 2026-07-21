#include "behavior_planner/behavior_planner_node.h"

int main(int argc, char **argv) {
  ros::init(argc, argv, "behavior_planner_node");
  behavior_planner::BehaviorPlannerNode node;
  node.run();
  return 0;
}
