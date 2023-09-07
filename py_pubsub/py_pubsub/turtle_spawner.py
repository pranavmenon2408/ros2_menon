from typing import List
import rclpy
import math
import numpy as np
from rclpy.context import Context
from rclpy.node import Node
from rclpy.parameter import Parameter
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from turtlesim.srv import Spawn

class Turtlespawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        self.spawner=self.create_client(Spawn,'spawn')
        
        self.listener=self.create_subscription(Pose,'turtle1/pose',self.handle_turtle_pose,1)
        self.turtle1=Pose()
        
        
        self.listener2=self.create_subscription(Pose,'turtle2/pose',self.handle_turtle2_pose,1)
        self.turtle2=Pose()
        self.publisher=self.create_publisher(Twist,'turtle2/cmd_vel',1)
        self.timer=self.create_timer(1.0,self.on_timer)
        self.turtle_spawning_service_ready=False
        self.reached_goal=False
        self.listener
        self.listener2
    def handle_turtle_pose(self,msg):
        self.turtle1=msg
        
        if not(self.turtle_spawning_service_ready):
            request=Spawn.Request()
            request.name='turtle2'
            request.x=4.00
            request.y=2.00
            request.theta=0.00

            self.result=self.spawner.call_async(request)
            self.turtle_spawning_service_ready=True
        
    def handle_turtle2_pose(self,msg):
        
        self.turtle2=msg
        
        
        
    def on_timer(self):
        if self.turtle_spawning_service_ready:
            
                    
            
            msg=Twist()
            scale_rotation_rate=1.0
            steering_angle=math.atan2(
                self.turtle1.y-self.turtle2.y,
                self.turtle1.x-self.turtle2.y
            )
            heading=steering_angle-self.turtle1.theta
            if(heading>round(math.pi,2)):
                heading=heading-2*round(math.pi,2)
            if(heading<-round(math.pi,2)):
                heading=heading+2*round(math.pi,2)

            msg.angular.z=scale_rotation_rate*(heading)
            
            
            scale_forward_speed=0.5
            msg.linear.x=scale_forward_speed*math.sqrt(
                (self.turtle1.x-self.turtle2.x)**2+
                (self.turtle1.y-self.turtle2.y)**2
            )
            
            self.publisher.publish(msg)
                
                
                
                
                

            
        else:
            self.get_logger().info('Service not ready')
def main(args=None):
    rclpy.init()
    turtlespawner=Turtlespawner()
    rclpy.spin(turtlespawner)
    rclpy.shutdown()
if __name__=="__main__":
    main()
