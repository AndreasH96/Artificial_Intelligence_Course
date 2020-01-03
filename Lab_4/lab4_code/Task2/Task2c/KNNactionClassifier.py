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
from sklearn.model_selection import cross_val_score
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

    # Append the 
    numericalDataLine.append(finalAction)

    numericalData.append(numericalDataLine)

#======= SEPARATE TRAIN AND TEST SETS ======

dataInput =[dataLine[:len(dataLine)-1] for dataLine in numericalData ]
dataTarget = [dataLine[-1] for dataLine in numericalData]


classifiers = [ ]

#======== MATPLOT SETTINGS ===========
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')
colors = ['g', 'r', 'c']

#========= EVALUATE DATA THROUGH CLASSIFIERS =====
kRange = list(np.arange(1, 100, 2))
distanceAlgorithms = ["Manhattan","Euclidean"]
for pValue, algorithmName in enumerate(distanceAlgorithms):
    scores = []
    maxAccuracy = {"round":0,"accuracy":0}
    for kValue in kRange:
        classifier = KNeighborsClassifier(n_neighbors=kValue,weights='uniform',p=pValue+1)

        score = cross_val_score(classifier, dataInput ,dataTarget)
        scores.append(score.mean())
        if score.mean() > maxAccuracy["accuracy"]:
            maxAccuracy["round"] = kValue
            maxAccuracy["accuracy"] = score.mean()

    distanceAlgorithms[pValue] += " Max accuracy:{} K:{}".format(round(maxAccuracy["accuracy"],4),maxAccuracy["round"])
    plt.plot(kRange, scores, '{}o:'.format(colors[pValue]))
plt.legend(distanceAlgorithms)

plt.xlabel("K-Value")
plt.ylabel("Accuracy")
plt.show()




