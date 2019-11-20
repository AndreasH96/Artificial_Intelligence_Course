from Lab1_Task2_PokerEnvironment import *


if __name__ == "__main__":
    player1 = FixedPokerPlayer()
    player2 = RandomPokerPlayer()
    environment = PokerEnvironment(player1,player2)
    environment.start()
