import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

WARN_DISTANCE = 0.5

class ObstacleWarning(Node):
	def __init__(self):
		super().__init__("obstacle_warning")

		self.declare_parameter("warn_distance", WARN_DISTANCE)
		self.warn_dist = self.get_parameter("warn_distance").value

		self.sub = self.create_subscription(
			LaserScan, "/scan", self.scan_callback, 10
		)

		self.get_logger().info(
			f"ObstacleWarning: will warn when obstacle < {self.warn_dist: .2f} m"
		)

	def scan_callback(self, msg: LaserScan):
		valid = [r for r in msg.ranges if msg.range_min <r < msg.range_max]
		if not valid:
			return

		min_dist = min(valid)

		if min_dist < self.warn_dist:
			self.get_logger().warning(
				f" Obstacle Detected at {min_dist:.3f} m (threshold={self.warn_dist:.2f} m)",
				throttle_duration_sec=0.5,
			)
		else:
			self.get_logger().info(
				f" Clear - nearest obstacle: {min_dist:.3f} m",
				throttle_duration_sec=2.0,
			)

def main():
	rclpy.init()
	node = ObstacleWarning()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	finally:
		node.destroy_node()
		rclpy.shutdown()
if __name__ == "__main__":
	main()

