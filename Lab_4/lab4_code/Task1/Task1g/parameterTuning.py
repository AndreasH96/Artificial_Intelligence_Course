import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
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


# split the targetcolumn to be calculated from the input data
trainSetInput = list(map(list, map(dataGetterForInput, trainSet)))
trainSetTarget = trainSet[:, 7]

testSetInput = list(map(list, map(dataGetterForInput, testSet)))
testSetTarget = testSet[:, 7]

DATALENGTH = len(testSetInput[0])

k_values = np.arange(1,50,2)
max_k = max(k_values)
maxScores = []

legends = ["Manhattan","Euclidean"]
colors = ['g*-','r*-']
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')

for p,method in enumerate(legends,0):
    sklearnScores = []
    maxScoreAndK = {"K":0,"score":-100}
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        sklearnKNN = KNeighborsRegressor(n_neighbors=k,p=p + 1)
        sklearnKNN.fit(trainSetInput,trainSetTarget)
        cross_val = cross_val_score(sklearnKNN, testSetInput ,testSetTarget)
        score = cross_val.mean()
        if score > maxScoreAndK.get("score"):
            maxScoreAndK["K"] = k 
            maxScoreAndK["score"] = score
        sklearnScores.append(score)
    maxScores.append(maxScoreAndK)
    plt.plot(k_values, sklearnScores, '{}'.format(colors[p]))

for index, maxScore in enumerate(maxScores):
    legends[index] += " Max accuracy:{} K:{}".format(round(maxScore["score"],4),maxScore["K"])

plt.legend(legends)

plt.xticks(np.arange(min(k_values), max(k_values)+1, 4.0))
plt.ylabel("$R^{2}$ Score")
plt.xlabel("K-Value")
plt.show()