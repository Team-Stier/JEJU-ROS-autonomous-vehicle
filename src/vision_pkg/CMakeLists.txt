cmake_minimum_required(VERSION 3.0.2)
project(vision_pkg)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  rospy
  sensor_msgs
  std_msgs
  dynamic_reconfigure
)

generate_dynamic_reconfigure_options(
  cfg/Vision.cfg
)

catkin_package(
  CATKIN_DEPENDS cv_bridge rospy sensor_msgs std_msgs dynamic_reconfigure
)

catkin_install_python(PROGRAMS
  src/main.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
