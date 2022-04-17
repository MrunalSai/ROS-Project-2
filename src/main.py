#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest                  
import sys
import actionlib
from mb_213284_miniprj.msg import startAction, startGoal, startFeedback, startResult


class skillcheck():

	def __init__(self):
	
		self.fl = [] 
		self.fr = []
		self.mid=[]
		self.theta = 0
		self.move = Twist()
		self.scan = LaserScan()
		self.position=Odometry()
		self.sub1=rospy.Subscriber('scan',LaserScan,self.laser_callback)
		self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
		self.sub2=rospy.Subscriber('odom',Odometry,self.odom_callback)
		self.action_server = actionlib.SimpleActionServer('mini_project_action_server', startAction, self.action_callback, auto_start=False)
		self.action_server.start()
		self.success = True
		self.result = startResult()
		
	def action_callback(self,goal):
		self.start = goal.start_driving
		if self.start == True:
			if self.action_server.is_preempt_requested():
				rospy.loginfo("Goal has cancelled")
				self.action_server.set_preempted()
				success = False				
			self.main()			
			if self.success:
				self.result.final_state = "exited the maze"
				self.action_server.set_succeeded(self.result)
	
	
	def laser_callback(self,scan):
		
		self.fl = scan.ranges[0:35]                        #stores front left laser readings
		self.fr = scan.ranges[324:359]                     #stores front right laser readings
		self.mid = scan.ranges	                            #stores complete laser reading list
		return scan
	
	def odom_callback(self,position):
		
		self.x = position.pose.pose.position.x
		self.y = position.pose.pose.position.y
		self.quaternion_orient = position.pose.pose.orientation
		[self.roll , self.pitch , self.theta]= euler_from_quaternion([self.quaternion_orient.x, self.quaternion_orient.y, self.quaternion_orient.z, self.quaternion_orient.w])
		return position
			
	def service_client(self):
		rospy.wait_for_service('/gazebo/delete_model')                                  
		delete_model_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel) 
		kk = DeleteModelRequest()                                                       
		kk.model_name = "obstacle"                                                   
		result = delete_model_service(kk)                                              
		print (result)
		
	def move_forward(self):
		while min(self.fl) >= 1 or min(self.fr) >= 1:
				self.move.linear.x = 0.1
				self.pub.publish(self.move)
				self.rate.sleep()
		self.move.linear.x = 0
		self.pub.publish(self.move)
		
	def rotate_right(self):
			while abs(-1.57 - self.theta) > 0.1:
				print('rotating to the right')
				self.move.angular.z = 0.1
				self.pub.publish(self.move)
				print(self.theta)
				self.rate.sleep()
				
			self.move.angular.z = 0
			self.pub.publish(self.move)
			
	def rotate_left(self):
			while abs(self.theta) >= 0.1 or self.theta <= -1.58:
				print('rotating')
				self.move.angular.z = 0.1
				self.pub.publish(self.move)
				print(self.theta)
				self.rate.sleep()
				
			self.move.angular.z = 0
			self.move.linear.x = 0
			self.pub.publish(self.move)
				
	def main(self):	
	
			self.rate = rospy.Rate(1)
			print(self.fl,self.fr)				
			
			self.move_forward() # To move forward
				
			self.service_client()							
				
			self.rotate_right()  #To rotate the bot to the right side								
			
			self.move_forward()  #To move along the wall, till it reaches other wall
							
			self.rotate_left()  #To rotate the bot to the left
						
			# To move the bot until the laser readings are inf on the wall side
						
			while min(self.mid[235:305]) != float('inf') : 
				print('moving along the wall')
				self.move.linear.x = 0.1
				self.pub.publish(self.move)
				self.rate.sleep()			
			
			self.move.linear.x =0
			self.pub.publish(self.move)
			print(self.move.linear.x)
						
			self.rotate_right()  #To rotate right			
			print('rotated right')
			i = 0
			while i<15:			
				self.move.linear.x = 0.1      # To move forward
				self.pub.publish(self.move)	
				print(self.mid)
				i+=1		
				self.rate.sleep()
			self.move.linear.x = 0
			self.pub.publish(self.move)		


if __name__=='__main__':
    
	try:
		rospy.init_node('miniprj')
		me = skillcheck()
		me.action_callback()
		rospy.spin()
	except rospy.ROSInterruptException:
        	pass

