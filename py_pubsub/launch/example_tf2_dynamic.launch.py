import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    demo_nodes=IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('py_pubsub'),'launch'),
            '/example_tf2_broadcaster.launch.py']),
            launch_arguments={'target_frame':'carrot1'}.items(),
        )
    return LaunchDescription([
        demo_nodes,
        Node(
            package='py_pubsub',
            executable='dynamic_frame_broadcaster',
            name='dynamic_broadcaster',
        ),
    ])
    
