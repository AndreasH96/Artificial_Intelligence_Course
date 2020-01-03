import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

trainSet, testSet = train_test_split(data, test_size=0.2)

sklearnmethods = ["manhattan","euclidean"]
k_values = np.arange(1,50,2)
max_k = max(k_values)
trainSetInput = trainSet[:, :8]
trainSetTarget = trainSet[:, 9]

testSetInput = testSet[:, :8]
testSetTarget = testSet[:, 9]
legends = ["Manhattan","Euclidean"]
maxScores = []

colors = ['g*-','r*-']
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')

for p,method in enumerate(sklearnmethods,0):
    sklearnScores = []
    maxScoreAndK = {"K":0,"score":0}
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        sklearnKNN = KNeighborsClassifier(n_neighbors=k,weights='uniform',p=p + 1)
        cross_val = cross_val_score(sklearnKNN, testSetInput,testSetTarget,cv = 100)
        score = cross_val.mean()
        if score > maxScoreAndK.get("score"):
            maxScoreAndK["K"] = k 
            maxScoreAndK["score"] = score
        sklearnScores.append(score)
    maxScores.append(maxScoreAndK)
    plt.plot(k_values, sklearnScores, '{}'.format(colors[p]))

for index, maxScore in enumerate(maxScores):
    legends[index] += " Max accuracy:{} K:{}".format(maxScore["score"],maxScore["K"])

plt.legend(legends)
plt.ylim(0.2, 1)
plt.xticks(np.arange(min(k_values), max(k_values)+1, 4.0))
plt.ylabel("Accuracy")
plt.xlabel("K-Value")
plt.show()