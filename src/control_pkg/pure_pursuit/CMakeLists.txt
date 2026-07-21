cmake_minimum_required(VERSION 3.0.2)
project(pure_pursuit)

add_compile_options(-std=c++14)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  nav_msgs
  erp42_msgs
  ublox_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES pure_pursuit_lib
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs nav_msgs erp42_msgs ublox_msgs
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_library(pure_pursuit_lib
  src/pure_pursuit.cpp
  src/pure_pursuit_node.cpp
)
add_dependencies(pure_pursuit_lib ${catkin_EXPORTED_TARGETS})
target_link_libraries(pure_pursuit_lib ${catkin_LIBRARIES})

add_executable(pure_pursuit_node src/main.cpp)
add_dependencies(pure_pursuit_node ${catkin_EXPORTED_TARGETS})
target_link_libraries(pure_pursuit_node pure_pursuit_lib ${catkin_LIBRARIES})

catkin_install_python(PROGRAMS
  scripts/steer_filter.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
