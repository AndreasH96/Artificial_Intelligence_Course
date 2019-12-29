import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from KNNRegression import KNNRegression
from sklearn.neighbors import KNeighborsRegressor
from operator import itemgetter

# import data from csv file
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

# split data into train and test set
trainSet, testSet = train_test_split(data, test_size=0.2)

# create the itemgetter for the input data
itemIndexes = np.arange(len(data[0]))
dataGetterForInput = itemgetter(np.delete(itemIndexes, [7,8]))


# split the targetcolum to be calculated from the input data
trainSetInput = list(map(list, map(dataGetterForInput, trainSet)))
trainSetTarget = trainSet[:, 7]

testSetInput = list(map(list, map(dataGetterForInput, testSet)))
testSetTarget = testSet[:, 7]

DATALENGTH = len(testSetInput[0])

sklearnmethods = ["manhattan","euclidean"]
k_values = np.arange(1,13,2)
max_k = max(k_values)

legends = ["Custom:Manhattan", "Custom:Euclidean" , "Custom:Cosine", "Custom:Chebyshev"]
maxScores = []
customColorCustomization = ['mo:','co:','wo:','yo:']
params = {'legend.fontsize': 16,
          'legend.handlelength': 2}
plt.rcParams.update(params)
plt.style.use('dark_background')

customMethods = ["manhattan","euclidean","cosine","chebyshev"]

print("===CUSTOM METHODS===")
for methodIndex,method in enumerate(customMethods,0):
    customScores = []    
    maxScoreAndK = {"K":0,"score":0}
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        customKNN = KNNRegression(data=data,indexToPredict = 7,K_val = k,distanceMethod = method)

        score = customKNN.analyzeData() 
        if score > maxScoreAndK.get("score"):
            maxScoreAndK["K"] = k 
            maxScoreAndK["score"] = score

        customScores.append(score)

    maxScores.append(maxScoreAndK)

    plt.plot(k_values, customScores, '{}'.format(customColorCustomization[methodIndex]))
   

for index, maxScore in enumerate(maxScores):
    legends[index] = legends[index] + ", Max:{}, K:{}".format(maxScore["score"],maxScore["K"])

plt.legend(legends)
plt.xticks(np.arange(min(k_values), max(k_values)+1, 4.0))
#plt.savefig("comparison.png")
plt.ylabel("Accuracy in %")
plt.title("KNN regression")
plt.xlabel("K value")
plt.show()