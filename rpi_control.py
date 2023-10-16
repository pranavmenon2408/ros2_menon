import lgpio
from gpiozero import PWMLED
import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import Num
import sys
from time import sleep
from math import fabs
class Rpicontrol(Node):
    def __init__(self,pwm,dir):
        self.pwm=pwm
        self.dir=dir
        self.flag=0
        self.h=lgpio.gpiochip_open(0)
        self.screw1=PWMLED(17)
        self.screw2=PWMLED(24)
        self.screw1.value=0
        self.screw2.value=0
        self.freq=10000
        for i in self.pwm:
            lgpio.gpio_claim_output(self.h, i)
            lgpio.tx_pwm(self.h, i, self.freq, 0)
        for i in self.dir:
            lgpio.gpio_claim_output(self.h, i)
        lgpio.gpio_claim_output(self.h, 18)
        lgpio.gpio_claim_output(self.h, 27)
        lgpio.gpio_claim_output(self.h, 22)
        #lgpio.gpio_claim_output(self.h, 17)
        #lgpio.gpio_claim_output(self.h, 24)
        
        lgpio.gpio_claim_output(self.h, 23)
        
        
        
        super().__init__('rpi_control')
        self.subscriber=self.create_subscription(Num,'vel',self.handle_control,10)
        self.subscriber
    def out(self,vel,i):
        if(abs(vel)>40):
            if(vel<0):
                lgpio.gpio_write(self.h, self.dir[i], 0)
                lgpio.tx_pwm(self.h, self.pwm[i], self.freq, abs((vel*50)//255))
            else:
                lgpio.gpio_write(self.h, self.dir[i], 1)
                lgpio.tx_pwm(self.h, self.pwm[i], self.freq, abs((vel*50)//255))
            

        else:
            lgpio.tx_pwm(self.h, self.pwm[i], self.freq, 0)
            return 0

        return abs((vel*100)//255)


    def handle_control(self,msg):
        
        vel=[msg.front,msg.left,msg.right]
        self.screw_flag=0
        actual_vel=[]
        for i in range(len(vel)):
            actual_vel.append(self.out(vel[i],i))
        
        ''' i,j,k=0,0,0
        while(i<actual_vel[0] and j<actual_vel[1] and k<actual_vel[2]):
            if(i>actual_vel[0]):
                lgpio.tx_pwm(self.h, self.pwm[0], self.freq, actual_vel[0])
            else:
                i+=10
                lgpio.tx_pwm(self.h, self.pwm[0], self.freq, i)
                
            if(j>actual_vel[1]):
                lgpio.tx_pwm(self.h, self.pwm[1], self.freq, actual_vel[1])
            else:
                j+=10
                lgpio.tx_pwm(self.h, self.pwm[1], self.freq, j)
                
            if(k>actual_vel[2]):
                lgpio.tx_pwm(self.h, self.pwm[2], self.freq, actual_vel[2])
            else:
                k+=10
                lgpio.tx_pwm(self.h, self.pwm[2], self.freq, k)'''
                

        if msg.l1==1:
            for i in range(3):
                lgpio.gpio_write(self.h, self.dir[i], 0)
                lgpio.tx_pwm(self.h, self.pwm[i], self.freq, 50)
        if msg.r1==1:
            for i in range(3):
                lgpio.gpio_write(self.h, self.dir[i], 1)
                lgpio.tx_pwm(self.h, self.pwm[i], self.freq, 50)
        if msg.a==1:
            lgpio.gpio_write(self.h, 27, 1)
            lgpio.gpio_write(self.h,22, 1)
            self.screw1.value=0.7
            self.screw2.value=0.7
            self.screw_flag=1
            #lgpio.gpio_write(self.h, 17, 1)
            #lgpio.gpio_write(self.h,24, 1)
        if msg.y==1:
            lgpio.gpio_write(self.h, 27, 0)
            lgpio.gpio_write(self.h,22, 0)
            self.screw1.value=0.7
            self.screw2.value=0.7
            self.screw_flag=1
            #lgpio.gpio_write(self.h, 17, 1)
            #lgpio.gpio_write(self.h,24, 1)
            


        if msg.button==1:
            for i in self.pwm:
                lgpio.tx_pwm(self.h, i, self.freq, 0)
            if self.flag==0:
                self.flag=1
            else:
                self.flag=0
        
        
    
            
                
            

        
        lgpio.gpio_write(self.h, 23, 0)
        #lgpio.gpio_write(self.h, 17, 0)
        #lgpio.gpio_write(self.h,24, 0)
        if self.screw_flag==0:
           self.screw1.value=0
           self.screw2.value=0
           #lgpio.gpio_write(self.h, 17, 0)
           #lgpio.gpio_write(self.h,24, 0)
           
        if self.flag==0:
           lgpio.tx_pwm(self.h, 18, self.freq, 100)
        else:
           lgpio.tx_pwm(self.h, 18, self.freq, 0)
        
            
        self.get_logger().info(f"I heard {msg.front} and {msg.left} and {msg.right} and {msg.l1} and {msg.r1}")
        
        
def main(args=None):
    pwm=[13,19,12]#13,19,12
    dir=[6,26,25]#6,26,25
    
    rclpy.init()
    rpicontrol=Rpicontrol(pwm,dir)
    rclpy.spin(rpicontrol)
    
    rclpy.shutdown()
    lgpio.gpiochip_close(rpicontrol.h)
if __name__=='__main__':
    main()



