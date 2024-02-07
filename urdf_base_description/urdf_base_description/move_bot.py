from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

class Movement(Node):
    def __init__(self):
        super().__init__('testing_ekf_node')
        self.pub=self.create_publisher(Twist,'/cmd_vel',10)
        self.timer=self.create_timer(0.1,self.timer_callback)
    def timer_callback(self):
        msg=Twist()
        msg.angular.z=-2.0
        #msg.linear.x=0.5
        self.pub.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    move=Movement()
    rclpy.spin(move)
    move.destroy_node()
    rclpy.shutdown()
if __name__=="__main__":
    main()