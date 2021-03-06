import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numericalValues import handTypeValueLookupTable, cardValueLookupTable, actionValueLookupTable
from pandas import DataFrame

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.svm import SVC
from operator import itemgetter
import re
# 2A: 1. Amount of money left for player  2. Players average bet 3. 



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
    moneyRemaining = []
    averageBetAmounts = []
    playerAggressivity = []
    # Split the actions into a list, with the empty filter removing indices containing empty strings
    dataLineSplit = list(filter(None,re.split(" |,",dataLine)))
    initialMoney = [int(dataLineSplit[3]), int(dataLineSplit[6])]
    playerActions = dataLineSplit[7:]
    actionsLineLength = len(playerActions)
    # Generate list of player 1 betting amounts
    player1ActionValues = [int(x) for x in playerActions[1::4]]
    # Generate list of player 2 betting amount, excluding the last action
    player2ActionValues = [int(x) for x in playerActions[3:actionsLineLength - 2 :4]]

    # Calculate the amount of money left for each player
    moneyRemaining.append(initialMoney[0] - sum(player1ActionValues))
    moneyRemaining.append(initialMoney[1] - sum(player2ActionValues))
    
    # Calculate the average of the player1 actions
    averageBetAmounts.append(sum(player1ActionValues) / len(playerActions[1::4]))
    # Calculate the average of the player2 actions
    averageBetAmounts.append(sum(player2ActionValues) / len(playerActions[3: actionsLineLength - 2:4]))

    # Calculate the aggressivity of the players, the ratio of their average bettings
    playerAggressivity.append(averageBetAmounts[0]/averageBetAmounts[1])
    playerAggressivity.append(averageBetAmounts[1]/averageBetAmounts[0])

    # Read the final action of player2, this is the target value for the classifier
    p2FinalAction = actionValueLookupTable[playerActions[-2]]
    return moneyRemaining, averageBetAmounts, playerAggressivity, p2FinalAction

data = np.loadtxt(open("lab4_code\Task2\Lab4PokerData.txt", "rb"),
                  delimiter="\n", dtype=str)

numericalData = []

for dataLine in data:
    numericalDataLine = []
    # Add the numerical version of the players hands
    numericalDataLine.extend(evaluatePlayerHands(dataLine))

    # Evaluate the average bets of the players and the final action of player 2
    # The last action of player 2 is left out of the average bets
    remainingMoney, averageBetAmounts, playerAggressivity, finalAction = evaluatePlayerActions(dataLine)

    numericalDataLine.extend(remainingMoney)

    numericalDataLine.extend(averageBetAmounts)

    numericalDataLine.extend(playerAggressivity)

    # Append the final action of player 2
    numericalDataLine.append(finalAction)

    numericalData.append(numericalDataLine)
    print(numericalDataLine)
    break

#======= SEPARATE TRAIN AND TEST SETS ======
trainSet, testSet = train_test_split(numericalData, test_size=0.2)
trainSetInput = [trainSetLine[:len(trainSetLine)-1] for trainSetLine in trainSet ]
trainSetTarget = [trainSetLine[-1] for trainSetLine in trainSet]


testSetInput = [testSetLine[:len(testSetLine)-1] for testSetLine in testSet ]
testSetTarget = [testSetLine[-1] for testSetLine in testSet]


classifiers = [ KNeighborsClassifier(n_neighbors=9,weights='distance',p=1),
               DecisionTreeClassifier(max_depth=7), RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)]

#======== MATPLOT SETTINGS ===========
legends = ["KNN", "DecisionTree", "Random Forest"]
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')
colors = ['g', 'r', 'c']

#========= EVALUATE DATA THROUGH CLASSIFIERS =====
roundNumberList = list(np.arange(1, 100, 1))
for classifier, color in zip(classifiers, colors):
    scores = list()
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
    
plt.legend(legends)
plt.xlabel("Round")
plt.ylabel("Accuracy")
plt.ylim(0.5,1)
plt.show()




