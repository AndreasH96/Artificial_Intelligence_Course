import numpy as np
from sklearn.model_selection  import train_test_split
from sklearn import svm
import os
import math
from numpy import dot
from numpy.linalg import norm
from collections import Counter
from operator import itemgetter
class DataPoint():
    def __init__(self,inputData, target):
        self.inputData = inputData
        self.targetValue = target

class KNNRegression():

    def __init__ (self,data,indexToPredict,K_val = 3, distanceMethod = "manhattan"):
        # assert data
        self.data = data
        self.indexToPredict = indexToPredict
        self.K = K_val
        self.trainSet, self.testSet = train_test_split(self.data, test_size=0.2)
        self.distanceMethod = distanceMethod
        itemIndexes = np.arange(len(data[0]))
        
        dataGetterForInput = itemgetter(np.delete(itemIndexes,indexToPredict))

        self.trainSetInput = list(map(list,map(dataGetterForInput,self.trainSet)))
        self.trainSetTarget = self.trainSet[:, indexToPredict]
        self.trainSetDataPoints = list()

        for inputData, targetValue in zip(self.trainSetInput,self.trainSetTarget):
            self.trainSetDataPoints.append(DataPoint(inputData,targetValue))
        
        self.testSetInput = list(map(list,map(dataGetterForInput,self.testSet)))
        self.testSetTarget = self.testSet[:, 7]
        self.testSetDataPoints = list()

        for inputData, targetValue in zip(self.testSetInput,self.testSetTarget):
            self.testSetDataPoints.append(DataPoint(inputData,targetValue))
        self.DATALENGTH = len(self.testSetInput[0])
        
    
    def getKNNeighbors(self, dataPoint, k):
        
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
            trainingDataPoint: (trainingDataPoint,distance(trainingDataPoint.inputData,dataPoint,self.DATALENGTH)), self.trainSetDataPoints))
        
        neighborDistances.sort(key=lambda point: point[1])

        return [neighbor for neighbor in neighborDistances[:k]]

    def predictOutcome(self,testSetWithNeighbors):
        outComes = []
        for testNode in testSetWithNeighbors:
            
            distanceTimesValSum = 0
            distanceSum = 0
            for neighbor in testNode[1]:
                neighBorDistance = neighbor[1]
                neighborVal = neighbor[0].targetValue

                distanceTimesValSum += (1/neighBorDistance) * neighborVal 
                distanceSum += (1/neighBorDistance)
            
            outCome = distanceTimesValSum/distanceSum
            
            outComes.append(outCome)
                
            


        return outComes

    def setK(self, newK):
        self.K = newK

    def analyzeData(self,printStats=False ):

        testsetNeighbors = [(testPoint,self.getKNNeighbors(testPoint.inputData,self.K)) for testPoint in self.testSetDataPoints] 
        predictedOutcome = self.predictOutcome(testsetNeighbors)

        absoluteError = [abs(predicted - actual)/actual for predicted,actual in zip(predictedOutcome,self.testSetTarget)]
        meanAccuracy = 1 - sum(absoluteError)/len(absoluteError)
        
        """ Number_of_Correct_Predictions = len([i for i, j in zip(predictedOutcome, self.testSetTarget) if abs(i - j) < 2])
        

        testAccuracy = (Number_of_Correct_Predictions/float(len(predictedOutcome)))
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
        return testAccuracy """
        return meanAccuracy
             
            
        
            