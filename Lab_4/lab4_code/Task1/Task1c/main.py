import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from KNNClassifier import KNNClassifier
from sklearn.neighbors import KNeighborsClassifier

data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

trainSet, testSet = train_test_split(data, test_size=0.2)

sklearnmethods = ["manhattan","euclidean"]
k_values = np.arange(1,2,2)
max_k = max(k_values)
trainSetInput = trainSet[:, :8]
trainSetTarget = trainSet[:, 9]

testSetInput = testSet[:, :8]
testSetTarget = testSet[:, 9]
legends = ["Sklearn:Manhattan","Sklearn:Euclidean","Custom:Manhattan", "Custom:Euclidean" , "Custom:Cosine", "Custom:Chebyshev"]
maxScores = []
sklearnColorCustomization = ['g*-','r*-']
customColorCustomization = ['mo:','co:','wo:','yo:']

font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')


print("===SKLEARN METHODS===")
for p,method in enumerate(sklearnmethods,0):
    sklearnScores = []
    maxScoreAndK = {"K":0,"score":0}
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        sklearnKNN = KNeighborsClassifier(n_neighbors=k,weights='uniform',p=p + 1)
        sklearnKNN.fit(trainSetInput,trainSetTarget)
        score = sklearnKNN.score(testSetInput,testSetTarget) 
        if score > maxScoreAndK.get("score"):
            maxScoreAndK["K"] = k 
            maxScoreAndK["score"] = score
        sklearnScores.append(score)
    maxScores.append(maxScoreAndK)

    plt.plot(k_values, sklearnScores, '{}'.format(sklearnColorCustomization[p]))
    #plt.annotate(s = maxScoreAndK["score"], xy = (maxScoreAndK["K"] + 0.05,maxScoreAndK["score"] +0.01),size = 20)
    #plt.text(s = "{}:{}:k={}".format(method,maxScoreAndK["score"],maxScoreAndK["K"]), x = maxScoreAndK["K"],y= maxScoreAndK["score"] +0.01,fontsize= 12)
    

solelyCustomMethods = ['cosine', 'chebyshev']

customMethods = ["manhattan","euclidean","cosine","chebyshev"]

print("===CUSTOM METHODS===")
for methodIndex,method in enumerate(customMethods,0):
    customScores = []    
    maxScoreAndK = {"K":0,"score":0}
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        customKNN = KNNClassifier(data=data,K_val = k,distanceMethod = method)

        score = customKNN.analyzeData(True) / 100.0
        if score > maxScoreAndK.get("score"):
            maxScoreAndK["K"] = k 
            maxScoreAndK["score"] = score

        customScores.append(score)

    maxScores.append(maxScoreAndK)

    plt.plot(k_values, customScores, '{}'.format(customColorCustomization[methodIndex]))
    #plt.text(s = "{}:{}:k={}".format(method,maxScoreAndK["score"],maxScoreAndK["K"]), x = maxScoreAndK["K"],y= maxScoreAndK["score"] +0.01,fontsize= 12)


for index, maxScore in enumerate(maxScores):
    legends[index] += " Max accuracy:{} Round:{}".format(maxScore["score"],maxScore["K"])

plt.legend(legends)
plt.ylim(0.2, 1)
plt.xticks(np.arange(min(k_values), max(k_values)+1, 4.0))
plt.ylabel("Accuracy")
plt.xlabel("K-Value")
plt.show()