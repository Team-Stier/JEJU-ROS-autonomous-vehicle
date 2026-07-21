# Install script for directory: /home/stier/catkin_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/stier/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE PROGRAM FILES "/home/stier/catkin_ws/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE PROGRAM FILES "/home/stier/catkin_ws/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/setup.bash;/home/stier/catkin_ws/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE FILE FILES
    "/home/stier/catkin_ws/build/catkin_generated/installspace/setup.bash"
    "/home/stier/catkin_ws/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/setup.sh;/home/stier/catkin_ws/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE FILE FILES
    "/home/stier/catkin_ws/build/catkin_generated/installspace/setup.sh"
    "/home/stier/catkin_ws/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/setup.zsh;/home/stier/catkin_ws/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE FILE FILES
    "/home/stier/catkin_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/stier/catkin_ws/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/setup.fish;/home/stier/catkin_ws/install/local_setup.fish")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE FILE FILES
    "/home/stier/catkin_ws/build/catkin_generated/installspace/setup.fish"
    "/home/stier/catkin_ws/build/catkin_generated/installspace/local_setup.fish"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/stier/catkin_ws/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/stier/catkin_ws/install" TYPE FILE FILES "/home/stier/catkin_ws/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/stier/catkin_ws/build/gtest/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/gps_bringup/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/lidar_pkg/lidar_stack/src/lidar_stack_bringup/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/lidar_pkg/lidar_stack/src/lidar_interfaces/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/erp42_msgs/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/control_pkg/stier_bringup/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox/ublox/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne_msgs/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/cam/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/control_pkg/rddf_recorder/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/lidar_pkg/lidar_stack/src/rrt_path/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/lidar_pkg/lidar_stack/src/safety_supervisor/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/ntrip/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ntrip_client-ros/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/rplidar_ros/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/lidar_pkg/lidar_stack/src/object_detector/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox/ublox_serialization/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox/ublox_msgs/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/control_pkg/pure_pursuit/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/control_pkg/behavior_planner/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox/ublox_gps/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox/ublox_msg_filters/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ublox_utils/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/gps/ROS-UTM-LLA/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne_driver/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne_laserscan/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne_pcl/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/lidar/velodyne/velodyne_pointcloud/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/vision_pkg/cmake_install.cmake")
  include("/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/stier/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
