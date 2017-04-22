import read
import sys
import time
import numpy as np
import sklearn
import test1 as vandi
from sklearn.externals import joblib
#IMPORTANT: 0 for STOP, 1 for FRONT, 2 for BACK, 3 for LEFT, 4 for RIGHT 
try:
	nn = joblib.load('finalnn.sav')
except IOError as e:	
	pass
fetch = read.InclinationFetcher()
val=0
try:
	inp = int(input())
	while (inp != 10 ):
		inp = int(input())

	fetch.start()
	vandi.start(True)
	while True:
		time.sleep(0.1)
		geti = fetch.get_inclination()
		data = []
		data.append(geti['x'])
		data.append(geti['y'])
		data.append(geti['z'])
		x_in = np.asarray(data)
		x_in = x_in.reshape(1,3)
		#print(x_in)
		y_out = nn.predict(x_in)
		command = int(y_out[0])
		vandi.move(command)
		
except KeyboardInterrupt:
	#print(type(y_out))
	fetch.stop()
	vandi.finish(True)
	sys.exit()
	
finally:
	fetch.stop()
	vandi.finish(True)
	sys.exit()

