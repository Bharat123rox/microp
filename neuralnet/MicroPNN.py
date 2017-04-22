from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import MLPClassifier as mlp
import numpy as np
from numpy.random import random, shuffle
from sklearn.externals import joblib
#Input has to be of the form np.ndarray or csv file or txt file, or any other file in neatly tabulated form
data = np.genfromtxt('MicroPdata.csv',delimiter=',') 	#Read data from csv file (Works for CSV files only)
shuffle(data) 											#Shuffles the order of training data so that it can be treated like a new dataset for each iteration of training
X,y = data[:,0:3],data[:,3]								#Extracts inputs and outputs from the 2-D matrix
try:
	nn = joblib.load('finalnn.sav')						#If there is an already trained neural network, train on top of it instead of creating a new neural network
except (FileNotFoundError,IOError) as e:	
	nn = mlp(hidden_layer_sizes=(4,4),activation='identity',solver='sgd',max_iter=4000,learning_rate_init=0.002) #Creates a new neural network with various parameters
X_train,X_test,y_train,y_true = train_test_split(X,y,test_size=0.2) #Split the training data into 80% training and 20% testing data. In general (test_size*100)% testing data and the rest is training data
nn.fit(X_train,y_train) 								#Train the neural network for n_iter iterations, all the magic happens here.
y_test = nn.predict(X_test) 							#Test the neural network's predictions
score = accuracy_score(y_true,y_test) 					#Get the accuracy
if score>0.5:
	joblib.dump(nn,'finalnn.sav')						#Save the trained neural network's parameters to disk if it has > 50% accuracy	
print(score)                        					#Final accuracy is a number between (0,1) both inclusive
