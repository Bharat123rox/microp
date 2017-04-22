#IMPORTANT: 0 for STOP, 1 for FRONT, 2 for BACK, 3 for RIGHT, 4 for LEFT 
'''from sknn.mlp import Classifier, Layer
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split '''
import numpy as np
from numpy.random import random
import pickle
#Input has to be of the form np.ndarray or csv file or txt file neatly tabulated
data = np.genfromtxt('training_data.csv',delimiter=',')
print(data)
'''nn = Classifier(
	layers = [Layer('Sigmoid',units=4),
	Layer('Sigmoid',units=4),	
	Layer('Softmax')],	
	learning_rate=0.015,
	n_iter=4000)
X_train,X_test,y_train,y_true = train_test_split(X,y,test_size=0.2)
nn.fit(X_train,y_train) #Train the neural network for n_iter iterations
y_test = nn.predict(X_test) #Test the neural network's predictions
print(y_test)
score = accuracy_score(y_true,y_test) #Get the accuracy
if score>0.5:
	pickle.dump(nn,open('nn.pkl','wb'))	#Save the trained neural network if it has >50% accuracy	
print(score)'''