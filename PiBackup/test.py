from time import sleep
import wheel as mov
import motor
m=motor.Motor(11,13,15)
print(m.in1)
print(m.in2)
print(m.e)
mov.setup(m)
mov.start(m)
mov.front(m)
sleep(5)
mov.reverse(m)
sleep(5)
mov.reverse(m)
sleep(5)
mov.front(m)
sleep(5)
mov.stop(m)
mov.terminate(m)
