execute_process(COMMAND "/home/stier/catkin_ws/build/drivers/gps/ntrip_client-ros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/stier/catkin_ws/build/drivers/gps/ntrip_client-ros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
