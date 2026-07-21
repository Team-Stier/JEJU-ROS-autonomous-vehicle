cmake_minimum_required(VERSION 3.0.2)
project(rrt_path)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  lidar_interfaces
  nav_msgs
  rospy
)

catkin_package(
  CATKIN_DEPENDS
    geometry_msgs
    lidar_interfaces
    nav_msgs
    rospy
)

catkin_install_python(PROGRAMS
  src/rrt_dynamic_goal.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
