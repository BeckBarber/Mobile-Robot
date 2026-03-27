from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mobile_robot'

setup(
	name=package_name,
	version='0.0.0',
	packages=find_packages(exclude=['test']),
	data_files=[
		('share/ament_index/resource_index/packages',
			['resource/'+ package_name]),
		('share/' + package_name, ['package.xml']),
		(os.path.join('share', package_name, 'launch'),
			glob('launch/*.launch.py')),
		(os.path.join('share', package_name, 'urdf'),
			glob('urdf/*')),
		(os.path.join('share', package_name, 'worlds'),
			glob('worlds/*')),
	],
	install_requires=['setuptools'],
	zip_safe=True,
	entry_points={
		'console_scripts':[
			'Joystick_teleop = mobile_robot.Joystick_teleop:main',
			'obstacle_warning = mobile_robot.obstacle_warning:main',
		],
	},
)
