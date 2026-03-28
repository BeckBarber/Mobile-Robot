import os
import tempfile
import subprocess
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import(
	DeclareLaunchArgument,
	ExecuteProcess,
	TimerAction,
)
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():

	pkg = get_package_share_directory("mobile_robot")

	xacro_file = os.path.join(pkg, "urdf", "mobile_robot.urdf.xacro")
	urdf_file = os.path.join(tempfile.gettempdir(), "mobile_robot.urdf")
	subprocess.run(["xacro", xacro_file, "-o", urdf_file])

	robot_state_publisher = Node(
		package="robot_state_publisher",
		executable="robot_state_publisher",
		parameters=[{
			"robot_description": open(urdf_file).read(),
			"use_sim_time": True,
		}],
	)

	world_file = os.path.join(pkg, "worlds", "robot_world.sdf")
	gazebo = ExecuteProcess(
		cmd=["gz", "sim", "-r", world_file],
		output="screen",
	)

	spawn_robot = Node(
		package="ros_gz_sim",
		executable="create",
		name="spawn_robot",
		output="screen",
		arguments=[
			"-name", "mobile_robot",
			"-file", urdf_file,
			"-x", "-3.5",
			"-y", "-4.0",
			"-z", "0.15",
		],
	)

	bridge = Node(
		package="ros_gz_bridge",
		executable="parameter_bridge",
		name="ros_gz_bridge",
		output="screen",
		parameters=[{"use_sim_time": True}],
		arguments=[
			"/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
			"/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
			"/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
			"/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
			"/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
			"/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
			"/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
			"/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
			"/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
		]
	)

	return LaunchDescription([
		robot_state_publisher,
		gazebo,
		TimerAction(period=8.0, actions=[spawn_robot]),
		TimerAction(period=8.0, actions=[bridge]),
	])
