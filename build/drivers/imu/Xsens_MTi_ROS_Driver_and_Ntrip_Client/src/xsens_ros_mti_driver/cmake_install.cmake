# Install script for directory: /home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/msg" TYPE FILE FILES "/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/msg/XsStatusWord.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/cmake" TYPE FILE FILES "/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/catkin_generated/installspace/xsens_mti_driver-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/stier/catkin_ws/devel/include/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/stier/catkin_ws/devel/share/roseus/ros/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/stier/catkin_ws/devel/share/common-lisp/ros/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/stier/catkin_ws/devel/share/gennodejs/ros/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/stier/catkin_ws/devel/lib/python3/dist-packages/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/stier/catkin_ws/devel/lib/python3/dist-packages/xsens_mti_driver")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/catkin_generated/installspace/xsens_mti_driver.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/cmake" TYPE FILE FILES "/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/catkin_generated/installspace/xsens_mti_driver-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/cmake" TYPE FILE FILES
    "/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/catkin_generated/installspace/xsens_mti_driverConfig.cmake"
    "/home/stier/catkin_ws/build/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/catkin_generated/installspace/xsens_mti_driverConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver" TYPE FILE FILES "/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver" TYPE EXECUTABLE FILES "/home/stier/catkin_ws/devel/lib/xsens_mti_driver/xsens_mti_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node"
         OLD_RPATH "/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/lib/xspublic/xscontroller:/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/lib/xspublic/xscommon:/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/lib/xspublic/xstypes:/opt/ros/noetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/xsens_mti_driver/xsens_mti_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/xsens_mti_driver" TYPE DIRECTORY FILES "/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/include/" FILES_MATCHING REGEX "/[^/]*\\.h$" REGEX "/\\.svn$" EXCLUDE REGEX "/\\.git$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xsens_mti_driver/launch" TYPE DIRECTORY FILES "/home/stier/catkin_ws/src/drivers/imu/Xsens_MTi_ROS_Driver_and_Ntrip_Client/src/xsens_ros_mti_driver/launch/" REGEX "/\\.git$" EXCLUDE)
endif()

