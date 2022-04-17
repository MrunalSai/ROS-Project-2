# ROS_Project_2

The bot is trapped in a room and the only exit is blocked by an obstacle. The task is to create a package that moves the turtlebot until it reaches a wall, then stop and delete the round obstacle with a service call. Then it has to exit the room.

**Dockerfile build:**

Image can be built using the Dokerfile (**docker build -t imagename:tag .**)

Then fireup the container by creating volume of this repository inside the container (**docker run -it --name <container_name> -v /<absolute_path_to>ROS_Project_2-main:/root/catkin_ws/src/ROS_Project_2-main**)

**Spawning the world:**

Launch the turtlebot3_gazebo package: r**oslaunch turtlebot3_gazebo turtlebot3_empty_world.launch**

Spawn the gazebo model: **roslaunch miniproject_world world.launch**

**Task:**


 We create a launch file named start.launch. 

 Create an action message called Start.action

 Write a subscriber that listens on the \scan topic and detect if you are getting close to a wall

 Write a service caller to delete the round obstacle in the gap with a service call to /gazebo/delete_model as soon as you reach any wall

 Write a wall following algorithm and drive along to exit the room
 
 **NOTE:** The action is used to start the robots drive behavior (start.launch should only start the action server using this action).
 
 We initialize the action server with the name mini_project_action_server.
 
 **Finally we publish the goal into the action topic, which starts the rest of the program: **

 
rostopic pub /mini_project_action_server/goal action/StartActionGoal "header:
seq: 0
stamp:
secs: 0
nsecs: 0
frame_id: ''
goal_id:
stamp:
secs: 0
nsecs: 0
id: ''
goal:
start_driving: true"

The code now reacts on this call and in the end the robot publishes the service call to   gazebo/delete_model and start moving towards/through the gap.


 
 
