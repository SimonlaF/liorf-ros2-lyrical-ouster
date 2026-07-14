cmake_minimum_required(VERSION 3.5)
project(liorf)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g -pthread")

include(cmake/rosidl_get_typesupport_target.cmake)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(pcl_msgs REQUIRED)
find_package(jsoncpp CONFIG REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(OpenCV REQUIRED)
find_package(PCL REQUIRED)
find_package(GTSAM REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenMP REQUIRED)
find_package(Boost REQUIRED COMPONENTS timer)
set(ROS2_MESSAGE_TARGETS
  ${std_msgs_TARGETS}
  ${sensor_msgs_TARGETS}
  ${geometry_msgs_TARGETS}
  ${nav_msgs_TARGETS}
  ${visualization_msgs_TARGETS}
  ${pcl_msgs_TARGETS}
)
set(ros2_lib "rclcpp;rclpy;std_msgs;sensor_msgs;geometry_msgs;nav_msgs;cv_bridge;pcl_msgs;pcl_conversions;visualization_msgs;tf2;tf2_ros;tf2_eigen;tf2_sensor_msgs;tf2_geometry_msgs")

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "/usr/share/cmake/geographiclib/")
find_package(GeographicLib REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME} 
  "msg/CloudInfo.msg"
  "srv/SaveMap.srv"
  DEPENDENCIES std_msgs sensor_msgs
)
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)

# include directories
include_directories(
  lib
  include
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${GTSAM_INCLUDE_DIR}
  ${ament_INCLUDE_DIRS}
  ${rclcpp_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
  ${sensor_msgs_INCLUDE_DIRS}
  ${geometry_msgs_INCLUDE_DIRS}
  ${nav_msgs_INCLUDE_DIRS}
  ${tf2_INCLUDE_DIRS}
  ${tf2_ros_INCLUDE_DIRS}
  ${tf2_geometry_msgs_INCLUDE_DIRS}
  ${pcl_conversions_INCLUDE_DIRS}
  ${cloud_msgs_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS} 
  ${GTSAM_INCLUDE_DIR}
  ${Boost_INCLUDE_DIRS}
  ${cv_bridge_INCLUDE_DIRS}
)

# link directories
link_directories(
  lib
  include
  ${PCL_LIBRARY_DIRS}
  ${OpenCV_LIBRARY_DIRS}
  ${GTSAM_LIBRARY_DIRS}
)

file(GLOB common_lib "lib/*.cpp")

###########
## Build ##
###########
# <!-- liorf_yjz_lucky_boy -->
# Range Image Projection
add_executable(
  ${PROJECT_NAME}_imageProjection
  src/imageProjection.cpp
  ${common_lib}
)

target_include_directories(
  ${PROJECT_NAME}_imageProjection
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/lib
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_LOCAL_INCLUDE_DIR}
)
# Modified for Lyrical with the deprecation of ament_target_dependencies
target_link_libraries(
  ${PROJECT_NAME}_imageProjection
  PRIVATE
  "${cpp_typesupport_target}"
  rclcpp::rclcpp
  cv_bridge::cv_bridge
  tf2::tf2
  tf2_ros::tf2_ros
  tf2_eigen::tf2_eigen
  tf2_sensor_msgs::tf2_sensor_msgs
  tf2_geometry_msgs::tf2_geometry_msgs
  pcl_conversions::pcl_conversions
  ${PCL_LIBRARIES}
  ${OpenCV_LIBRARIES}
  ${visualization_msgs_TARGETS}
  Eigen3::Eigen
  ${ROS2_MESSAGE_TARGETS}
)


# Mapping Optimization
add_executable(
  ${PROJECT_NAME}_mapOptmization
  src/mapOptmization.cpp
  ${common_lib}
  include/Scancontext.cpp
)

target_compile_options(
  ${PROJECT_NAME}_mapOptmization
  PRIVATE
  ${OpenMP_CXX_FLAGS}
)

target_include_directories(
  ${PROJECT_NAME}_mapOptmization
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/lib
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${GeographicLib_INCLUDE_DIRS}
  ${EIGEN3_LOCAL_INCLUDE_DIR}
)

target_link_libraries(
  ${PROJECT_NAME}_mapOptmization
  PRIVATE
  Boost::timer
  "${cpp_typesupport_target}"
  rclcpp::rclcpp
  cv_bridge::cv_bridge
  tf2::tf2
  tf2_ros::tf2_ros
  tf2_eigen::tf2_eigen
  tf2_sensor_msgs::tf2_sensor_msgs
  tf2_geometry_msgs::tf2_geometry_msgs
  pcl_conversions::pcl_conversions
  ${visualization_msgs_TARGETS}
  ${PCL_LIBRARIES}
  ${OpenCV_LIBRARIES}
  OpenMP::OpenMP_CXX
  ${GeographicLib_LIBRARIES}
  Eigen3::Eigen
  gtsam
  ${ROS2_MESSAGE_TARGETS}
)


# IMU Preintegration
add_executable(
  ${PROJECT_NAME}_imuPreintegration
  src/imuPreintegration.cpp
  ${common_lib}
)

target_include_directories(
  ${PROJECT_NAME}_imuPreintegration
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_SOURCE_DIR}/lib
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${EIGEN3_LOCAL_INCLUDE_DIR}
)

target_link_libraries(
  ${PROJECT_NAME}_imuPreintegration
  PRIVATE
  Boost::timer
  "${cpp_typesupport_target}"
  rclcpp::rclcpp
  cv_bridge::cv_bridge
  tf2::tf2
  tf2_ros::tf2_ros
  tf2_eigen::tf2_eigen
  tf2_sensor_msgs::tf2_sensor_msgs
  tf2_geometry_msgs::tf2_geometry_msgs
  pcl_conversions::pcl_conversions
  ${PCL_LIBRARIES}
  ${visualization_msgs_TARGETS}
  ${OpenCV_LIBRARIES}
  gtsam
  Eigen3::Eigen
  ${ROS2_MESSAGE_TARGETS}
)
install(
  DIRECTORY launch config rviz
  DESTINATION share/${PROJECT_NAME}/
)

install(
  TARGETS 
	${PROJECT_NAME}_imageProjection
	${PROJECT_NAME}_imuPreintegration
	${PROJECT_NAME}_mapOptmization
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY "include/"
  DESTINATION include
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_include_directories(include)

ament_package()
