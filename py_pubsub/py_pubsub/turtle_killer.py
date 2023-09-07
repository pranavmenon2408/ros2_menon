import rclpy
from rclpy.node import Node
import random
from turtlesim.srv import Kill,Spawn
from turtlesim.msg import Pose
class Turtlekiller(Node):
    def __init__(self):
        super().__init__('turtle_killer')
        
        self.listener=self.create_subscription(Pose,'turtle1/pose',self.handle_turtle_pose,1)
        self.turtle1=Pose()
        self.listener2=self.create_subscription(Pose,'turtle2/pose',self.handle_turtle2_pose,1)
        self.killer=self.create_client(Kill,'kill')
        self.spawner=self.create_client(Spawn,'spawn')
        self.turtle_killed=False
        self.listener
        self.listener2
    def handle_turtle_pose(self,msg):
        self.turtle1=msg
        self.turtle1.x=round(msg.x,2)
        self.turtle1.y=round(msg.y,2)
        
    def handle_turtle2_pose(self,msg):
        
        if not(self.turtle_killed):

         if(round(abs(msg.x-self.turtle1.x),2)<=0.50 and round(abs(msg.y-self.turtle1.y),2)<=0.50):
            request=Kill.Request()
            request.name='turtle1'
            self.killturtle=self.killer.call_async(request)
            self.turtle_killed=True
        else:
            request=Spawn.Request()
            request.name='turtle1'
            request.x=float(random.randint(0,10))
            request.y=float(random.randint(0,10))
            request.theta=float(0)

            self.result=self.spawner.call_async(request)
            self.turtle_killed=False

def main(args=None):
    rclpy.init()
    turtlekiller=Turtlekiller()
    rclpy.spin(turtlekiller)
    rclpy.shutdown()
if __name__=="__main__":
    main()

        