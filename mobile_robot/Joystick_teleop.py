import rclpy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def joy_callback(msg,publisher):
	twist_msg = Twist()
	twist_msg.linear.x = 2.0 * msg.axes[1]
	twist_msg.angular.z = 2.0 * msg.axes[0]

	publisher.publish(twist_msg)

def main():
	rclpy.init()

	node=rclpy.create_node('joy_controller')
	subscription=node.create_subscription(Joy, '/joy', lambda msg: joy_callback(msg, publisher), 10)
	publisher = node.create_publisher(Twist, '/cmd_vel', 10)

	rclpy.spin(node)

	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
