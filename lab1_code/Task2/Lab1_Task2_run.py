from Lab1_Task2_PokerEnvironment import *


if __name__ == "__main__":
    player1 = FixedPokerPlayer()
    player2 = MemoryPokerPlayer()
    environment = PokerEnvironment(player1,player2)
    environment.generateCorrelationComparisonPlays()
    environment.start()
    player2.evaluateOpponent()
    