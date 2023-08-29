from typing import List
from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.context import Context
from rclpy.node import Node
from rclpy.parameter import Parameter

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv=self.create_service(AddTwoInts,'add_two_ints',self.add_two_ints_callback)

    def add_two_ints_callback(self,request,response):
        response.sum=request.a+request.b
        self.get_logger().info(f'Incoming request\na: {request.a} b: {request.b}')
        return response
    
def main():
    rclpy.init()
    minimal_service=MinimalService()
    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__=='__main__':
    
    main()
    
