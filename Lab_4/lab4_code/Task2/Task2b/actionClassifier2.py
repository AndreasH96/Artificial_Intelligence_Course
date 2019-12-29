import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numericalValues import handTypeValueLookupTable, cardValueLookupTable, actionValueLookupTable
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from operator import itemgetter
import re
# 2A: 1. Players average bet, 2. 



def evaluatePlayerHands(dataLine):

    def evaluateHandString(handString):
        handData = list(filter(None, handString.split(" ")))

        evaluatedHand = []
        evaluatedHand.append(handTypeValueLookupTable[handData[0]])
        evaluatedHand.append(cardValueLookupTable[handData[1]])
        evaluatedHand.append(int(handData[2]))

        return evaluatedHand

    dataSections = dataLine.split(',')
    evaluatedHands = []
    player1Hand = evaluateHandString(dataSections[1])
    player2Hand = evaluateHandString(dataSections[2])
    playerHands = player1Hand + player2Hand
    for section in playerHands:
        evaluatedHands.append(section)
    return evaluatedHands

def evaluatePlayerActions(dataLine):
    averageBetAmounts = []
    playerActions = list(filter(None,re.split(" |,",dataLine)))[7:]
    actionsLineLength = len(playerActions)
    averageBetAmounts.append(sum([int(x) for x in playerActions[1::4]]) / len(playerActions[1::4]))
    averageBetAmounts.append(sum([int(x) for x in playerActions[3:actionsLineLength - 2 :4]]) / len(playerActions[3: actionsLineLength - 2:4]))

    p2FinalAction = actionValueLookupTable[playerActions[-2]]
    return averageBetAmounts, p2FinalAction

data = np.loadtxt(open("lab4_code\Task2\Lab4PokerData.txt", "rb"),
                  delimiter="\n", dtype=str)

numericalData = []

for dataLine in data:
    numericalDataLine = []
    # Add the numerical version of the players hands
    numericalDataLine.extend(evaluatePlayerHands(dataLine))

    # Evaluate the average bets of the players and the final action of player 2
    # The last action of player 2 is left out of the average bets
    averageBetAmounts, finalAction = evaluatePlayerActions(dataLine)

    numericalDataLine.extend(averageBetAmounts)

    # Append the 
    numericalDataLine.append(finalAction)

    numericalData.append(numericalDataLine)

print(DataFrame(numericalData))

trainSet, testSet = train_test_split(numericalData, test_size=0.2)
trainSetInput = [trainSetLine[:len(trainSetLine)-1] for trainSetLine in trainSet ]
trainSetTarget = [trainSetLine[-1] for trainSetLine in trainSet]


testSetInput = [testSetLine[:len(testSetLine)-1] for testSetLine in testSet ]
testSetTarget = [testSetLine[-1] for testSetLine in testSet]

legends = ["KNN", "DecisionTree", "Random Forest"]
classifiers = [ KNeighborsClassifier(n_neighbors=7,weights='uniform',p=1 + 1),
               DecisionTreeClassifier(max_depth=6), RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)]

roundNumberList = list(np.arange(1, 10, 1))

params = {'legend.fontsize': 16,
          'legend.handlelength': 2}
plt.rcParams.update(params)
plt.style.use('dark_background')
colors = ['g', 'r', 'c']
for classifier, color in zip(classifiers, colors):
    scores = list()

    for roundNumber in roundNumberList:
        classifier.fit(trainSetInput, trainSetTarget)
        scores.append(classifier.score(testSetInput, testSetTarget))

    plt.plot(roundNumberList, scores, '{}o:'.format(color))
plt.legend(legends)
plt.show()




#========= FORMULATE ATTRIBUTES ======


#======= SEND INTO ML =====