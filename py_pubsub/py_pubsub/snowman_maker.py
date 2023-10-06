import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from turtlesim.srv import Spawn
import math
class Snowman(Node):
    def __init__(self):
        super().__init__('snowman')
        self.pub1=self.create_publisher(Twist,'turtle1/cmd_vel',10)
        self.pub2=self.create_publisher(Twist,'turtle2/cmd_vel',10)
        self.sub=self.create_subscription(Pose,'turtle1/pose',self.callback,1)
        self.spawner=self.create_client(Spawn,'spawn')
        self.sub
        self.pose=Pose()
        self.timer=self.create_timer(0.1,self.on_timer)
        self.circledone=False
        self.first_call=False
        self.turtle_spawned=False
        self.current_angle=0.0
        self.time=0.0
        self.theta=round(360*math.pi/180,2)
    def callback(self,msg):
        if not(self.first_call):
            self.pose.x=msg.x
            self.pose.y=msg.y
            self.first_call=True
            
    def on_timer(self):
        self.vel_msg=Twist()
        if not(self.circledone):
            if(self.current_angle<self.theta):
                self.vel_msg.linear.x=1.0
                self.vel_msg.angular.z=1.0
                self.pub1.publish(self.vel_msg)
                self.time+=0.1
                self.current_angle=self.time*1
            else:
                self.vel_msg.linear.x=0.0
                self.vel_msg.angular.z=0.0
                self.pub1.publish(self.vel_msg)
                self.circledone=True
                self.time=0.0
                self.current_angle=0.0
        else:
            if not(self.turtle_spawned):
                request=Spawn.Request()
                request.name='turtle2'
                request.x=self.pose.x
                request.y=self.pose.y
                request.theta=0.0
                self.result=self.spawner.call_async(request)
                self.turtle_spawned=True
            else:
                if(self.current_angle<self.theta):
                    self.vel_msg.linear.x=2.0
                    self.vel_msg.angular.z=-1.0
                    self.pub2.publish(self.vel_msg)
                    self.time+=0.1
                    self.current_angle=self.time*1
                else:
                    self.vel_msg.linear.x=0.0
                    self.vel_msg.angular.z=0.0
                    self.pub2.publish(self.vel_msg)
                    

                

def main():
    rclpy.init()
    snowman=Snowman()
    rclpy.spin(snowman)
    rclpy.shutdown()

if __name__=='__main__':
    main()
