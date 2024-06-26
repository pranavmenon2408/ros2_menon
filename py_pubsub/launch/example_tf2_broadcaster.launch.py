from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='py_pubsub',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[{'turtlename':'turtle1'}]
        ),
        DeclareLaunchArgument(
            'target_frame',default_value='turtle1',
            description='Target from name.'
        ),
        Node(
            package='py_pubsub',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[{'turtlename':'turtle2'}]

        ),
        Node(
            package='py_pubsub',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[{'target_frame':LaunchConfiguration('target_frame')}]
        ),
        Node(
            package='py_pubsub',
            executable='turtle_killer',
            name='turtle_killer'
        ),
        
        
    ])