import motor as m
import wheel as w
import move
from time import sleep
m1=m.Motor(11,13,15)
m2=m.Motor(16,18,22)
w1=w.Wheel(m1)
w2=w.Wheel(m2)
obj=move.Move.getInstance(w1,w2)
val=1
try:
	while True:
		data = int(input())
		if data == 1:
			obj.mstart()
		elif data == 2:
			if obj.ready:
				obj.forward()
			else:
				print("Not ready")
		elif data == 3:
			if obj.ready:
				obj.reverse()
			else:
				print("Not ready")
		elif data == 4:
			if obj.ready:
				obj.right()
			else:
				print("Not ready")
		elif data == 5:
			if obj.ready:
				obj.left()
			else:
				print("Not ready")
		elif data == 6:
			if obj.ready:
				obj.mhalt()
			else:
				print("Not ready")
		elif data == 7:
			if obj.ready:
				obj.finish()
			break
		else:
			break

	if obj.ready:
		obj.mhalt()
		obj.finish()
	val=0
except:
	print("errroror")
finally:
	if val == 1:
		obj.mstart()
		obj.mhalt()
		obj.finish()
