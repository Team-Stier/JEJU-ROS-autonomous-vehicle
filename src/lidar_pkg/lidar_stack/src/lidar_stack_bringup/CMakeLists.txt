cmake_minimum_required(VERSION 3.0.2)
project(lidar_stack_bringup)

find_package(catkin REQUIRED)

catkin_package()

install(FILES
  launch/lidar_stack_bringup.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
