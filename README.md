# Mobile-Robot
Mobile 4-wheel robot with joystick control and 360 degree lidar scan, joystick teleop, IMU, camera,  and an obstacle-fiile world.

---

## Package Structure

'''
~/ros2_jazzy/ros2_ws/src/mobile_robot/
├── config
│   └── robot.rviz
├── launch
│   ├── gazebo_world.launch.py
│   └── rviz.launch.py
├── mobile_robot
│   ├── __init__.py
│   ├── Joystick_teleop.py
│   ├── lidar_launch.py
│   └── obstacle_warning.py
├── models
│   └── model.sdf
├── package.xml
├── setup.cfg
├── setup.py
├── test
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── urdf
│   └── mobile_robot.urdf.xacro
└── worlds
    ├── robot_world.sdf

'''

---

## System Requirements

| Requirement | Version |
|-------------|---------|
| Ubuntu      | 24.04   |
| ROS 2       | Jazzy   |
| Gazebo      | Harmonic (gz sim) |
| Python      | 3.12+   |

---

## Installation

### 1 - Install ROS 2 Jazzy

follow the official guide : https://docs.ros.org/en/jazzy/Installation.html

'''bash
source /opt/ros/jazzy/setup.bas
'''
### 2 - Install Gazebo Harmonic + ROS-GZ integration

```bash
sudo apt install \
  ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 \
  ros-jazzy-joy \
  ros-jazzy-teleop-twist-joy
```

### 3 - Build

'''bash
cd ~/ros2_jassy/ros2_ws
colcon build --packages-select mobile_robot --symlink-install
source install/setup.bash
'''

---

## Running the Project

### Terminal 1 - Gazebo Simulation

'''bash
source ~/ros2_jazzy/ros2_ws/install/setup.bash
ros2 launch mobile_robot gazebo_world.launch.py

### Terminal 2 - RViz visualization 

'''bash
source ~/ros2_jazzy/ros2_ws/install/setup.bash
ros2 launch mobile_robot rviz.launch.py
'''

### Terminal 3 - Joystick Teleop

'''bash
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox'
'''

The Joystick Teleop file is not under the work space but actually in /opt/ros/jazzy/share/teleop_twist_joy/ and in order to write the file here you might need to sudo nano. The location is also why it is teleop-launch and not teleop_launch. for the joy_config:='xbox' you can replace the 'xbox' with whatever model of controller you are using.

### Terminal 4 (optional) - Obstacle warning node

'''bash
ros2 run mobile_robot obstacle_warning
'''
Logs a warning whenever any lidar beam detects an obstacle closer than 0.5 m.

### Record a ROS bag (optional)

'''bash
ros2 bag record /scan /cmd_vel /odom -o robot_session
'''

---

## ROS Topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/cmd_vel` | `geometry_msgs/Twist` | ROS → Gazebo |
| `/scan` | `sensor_msgs/LaserScan` | Gazebo → ROS |
| `/odom` | `nav_msgs/Odometry` | Gazebo → ROS |
| `/tf` | `tf2_msgs/TFMessage` | Gazebo → ROS |
| `/joint_states` | `sensor_msgs/JointState` | Gazebo → ROS |
| `/imu` | `sensor_msgs/Imu` | Gazebo → ROS |
| `/camera/image_raw` | `sensor_msgs/Image` | Gazebo → ROS |
| `/clock` | `rosgraph_msgs/Clock` | Gazebo → ROS |


---
## Robot Specifications
| Parameter | Value |
|-----------|-------|
| Chassis (L × W × H) | 0.45 × 0.30 × 0.12 m |
| Wheel radius | 0.06 m |
| Wheel width | 0.03 m |
| Wheel separation | 0.48 m |
| Drive type | Differential (4-wheel, single DiffDrive plugin) |
| Total mass | ~6 kg |

### Wheel positions (relative to chassis center)

| Wheel | X | Y | Z |
|-------|---|---|---|
| Front Left | +0.12 m | +0.165 m | −0.06 m |
| Front Right | +0.12 m | −0.165 m | −0.06 m |
| Rear Left | −0.12 m | +0.165 m | −0.06 m |
| Rear Right | −0.12 m | −0.165 m | −0.06 m |


---

## Lidar Specifications

| Parameter | Value |
|-----------|-------|
| Type | gpu_lidar (2D) |
| Min range | 0.3 m |
| Max range | **12.0 m** |
| Scan angle | −π to +π **(360° full circle)** |
| Samples | 360 |
| Update rate | 10 Hz |
| ROS topic | `/scan` |
| Frame | `lidar_frame` |


---
## World / Map

The world file (`robot_world.sdf`) contains:
- 10 × 10 m arena with solid boundary walls
- 4 interior maze walls creating corridors
- 4 box obstacles (various sizes/colours)
- 2 cylinder obstacles

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Gazebo can't find world file | Check `worlds/` is in `setup.py` data_files; rebuild |
| Robot doesn't appear | Increase TimerAction delay; check xacro compiles with `xacro urdf/mobile_robot.urdf.xacro` |
| Robot doesn't move | Confirm DiffDrive plugin is in xacro; check `/cmd_vel` bridge direction is `]` |
| No lidar in RViz | Add LaserScan display, topic `/scan`; check bridge has `[gz.msgs.LaserScan` |
| Wheel TF errors in RViz | Confirm JointStatePublisher plugin is in xacro and `/joint_states` is bridged |
| Bridge type errors | Check for typos in message type names in launch file bridge arguments |

---
