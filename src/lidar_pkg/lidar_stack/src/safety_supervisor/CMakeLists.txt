cmake_minimum_required(VERSION 3.0.2)
project(safety_supervisor)

find_package(catkin REQUIRED COMPONENTS
  dynamic_reconfigure
  geometry_msgs
  lidar_interfaces
  nav_msgs
  rospy
  std_msgs
  visualization_msgs
)

generate_dynamic_reconfigure_options(
  cfg/PredictedPathParameters.cfg
  cfg/SafetySupervisorParameters.cfg
)

catkin_package(
  CATKIN_DEPENDS
    dynamic_reconfigure
    geometry_msgs
    lidar_interfaces
    nav_msgs
    rospy
    std_msgs
    visualization_msgs
)

catkin_install_python(PROGRAMS
  src/path_forecaster.py
  src/predicted_path_visualizer.py
  src/safety_supervisor_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(FILES
  launch/safety_supervisor_bringup.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
