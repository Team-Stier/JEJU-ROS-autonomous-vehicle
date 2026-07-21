cmake_minimum_required(VERSION 3.0.2)
project(behavior_planner)

add_compile_options(-std=c++14)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  nav_msgs
  ublox_msgs
  erp42_msgs
  pure_pursuit
  roslib
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES behavior_planner_lib
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs nav_msgs ublox_msgs erp42_msgs pure_pursuit roslib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_library(behavior_planner_lib
  src/path_manager.cpp
  src/traffic_manager.cpp
  src/behavior_planner_node.cpp
)
target_link_libraries(behavior_planner_lib ${catkin_LIBRARIES})

add_executable(behavior_planner_node src/main.cpp)
target_link_libraries(behavior_planner_node behavior_planner_lib ${catkin_LIBRARIES})
