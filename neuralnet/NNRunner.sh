#!usr/bin/bash
#Run the training neural network program N times in Ubuntu/Raspbian(in this case N=20, can be easily modified)
for i in {1..20}
do
	sudo python3 MicroPNN.py
done