import os
from glob import glob
from setuptools import setup
from setuptools import find_packages, setup

package_name = 'server_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.[urdf][xacro]*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.[world]*')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.[dae][stl][png]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pranavmenon',
    maintainer_email='pranav2408dhruv@gmail.com',
    description='Package for Server Bot',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
