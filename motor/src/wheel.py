import RPi.GPIO as GPIO
from time import sleep
class Wheel:
    def __init__(self,m):
        self.m = m

    def setupp(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.m.in1,GPIO.OUT)
        GPIO.setup(self.m.in2,GPIO.OUT)
        GPIO.setup(self.m.e,GPIO.OUT)

    def begin(self):
        #print("motor start")
        GPIO.output(self.m.in1,GPIO.HIGH)
        GPIO.output(self.m.in2,GPIO.HIGH)
        GPIO.output(self.m.e,GPIO.HIGH)

    def clkwise(self):
        #print("moving forward..");
        GPIO.output(self.m.in1,GPIO.HIGH)
        GPIO.output(self.m.in2,GPIO.LOW)

    def aclkwise(self):
        #print("moving backward..")
        GPIO.output(self.m.in1,GPIO.LOW)
        GPIO.output(self.m.in2,GPIO.HIGH)

    def mstop(self):
        #print("motor stops ...")
        GPIO.output(self.m.e,GPIO.LOW)

    def mresume(self):
	    GPIO.output(self.m.e,GPIO.HIGH)

    def terminate(self):
        GPIO.cleanup()
