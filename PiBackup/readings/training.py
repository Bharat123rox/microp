import read
import time
import csv,sys
#IMPORTANT: 0 for STOP, 1 for FRONT, 2 for BACK, 3 for RIGHT, 4 for LEFT  
data1 = []
fetch = read.InclinationFetcher(filter_gyro_weight=0.8)
fetch.start()
for i in range(0, 1000):
  time.sleep(0.075)
  geti = fetch.get_inclination()
  data = []
  data.append(geti['x'])
  data.append(geti['y'])
  data.append(geti['z'])
  data.append(0)
  data1.append(list(data))
fetch.stop()
#print(data1)
with open('training_data.csv','a+') as f:
	writer = csv.writer(f)
	for j in range(len(data1)):
		writer.writerow(data1[j])