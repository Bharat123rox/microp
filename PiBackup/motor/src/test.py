import motor as m
import wheel as w
import move
from time import sleep
m1=m.Motor(11,13,15)
m2=m.Motor(16,18,22)
w1=w.Wheel(m1)
w2=w.Wheel(m2)
ob=move.Move(w1,w2)
val=1
try:
	ob.mstart()
	ob.forward()
	sleep(4)
	ob.reverse()
	sleep(4)
	ob.left()
	sleep(4)
	ob.right()
	sleep(4)
	ob.mhalt()
	ob.finish()
	val=0
except:
	print("errorrrrr")
finally:
	if val == 1:
		ob.mhalt()
		ob.finish()
