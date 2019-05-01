cmake_minimum_required(VERSION 2.8.3)
project(solo_control)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    std_msgs
    mavros_msgs
    geometry_msgs
    nav_msgs
)

catkin_package(
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(solo_control_node
	main.cpp 
) 

target_link_libraries(solo_control_node ${catkin_LIBRARIES})
