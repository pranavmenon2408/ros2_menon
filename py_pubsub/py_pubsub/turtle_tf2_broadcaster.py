import rclpy
from rclpy.node import Node
import numpy as np
import math
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose
def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q
class TransformPublisher(Node):
    def __init__(self):
        super().__init__('turtle_tf2_publisher')
        self.turtlename=self.declare_parameter('turtlename','turtle').get_parameter_value().string_value
        self.tf_broadcaster=TransformBroadcaster(self)
        self.subscription=self.create_subscription(Pose,f'/{self.turtlename}/pose',self.handle_turtle_pose,1)
        self.subscription
    def handle_turtle_pose(self,msg):
        t=TransformStamped()
        t.header.stamp=self.get_clock().now().to_msg()
        t.header.frame_id='world'
        t.child_frame_id=self.turtlename

        t.transform.translation.x=msg.x
        t.transform.translation.y=msg.y
        t.transform.translation.z=0.0

        q=quaternion_from_euler(0,0,msg.theta)
        t.transform.rotation.x=q[0]
        t.transform.rotation.y=q[1]
        t.transform.rotation.z=q[2]
        t.transform.rotation.w=q[3]

        self.tf_broadcaster.sendTransform(t)
def main():
    rclpy.init()
    transformpub=TransformPublisher()
    try:
        rclpy.spin(transformpub)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
if __name__=='__main__':
    main()

