import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# Neural network multilayer perception
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

trainSet, testSet = train_test_split(data, test_size=0.2)

trainSetInput = trainSet[:, :8]
trainSetTarget = trainSet[:, 9]

testSetInput = testSet[:, :8]
testSetTarget = testSet[:, 9]

DATALENGTH = len(testSetInput[0])

legends = ["Neural Network", "Decision Tree", "Random Forest"]

classifiers = [MLPClassifier(alpha=1, max_iter=1000),
               DecisionTreeClassifier(max_depth=6), RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)]

font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')
colors = ['g', 'r', 'c']

roundNumberList = np.arange(1, 50, 1)
for name, classifier, color in zip(legends, classifiers, colors):
    scores = []
    maxAccuracy = {"round":0,"accuracy":0}
    for roundNumber in roundNumberList:
        classifier.fit(trainSetInput, trainSetTarget)
        score = classifier.score(testSetInput, testSetTarget)
        scores.append(score)
        if score > maxAccuracy["accuracy"]:
            maxAccuracy["round"] = roundNumber
            maxAccuracy["accuracy"] = score
    legends[classifiers.index(classifier)] += " Max accuracy:{} Round:{}".format(maxAccuracy["accuracy"],maxAccuracy["round"])
    plt.plot(roundNumberList, scores, '{}o:'.format(color))
    plt.ylim(0.5, 1)
plt.xlabel("Round")
plt.ylabel("Accuracy")
plt.legend(legends)

plt.show()
