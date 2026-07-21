#include "pure_pursuit/pure_pursuit_node.h"

int main(int argc, char **argv) {
  ros::init(argc, argv, "pure_pursuit_node");
  pure_pursuit::PurePursuitNode node;
  node.run();
  return 0;
}
