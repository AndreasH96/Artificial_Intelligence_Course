__author__ = 'fyt'
import math
import random
# identify if there is one or more pairs in the hand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

# 2 example poker hands
CurrentHand1 = ['Ad', '2s', '2c']
CurrentHand2 = ['5s', '5c', '5d']

def generateHand(occupiedCards = []):

    def generateCard():
        possibleRanks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        possibleSuits = ['s', 'h', 'd', 'c']
        return possibleRanks[random.randint(0,12)] + possibleSuits[random.randint(0,3)]

    playerHand = []
    for cardIndex in range(0,3):
        generatedCard = generateCard()
        while generatedCard in playerHand or generatedCard in occupiedCards:
            generatedCard = generateCard()
        playerHand.append(generatedCard)
    return playerHand

# identify hand category using IF-THEN rule
def identifyHand(Hand_):
    for c1 in Hand_:
        for c2 in Hand_:
            if (c1[0] == c2[0]) and (c1[1] < c2[1]):
                yield dict(name='pair',rank=c1[0],suit1=c1[1],suit2=c2[1])

# Print out the result
def analyseHand(Hand_):
    HandCategory = []

    functionToUse = identifyHand

    for category in functionToUse(Hand_):
        print('Category: ')
        for key in "name rank suit1 suit2".split():
            print (key,"=",category[key])
        print

hand = generateHand()
hand2 = generateHand(hand)
print(hand)
print(hand2)
analyseHand(hand)
analyseHand(hand2)



