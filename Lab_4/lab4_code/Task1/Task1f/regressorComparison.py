import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# Neural network multilayer perception
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from operator import itemgetter
# import data from csv file
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

# split data into train and test set
trainSet, testSet = train_test_split(data, test_size=0.2)

# create the itemgetter for the input data
itemIndexes = np.arange(len(data[0]))
dataGetterForInput = itemgetter(np.delete(itemIndexes, 7))


# split the targetcolum to be calculated from the input data
trainSetInput = list(map(list, map(dataGetterForInput, trainSet)))
trainSetTarget = trainSet[:, 7]

testSetInput = list(map(list, map(dataGetterForInput, testSet)))
testSetTarget = testSet[:, 7]

DATALENGTH = len(testSetInput[0])


regressorNames = ["Neural Network", "Decision Tree", "Random Forest"]

# Initiate the regressors
regressors = [MLPRegressor(alpha=1, max_iter=1000),
               DecisionTreeRegressor(max_depth=6), RandomForestRegressor(max_depth=5, n_estimators=10, max_features=1)]

# matplot styling
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')

colors = ['g', 'r', 'c']
roundNumberList = np.arange(1, 50, 1)

labels = []
for name, regressor, color in zip(regressorNames, regressors, colors):
    maxAccuracy = {"value":0,"round":0}
    scores = []
    for roundNumber in roundNumberList:
        regressor.fit(trainSetInput, trainSetTarget)
        score = regressor.score(testSetInput, testSetTarget)
        scores.append(score)
        if score > maxAccuracy["value"]:
            maxAccuracy["value"] = score
            maxAccuracy["round"] = roundNumber

    # Add max and min accuracy to label of regressor
    labels.append(name + " Max accuracy:{} Round:{}".format(round(maxAccuracy["value"],4),maxAccuracy["round"]))
    plt.plot(roundNumberList, scores, '{}o:'.format(color))


plt.xlabel("Round")
plt.ylabel("$R^{2}$ Score")
plt.legend(labels)

plt.show()
