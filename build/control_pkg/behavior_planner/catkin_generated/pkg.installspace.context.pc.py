# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;std_msgs;geometry_msgs;nav_msgs;ublox_msgs;erp42_msgs;pure_pursuit;roslib".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lbehavior_planner_lib".split(';') if "-lbehavior_planner_lib" != "" else []
PROJECT_NAME = "behavior_planner"
PROJECT_SPACE_DIR = "/home/stier/catkin_ws/install"
PROJECT_VERSION = "0.0.0"
