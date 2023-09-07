import math
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

from tf2_ros import TypeException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from turtlesim.srv import Spawn,Kill
from geometry_msgs.msg import Pose

class TurtleListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_listener')
        self.target_frame=self.declare_parameter('target_frame','turtle1').get_parameter_value().string_value
        self.tf_buffer=Buffer()
        self.tf_listener=TransformListener(self.tf_buffer,self)
        self.spawner=self.create_client(Spawn,'spawn')
        
        self.turtle_spawning_service_ready=False
        self.turtle_spawned=False
        self.publisher=self.create_publisher(Twist,'turtle2/cmd_vel',1)
        
        self.timer=self.create_timer(1.0,self.on_timer)
        
    
    def on_timer(self):
        from_frame_rel=self.target_frame
        to_frame_rel='turtle2'
        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                try:
                    t=self.tf_buffer.lookup_transform(
                        to_frame_rel,from_frame_rel,rclpy.time.Time()
                    
                    )
                    
                except TypeException as ex:
                    self.get_logger().info(f"Could not transform {to_frame_rel} to {from_frame_rel}: {ex}")
                    return
                msg=Twist()
                scale_rotation_rate=1.0
                msg.angular.z=scale_rotation_rate*math.atan2(
                    t.transform.translation.y,
                    t.transform.translation.x
                )
                scale_forward_speed=0.5
                msg.linear.x=scale_forward_speed*math.sqrt(
                    t.transform.translation.x**2+
                    t.transform.translation.y**2
                )
                self.publisher.publish(msg)
                
                

            else:
                if self.result.done():
                    self.get_logger().info(
                        f'Successfully spawned {self.result.result().name}'
                    )
                    self.turtle_spawned=True
                else:
                    self.get_logger().info('Spawn is not finished')
        else:
            if self.spawner.service_is_ready():
                request=Spawn.Request()
                request.name='turtle2'
                request.x=float(4)
                request.y=float(2)
                request.theta=float(0)

                self.result=self.spawner.call_async(request)
                self.turtle_spawning_service_ready=True
            else:
                self.get_logger().info('Service not ready')
    

def main():
    rclpy.init()
    turtle_listener=TurtleListener()
    try:
        rclpy.spin(turtle_listener)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
if __name__=='__main__':
    main()

