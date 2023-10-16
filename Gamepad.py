#!/usr/bin/pyhton3
import sys
import math
import rclpy
import lgpio
from rclpy.node import Node
from tutorial_interfaces.msg import Num
from robopy.rpi_control import Rpicontrol
import pygame

class Gamepad(Node):
    def __init__(self):
        super().__init__('Gamepad')
        self.publisher=self.create_publisher(Num,'vel',10)
        self.timer=self.create_timer(1.0,self.on_timer)
    def map(self,v, in_min, in_max, out_min, out_max):
        if v < in_min:
            v = in_min
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min 
    def omni(self,x,y,minSpeed,maxSpeed):
        r=math.sqrt(math.pow(x,2)+math.pow(y,2))
        theta=math.atan2(y,x)*180.0/math.pi
        if theta>90:
            theta=450-theta
        else:
            theta=90-theta
        theta=(theta*math.pi)/180.0
        wheel_angles=[(90*math.pi)/180.0,(210*math.pi)/180.0,(330*math.pi)/180.0]
        wheel_velocity=[]
        for i in wheel_angles:
            wv=r*math.sin(theta)*math.sin(i)+r*math.cos(theta)*math.cos(i)
            wv=int(self.map(wv,-1,1,minSpeed,maxSpeed))
            wheel_velocity.append(wv)
        return wheel_velocity
    def on_timer(self):
        pygame.init()
        axis_data = None
        button_data = None
        hat_data = None
        j = pygame.joystick
        j.init()
        control=j.Joystick(0)
        control.init()
        while True:
            if not axis_data:
                axis_data = {}
            if not button_data:
                button_data = {}
                for i in range(control.get_numbuttons()):
                    button_data[i] = False
            for event in pygame.event.get():
            #start=time.time()
                if event.type == pygame.JOYAXISMOTION:
                    axis_data[event.axis] = round(event.value,2)
                if event.type == pygame.JOYBUTTONDOWN:
                    button_data[event.button] = True
                if event.type == pygame.JOYBUTTONUP:
                    button_data[event.button] = False
                
                if(0 in axis_data.keys() and 1 in axis_data.keys()):
                    omni_vel=self.omni(axis_data[0],axis_data[1],-255,255)
                    msg=Num()
                    msg.front=omni_vel[0]
                    msg.left=omni_vel[1]
                    msg.right=omni_vel[2]
                    msg.button=button_data[0]
                    msg.l1=button_data[4]
                    msg.r1=button_data[5]
                    msg.a=button_data[1]
                    msg.y=button_data[2]
                    self.publisher.publish(msg)
                '''if(button_data[0]==1):
                    
                    
                    sys.exit(0)'''
def main(args=None):
    rclpy.init()
    pad=Gamepad()
    rclpy.spin(pad)
    rclpy.shutdown()
if __name__=="__main__":
    main()
