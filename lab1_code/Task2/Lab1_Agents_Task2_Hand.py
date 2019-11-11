from Lab1_Agents_Task2_Card import Card
class Hand:

    def __init__(self, playerId):
        self.HolderId = playerId
        self.cards = []
    def updateHand(self, newHand):
        self.cards = newHand
     # identify hand category using IF-THEN rule
    def identifyHand(self):
        #---Evaluate if 3 of a kind ---
        
        Hand_ = self.cards
        for card in Hand_:
            print(card.rank, card.suit)
        #print(self.cards)
        print(list(set([(card.rank,card.suit, self.countSameRank(card.rank)) for card in Hand_])))
        
    # Print out the result
    def countSameRank(self, cardRank):
        counter = 0
        for cardIndex in range(3):
            if cardRank == self.cards[cardIndex].rank:
                counter+=1
        return counter

    def analyseHand(self):
        HandCategory = []
        self.identifyHand()
        """functionToUse = self.identifyHand
        print (self.cards)
        for category in functionToUse():
            print('Category: ')
            for key in "name rank suit1 suit2".split():
                print (key,"=",category[key])
            print"""