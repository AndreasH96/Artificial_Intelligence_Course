import numpy as np
from sklearn.model_selection  import train_test_split
from sklearn import svm
import os
import math
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.colors import ListedColormap

class KNNClassifier():

    def __init__ (self,data):
        # assert data
        self.data = data
    
        self.trainSet, self.testSet = train_test_split(self.data, test_size=0.2)

        self.testSetInput = self.testSet[:, :8]
        self.testSetTarget = self.testSet[:, 9]
        self.DATALENGTH = len(self.testSetInput[0])

        self.K = 3
        
    
    def getKNNeighbors(self,trainingSet, dataPoint, k):
        
        def euclideanDistance(dataPoint1, dataPoint2, length):
            distance = 0
            distance = math.sqrt(sum([pow(dataPoint1[x] - dataPoint2[x],2) for x in range(length)]))
            return distance

        neighborDistances = list(map(lambda 
            trainingDataPoint: (trainingDataPoint, euclideanDistance(trainingDataPoint,dataPoint,self.DATALENGTH)) ,trainingSet))

        neighborDistances.sort(key=lambda point: point[1])

        return  [neighbor[0] for neighbor in neighborDistances[:k]]

    def predictOutcome(self,testSetWithNeighbors):
        outComes = []
        for testNode in testSetWithNeighbors:
            neighborClassCounter = Counter(testNode[1][x][self.DATALENGTH +1] for x in range(len(testNode[1])))
            outComes.append(max(neighborClassCounter, key = neighborClassCounter.get))

        return outComes

    def setK(self, newK):
        self.K = newK

    def analyzeData(self,plot ):

        def plotOutCome(outComeClasses):
            plt.style.use('default')
            plt.style.use('seaborn-talk')
            cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
            cmap_bold = ListedColormap(['darkorange', 'c', 'darkblue'])
            dataPointColors = ('r' , 'b' , 'g')
            #for dataPoint in self.trainSet:
            h = .02 # step size in the mesh

            x_min, x_max = self.testSetInput[:,5].min() , self.testSetInput[:,5].max()
            y_min, y_max = self.testSetInput[:,6].min(), self.testSetInput[:,6].max() 
            xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
            plt.figure(1, figsize=(4, 3))
            print(xx.shape)
            #print(xx..shape)
            Z = np.array(np.array(self.testSetTarget))
            print(Z.shape)

            print(Z)
            Z = Z.reshape(xx.ravel().shape)
            plt.figure()
            plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

            plt.scatter( self.trainSet[:, 6], self.trainSet[:, 5], c=[point[9] for point in self.trainSet], cmap=cmap_bold,
            edgecolor='k', s=20)
            #plt.figure()
            #plt.pcolormesh()
            print(self.trainSet[:, 0])
            #plt.plot(dataPoint[8] ,dataPoint[9],'{},'.format(dataPointColors[int(dataPoint[9])-1]))
                
            plt.show()
        
        print ('*******************************************')
        print('Length of Total Data:', len(self.data))
        print ('*******************************************')
        print('Length of Train Data:', len(self.trainSet))
        print('Length of Test Data', len(self.testSet))

        testsetNeighbors = [(testPoint,self.getKNNeighbors(self.trainSet,testPoint,self.K)) for testPoint in self.testSetInput] 
        predictedOutcome = self.predictOutcome(testsetNeighbors)

        Number_of_Correct_Predictions = len([i for i, j in zip(predictedOutcome, self.testSetTarget) if i == j])
        

        testAccuracy = (Number_of_Correct_Predictions/float(len(predictedOutcome)))*100
        print ('*******************************************')
        print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(predictedOutcome),
            'Number of Test Data')
        print('Accuracy of Prediction in Percent:', testAccuracy) 

        if plot:
            plotOutCome(predictedOutcome)
             
            
        
            