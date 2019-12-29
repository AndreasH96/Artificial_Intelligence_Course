import numpy as np
from sklearn.model_selection  import train_test_split
from sklearn import svm
import os
import math
from numpy import dot
from numpy.linalg import norm
from collections import Counter
#distanceFunctions = ["euclideanDistance", "manhattanDistance", "cosineDistance"]

class KNNClassifier():

    def __init__ (self,data,K_val = 3, distanceMethod = "manhattan"):
        # assert data
        self.data = data
        self.K = K_val
        self.trainSet, self.testSet = train_test_split(self.data, test_size=0.2)
        self.distanceMethod = distanceMethod
        self.testSetInput = self.testSet[:, :8]
        self.testSetTarget = self.testSet[:, 9]
        self.DATALENGTH = len(self.testSetInput[0])
        
    
    def getKNNeighbors(self,trainingSet, dataPoint, k):
        
        def distance(dataPoint1, dataPoint2, length):
            manhattanOrEucliean = ["manhattan", "euclidean"]
            if self.distanceMethod in manhattanOrEucliean:
                p = manhattanOrEucliean.index(self.distanceMethod) + 1
                distance = pow(sum([pow(dataPoint1[x] - dataPoint2[x],p) for x in range(length)]), (1/p))

            elif self.distanceMethod == "cosine":
                distance = dot(dataPoint1[0:length],dataPoint2)/(norm(dataPoint1)*norm(dataPoint2))
                #print(distance)
            elif self.distanceMethod == "chebyshev":
                distance = max([abs(dataPoint1[x] - dataPoint2[x]) for x in range(length)])
            
            if self.distanceMethod in ["manhattan",'cosine']:
                    distance = 1/distance
            return distance

        neighborDistances = list(map(lambda 
            trainingDataPoint: (trainingDataPoint,distance(trainingDataPoint,dataPoint,self.DATALENGTH)) ,trainingSet))

        neighborDistances.sort(key=lambda point: point[1])

        return [neighbor[0] for neighbor in neighborDistances[:k]]

    def predictOutcome(self,testSetWithNeighbors):
        outComes = []
        for testNode in testSetWithNeighbors:
            neighborClassCounter = Counter(testNode[1][x][self.DATALENGTH +1] for x in range(len(testNode[1])))
            outComes.append(max(neighborClassCounter, key = neighborClassCounter.get))

        return outComes

    def setK(self, newK):
        self.K = newK

    def analyzeData(self,printStats=False ):


        testsetNeighbors = [(testPoint,self.getKNNeighbors(self.trainSet,testPoint,self.K)) for testPoint in self.testSetInput] 
        predictedOutcome = self.predictOutcome(testsetNeighbors)

        Number_of_Correct_Predictions = len([i for i, j in zip(predictedOutcome, self.testSetTarget) if i == j])
        

        testAccuracy = (Number_of_Correct_Predictions/float(len(predictedOutcome)))*100
        if printStats:
            print ('*******************************************')
            print('Length of Total Data:', len(self.data))
            print ('*******************************************')
            print('Length of Train Data:', len(self.trainSet))
            print('Length of Test Data', len(self.testSet))
            print ('*******************************************')
            print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(predictedOutcome),
                'Number of Test Data')
            print('Accuracy of Prediction in Percent:', testAccuracy) 
        return testAccuracy
             
            
        
            