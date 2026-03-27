import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

	pkg = get_package_share_directory("mobile_robot")
	rviz_config = os.path.join(pkg, "config", "robot.rviz")

	use_sim_time_arg = DeclareLaunchArgument(
		"use_sim_time", default_value="true"
	)

	use_sim_time = LaunchConfiguration("use_sim_time")

	rviz_node = Node(
		package="rviz2",
		executable="rviz2",
		name="rviz2",
		output="screen",
		arguments=["-d", rviz_config],
		parameters=[{"use_sim_time": use_sim_time}],
	)

	return LaunchDescription([use_sim_time_arg, rviz_node])
