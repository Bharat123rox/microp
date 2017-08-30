# Microprocessors Project
This was a group project and this repository contains the code for making a Gesture Controlled Wheelchair Prototype 
using Raspberry Pi 3 and certain Python Libraries which utilize the GPIO Functionality of the Raspberry Pi
## My contributions
My contributions to this project had been a neural network to drive the motor left, right, front and back, whose core component is
[this Neural Network](https://github.com/Bharat123rox/microp/blob/master/neuralnet/MicroPNN.py)
in which supervised learning has been used in the form of an Artificial Neural Network (ANN)
### Training data
Training data was obtained from the CSV file [here](https://github.com/Bharat123rox/microp/blob/master/neuralnet/MicroPdata.csv) 
of around 10,000 samples for training the vehicle and the neural network was 'pickled' (saved as an object) to disk as a
[Saved Neural Net](https://github.com/Bharat123rox/microp/blob/master/neuralnet/finalnn.sav)
