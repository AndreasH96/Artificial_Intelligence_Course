import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numericalValues import handTypeValueLookupTable, cardValueLookupTable, actionValueLookupTable
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from operator import itemgetter
# 2A: 1.


def calcHandValue(hand):
    value = 100 * (hand["type"]) + 8 * hand["card"]
    return value


def evaluateHandString(handString):
    handData = list(filter(None, handString.split(" ")))
    #evaluatedHand = {"value": 0, "cash": 0}
    #hand = {"type":handTypeValueLookupTable[handData[0]], "card": cardValueLookupTable[handData[1]]}
    evaluatedHand = []
    evaluatedHand.append(handTypeValueLookupTable[handData[0]])
    evaluatedHand.append(cardValueLookupTable[handData[1]])
    evaluatedHand.append(int(handData[2]))
    """ evaluatedHand["value"] = calcHandValue(hand)
    evaluatedHand["cash"] = handData[2] """

    return evaluatedHand


def evaluateActionString(actionString):
    actionData = list(filter(None, actionString.split(" ")))
    evaluatedActions = {"p1": {"action": 0, "amount": 0},
                        "p2": {"action": 0, "amount": 0}}

    evaluatedActions["p1"]["action"] = actionValueLookupTable[actionData[0]]
    evaluatedActions["p1"]["amount"] = int(actionData[1])
    if len(actionData) > 2:
        evaluatedActions["p2"]["action"] = actionValueLookupTable[actionData[2]]
        evaluatedActions["p2"]["amount"] = int(actionData[3])

    return evaluatedActions


data = np.loadtxt(open("lab4_code\Task2\Lab4PokerData.txt", "rb"),
                  delimiter="\n", dtype=str)

numericalData = []
for dataLine in data:
    numericalDataLine = []
    sections = dataLine.split(',')
    player1Hand = evaluateHandString(sections[1])
    player2Hand = evaluateHandString(sections[2])
    playerHands = player1Hand + player2Hand
    for section in playerHands:
        numericalDataLine.append(section)

    for action in sections[3:]:
        if action != " ":
            evaluatedAction = evaluateActionString(action)
            numericalDataLine.append(evaluatedAction["p1"]["action"])
            numericalDataLine.append(evaluatedAction["p1"]["amount"])
            if len(action) > 2:
                numericalDataLine.append(evaluatedAction["p2"]["action"])
                numericalDataLine.append(evaluatedAction["p2"]["amount"])

            # numericalDataLine.append(evaluateActionString(action))
    numericalData.append(numericalDataLine)
# print(DataFrame(numericalData))

trainSet, testSet = train_test_split(numericalData, test_size=0.2)
trainSetInput = []
trainSetTarget = []

for trainSetLine in trainSet:
    lineLength = len(trainSetLine)
    itemIndexes = np.arange(lineLength)
    #3,4,5,
    dataGetterForInput = np.delete(itemIndexes, (lineLength - 2, lineLength-1))
    
    # split the targetcolum to be calculated from the input data
    trainSetInput.append([trainSetLine[x] for x in dataGetterForInput])

    #inputDataGetter = itemgetter()
    #trainSetInput.append(trainSetLine[:12])
    trainSetTarget.append(trainSetLine[lineLength-2])
print(trainSet)


testSetInput = [[]]
testSetTarget = [[]]
for testSetLine in testSet:
    lineLength = len(testSetLine)
    itemIndexes = np.arange(lineLength)
    #3,4,5,
    dataGetterForInput = np.delete(itemIndexes, (lineLength - 2, lineLength-1))

    testSetInput.append(list([testSetLine[x] for x in dataGetterForInput]))
    testSetTarget.append(testSetLine[lineLength-2])

print(DataFrame(numericalData))

classifiers = [RandomForestClassifier(
    max_depth=5, n_estimators=10, max_features=1)]

scores = []
colors = ['g', 'r', 'b']
for classifier, color in zip(classifiers, colors):
    roundNumberList = np.arange(1, 10, 1)

    for roundNumber in roundNumberList:
        classifier.fit(trainSetInput, trainSetTarget)
        scores.append(classifier.score(testSetInput, testSetTarget))

    plt.plot(roundNumberList, scores, '{}o:'.format(color))
plt.show()
