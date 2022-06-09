# camera_eden

Camera package for Eden Robotics.

## Installation

Then clone this repository on you workspace. Make the repository and source the setup.

```console
~ $ cd eden_ws/src
~/eden_ws/src $ git clone https://github.com/AlessandriniAntoine/camera_eden.git
~/eden_ws/src $ cd ..
~/eden_ws $ catkin_make && source devel/setup.zsh
```

## Run

Open a terminal and launch ROS1.

```console
~ $ source /opt/ros/noetic/setup.zsh && roscore 
```

Open an other terminal and source the setup of you workspace and run the package

```console
~ $ cd eden_ws && source devel/setup.zsh
~/eden_ws $ rosrun camera_edens camera_node.py
```

### Node

This package has two node :

- camera_node : to get the video and change the different mode
- follow_node : to track a selected object

## Hardware

- stereo camera

## Software

- Python 3
- Ros1 noetic
- OpenCv 4.2
