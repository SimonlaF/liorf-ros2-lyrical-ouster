import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    share_dir = get_package_share_directory('liorf')

    parameter_file = LaunchConfiguration('params_file')

    rviz_config_file = os.path.join(
        share_dir,
        'rviz',
        'mapping.rviz'
    )

    params_declare = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            share_dir,
            'config',
            'lio_sam_ouster.yaml'
        ),
        description='Path to the ROS 2 parameters file to use.'
    )

    static_map_to_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='map_to_odom_static_tf',
        arguments=[
            '--frame-id', 'map',
            '--child-frame-id', 'odom'
        ],
        output='screen'
    )

    imu_preintegration = Node(
        package='liorf',
        executable='liorf_imuPreintegration',
        name='liorf_imuPreintegration',
        parameters=[parameter_file],
        output='screen'
    )

    image_projection = Node(
        package='liorf',
        executable='liorf_imageProjection',
        name='liorf_imageProjection',
        parameters=[parameter_file],
        output='screen'
    )

    map_optimization = Node(
        package='liorf',
        executable='liorf_mapOptmization',
        name='liorf_mapOptmization',
        parameters=[parameter_file],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        params_declare,
        static_map_to_odom,
        imu_preintegration,
        image_projection,
        map_optimization,
        rviz
    ])