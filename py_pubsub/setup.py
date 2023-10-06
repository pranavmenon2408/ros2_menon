import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pranavmenon',
    maintainer_email='pranav2408dhruv@gmail.com',
    description='Examples of minimal publisher/subscriber using rclpy',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                  'talker=py_pubsub.publisher_member_function:main',
                  'listener=py_pubsub.subscriber_member_function:main',
                  'minimal_param_node=py_pubsub.python_parameters_node:main',
                  'fibonacci_action_server = py_pubsub.fibonacci_action_server:main',
                  'fibonacci_action_client=py_pubsub.fibonacci_action_client:main',
                  'static_turtle_tf2_broadcaster = py_pubsub.static_turtle_tf2_broadcaster:main',
                  'turtle_tf2_broadcaster=py_pubsub.turtle_tf2_broadcaster:main',
                  'turtle_tf2_listener=py_pubsub.turtle_tf2_listener:main',
                  'dynamic_frame_broadcaster=py_pubsub.dynamic_frame_broadcaster:main',
                  'turtle_killer=py_pubsub.turtle_killer:main',
                  'turtle_spawner=py_pubsub.turtle_spawner:main',
                  'snowman=py_pubsub.snowman_maker:main',
        ],
    },
)
