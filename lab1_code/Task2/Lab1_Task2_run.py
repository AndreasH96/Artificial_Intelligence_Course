from Lab1_Task2_PokerEnvironment import *
#__name__ = "__main__" 

if __name__ == "__main__":
    player1 = ReflexPokerPlayer()
    player2 = MemoryPokerPlayer()
    environment = PokerEnvironment(player1,player2)
    environment.start()