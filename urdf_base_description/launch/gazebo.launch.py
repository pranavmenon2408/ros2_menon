from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,ExecuteProcess,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution,LaunchConfiguration
from launch.conditions import IfCondition
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('urdf_base_description')

    xacro_file = os.path.join(share_dir, 'urdf', 'urdf_base.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    robot_localization_file_path = os.path.join(share_dir, 'config','ekf.yaml') 
    #launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')

    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'turtlebot3_world.world'
    )
    default_rviz_config_path = os.path.join(share_dir, 'rviz/nav2_config.rviz')
    nav2_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup') 
    nav2_launch_dir = os.path.join(nav2_dir, 'launch') 
    nav2_params_path = os.path.join(share_dir, 'config', 'nav2_params.yaml')
    nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
    static_map_path = os.path.join(share_dir, 'maps', 'turtlebot3_world.yaml')
    behavior_tree_xml_path = os.path.join(nav2_bt_path, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml')
    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    slam = LaunchConfiguration('slam')
    use_namespace = LaunchConfiguration('use_namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    #use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_simulator = LaunchConfiguration('use_simulator')
    
    map_yaml_file = LaunchConfiguration('map')
    autostart = LaunchConfiguration('autostart')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    
    
    remappings = [('/tf', 'tf'),
                ('/tf_static', 'tf_static')]
    declare_namespace_cmd = DeclareLaunchArgument(
    name='namespace',
    default_value='',
    description='Top-level namespace')

    declare_use_namespace_cmd = DeclareLaunchArgument(
        name='use_namespace',
        default_value='False',
        description='Whether to apply a namespace to the navigation stack')
            
    declare_autostart_cmd = DeclareLaunchArgument(
        name='autostart', 
        default_value='true',
        description='Automatically startup the nav2 stack')

    declare_bt_xml_cmd = DeclareLaunchArgument(
        name='default_bt_xml_filename',
        default_value=behavior_tree_xml_path,
        description='Full path to the behavior tree xml file to use')
    
    declare_map_yaml_cmd = DeclareLaunchArgument(
    name='map',
    default_value=static_map_path,
    description='Full path to map file to load')
    
    declare_params_file_cmd = DeclareLaunchArgument(
    name='params_file',
    default_value=nav2_params_path,
    description='Full path to the ROS2 parameters file to use for all launched nodes')
    
    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        name='rviz_config_file',
        default_value=default_rviz_config_path,
        description='Full path to the RVIZ config file to use')

    

    declare_slam_cmd = DeclareLaunchArgument(
        name='slam',
        default_value='False',
        description='Whether to run SLAM')
        
    

    declare_use_rviz_cmd = DeclareLaunchArgument(
        name='use_rviz',
        default_value='True',
        description='Whether to start RVIZ')
    
    
    

    

   
  
    

    declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf}
        ],
        remappings=remappings
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )
    
    gzserver_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            ),
            launch_arguments={'world': world}.items()
        )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # gazebo_server = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzserver.launch.py'
    #         ])
    #     ]),
    #     launch_arguments={
    #         'pause': 'true'
    #     }.items()
    # )

    # gazebo_client = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzclient.launch.py'
    #         ])
    #     ])
    # )
   

    urdf_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'urdf_base',
            '-topic', 'robot_description'
        ],
        output='screen'
    )
    
    # tf_static=Node(
    #         package='tf2_ros',
    #         namespace = 'scan_to_map',
    #         executable='static_transform_publisher',
    #         arguments= ["0", "0", "0", "0", "0", "0", "map", "scan"]
    #     )
    start_robot_localization_cmd = Node(
    package='robot_localization',
    executable='ekf_node',
    name='ekf_filter_node',
    output='screen',
    parameters=[robot_localization_file_path, 
    {'use_sim_time': True}])

    start_rviz_cmd = Node(
    condition=IfCondition(use_rviz),
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
    arguments=['-d', rviz_config_file])    

  #Launch the ROS 2 Navigation Stack
    start_ros2_navigation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
        launch_arguments = {'namespace': namespace,
                            'use_namespace': use_namespace,
                            'slam': slam,
                            'map': map_yaml_file,
                            'params_file': params_file,
                            'default_bt_xml_filename': default_bt_xml_filename,
                            'autostart': autostart}.items())

    return LaunchDescription([
        declare_namespace_cmd,
        declare_use_namespace_cmd,
        declare_autostart_cmd,
        declare_bt_xml_cmd,
        declare_map_yaml_cmd,
        declare_params_file_cmd,
        declare_rviz_config_file_cmd,
        declare_slam_cmd,
        declare_use_rviz_cmd,
        declare_use_sim_time_cmd,
        
        
        robot_state_publisher_node,
        joint_state_publisher_node,
        
        
        gzserver_cmd,
        gzclient_cmd,
        urdf_spawn_node,
        start_robot_localization_cmd,
        # start_ros2_navigation_cmd,
        # start_rviz_cmd
        
       
        
    ])
