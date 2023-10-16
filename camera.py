'''import socket, cv2, pickle,struct

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = "192.168.23.102"#socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	client_socket,addr = server_socket.accept()
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture(0)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = cv2.resize(frame,(400,400))
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			
			#cv2.imshow('TRANSMITTING VIDEO',frame)
			if cv2.waitKey(1) == ord('q'):
				client_socket.close()'''
import socket, cv2, pickle,struct
import rclpy
from rclpy.node import Node

class Camera(Node):
	def __init__(self):
		super().__init__("camera_node")
		
		self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.host_name  = socket.gethostname()
		self.host_ip = "192.168.45.102"#socket.gethostbyname(host_name)
		self.get_logger().info(f"Host Ip {self.host_ip}")#print('HOST IP:',host_ip)
		self.port = 9999
		self.socket_address = (self.host_ip,self.port)

		# Socket Bind
		self.server_socket.bind(self.socket_address)

		# Socket Listen
		self.server_socket.listen(5)
		self.get_logger().info(f"LISTENING AT:{self.socket_address}")

		self.client_socket,addr = self.server_socket.accept()
		self.get_logger().info(f'GOT CONNECTION FROM:{addr}')
		if self.client_socket:
				self.vid = cv2.VideoCapture(0)

		self.timer=self.create_timer(0.01,self.on_timer)

	
	def on_timer(self):

		if(self.vid.isOpened()):
			img,frame = self.vid.read()
			frame = cv2.resize(frame,(320,320))
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			self.client_socket.sendall(message)
			
			#cv2.imshow('TRANSMITTING VIDEO',frame)
			if cv2.waitKey(1) == ord('q'):
				self.client_socket.close()
def main(args=None):
	rclpy.init(args=args)
	cam=Camera()
	rclpy.spin(cam)
	cam.vid.release()
	cv2.destroyAllWindows()
	rclpy.shutdown()

if __name__=='__main__':
	main()


