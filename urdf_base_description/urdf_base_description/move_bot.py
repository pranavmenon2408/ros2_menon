import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            'camera1/image_raw',
            self.image_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # Process the image here
        cv2.imshow('image', cv_image)
        edge = cv2.Canny(cv_image, 100, 200)
        cv2.imshow('edge', edge)
        self.get_logger().info('Received a server cam image')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

def main(args=None):
    rclpy.init(args=args)
    subscriber = ImageSubscriber()
    rclpy.spin(subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

