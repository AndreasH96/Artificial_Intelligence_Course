from Lab1_Agents_Task2_Card import Card
import json

class Hand:

    def __init__(self):
        self.cards = []
        with open ('lab1_code\Task2\cards.json') as json_file:
            self.rankToValueJSON = json.load(json_file)['cards']

    def updateHand(self, newHand):
        self.cards = newHand
     # identify hand category using IF-THEN rule
    def identifyHand(self):
        #---Evaluate if 3 of a kind ---
        Hand_ = self.cards
        cardPairings = {"Category":'unknown',"Value": 0, "cards":list(set([(card.rank,card.suit, self.countSameRank(card.rank)) for card in Hand_]))}

        # Sort cards according to their rank, by using loopup table
        cardPairings["cards"].sort(key=lambda card:self.rankToValueJSON[card[0]], reverse= True)
        # Sort cards according to one amount of same ranks in hand
        cardPairings["cards"].sort(key=lambda card:card[2], reverse= True)

        if cardPairings["cards"][0][2] == 3:
            cardPairings["Category"] = "Three of a kind"
        elif cardPairings["cards"][0][2] == 2:
            cardPairings["Category"] = "Pair"
        else:
            cardPairings["Category"] = "One of a kind"
    
        cardPairings["Value"] = pow(10, cardPairings["cards"][0][2]) * self.rankToValueJSON(cardPairings["cards"][0][0])
        return cardPairings

    
    # Print out the result
    def countSameRank(self, cardRank):
        counter = 0
        for cardIndex in range(3):
            if cardRank == self.cards[cardIndex].rank:
                counter+=1
        return counter

    