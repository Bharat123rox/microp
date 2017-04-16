import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
motor1_in1 = 11
motor1_in2 = 13
motor1_e = 15
motor2_in1 = 16
motor2_in2 = 18
motor2_e = 22
try:
	GPIO.setup(motor1_in1,GPIO.OUT)
	GPIO.setup(motor1_in2,GPIO.OUT)
	GPIO.setup(motor1_e,GPIO.OUT)
	GPIO.setup(motor2_in1,GPIO.OUT)
	GPIO.setup(motor2_in2,GPIO.OUT)
	GPIO.setup(motor2_e,GPIO.OUT)
	print("motor start")
	p=GPIO.PWM(motor1_e,100)
	p.start(20)
	GPIO.output(motor1_e,GPIO.HIGH)
	GPIO.output(motor1_in2,GPIO.LOW)
	GPIO.output(motor1_in1,GPIO.HIGH)
	GPIO.output(motor2_e,GPIO.HIGH)
	GPIO.output(motor2_in2,GPIO.LOW)
	GPIO.output(motor2_in1,GPIO.HIGH)
	sleep(10);
	p.ChangeDutyCycle(80);
	sleep(5);
	print("stop")
	GPIO.output(motor1_e,GPIO.LOW)
	GPIO.output(motor2_e,GPIO.LOW)
except:
	print("error")
finally:
	GPIO.cleanup()
GPIO.cleanup()
