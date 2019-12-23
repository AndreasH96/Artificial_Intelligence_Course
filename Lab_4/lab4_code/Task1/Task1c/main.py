import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from KNNClassifier import KNNClassifier
from sklearn.neighbors import KNeighborsClassifier

data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

trainSet, testSet = train_test_split(data, test_size=0.2)

methods = ["manhattan","euclidean"]
k_values = np.arange(1,100,2)
max_k = max(k_values)
trainSetInput = trainSet[:, :8]
trainSetTarget = trainSet[:, 9]

testSetInput = testSet[:, :8]
testSetTarget = testSet[:, 9]
legends = ["Sklearn:Manhattan","Custom:Manhattan","Sklearn:Euclidean", "Custom:Euclidean" , "Custom:Cosine", "Custom:Chebyshev"]

sklearnColorCustomization = ['g*-','r*-']
customColorCustomization = ['mo:','co:','wo:','yo:']
params = {'legend.fontsize': 16,
          'legend.handlelength': 2}
plt.rcParams.update(params)
plt.style.use('dark_background')
for p,method in enumerate(methods,1):
    sklearnScores = []
    customScores = []
    for k in k_values:
        
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        sklearnKNN = KNeighborsClassifier(n_neighbors=k,weights='uniform',p=p)
        sklearnKNN.fit(trainSetInput,trainSetTarget)
        sklearnScores.append(sklearnKNN.score(testSetInput,testSetTarget) )


        customKNN = KNNClassifier(data=data,K_val = k,distanceMethod = method)
        customScores.append(customKNN.analyzeData() / 100.0)
    plt.plot(k_values, sklearnScores, '{}'.format(sklearnColorCustomization[p-1]))
    plt.plot(k_values, customScores, '{}'.format(customColorCustomization[p-1]))

solelyCustomMethods = ['cosine', 'chebyshev']
for methodIndex,method in enumerate(solelyCustomMethods,2):
    customScores = []    
    for k in k_values:
        print("{}:|{}{}|".format(method, "#"*k,"-"*(max_k-k) ))
        customKNN = KNNClassifier(data=data,K_val = k,distanceMethod = method)
        customScores.append(customKNN.analyzeData() / 100.0)

    plt.plot(k_values, customScores, '{}'.format(customColorCustomization[methodIndex   ]))
plt.legend(legends)
plt.ylim(0.2, 1)
plt.xticks(np.arange(min(k_values), max(k_values)+1, 4.0))
plt.savefig("comparison.png")
plt.show()