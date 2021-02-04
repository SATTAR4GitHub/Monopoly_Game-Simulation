"""
Abdus Sattar Mia - 000394648
Dated: Nov 14, 2020

"""
import numpy as np
np.random.seed(1)

class Player:
    def __init__(self):
        self.position = 0    # current position
        self.doubleCounter = 0 # double value counter
        self.isInJail = False # determine if 'just visiting' or 'in jail'?

        # If a plyer has jail free cards or not
        self.isJailFreeChance = False
        self.isJailFreeCommunity = False

        # player's record
        self.squareRecorder = [0] * 40
        self.jailRecorder = [0] * 2

    # Roll two fair six-sided dice
    def rollDice(self):
        diceRoll = [np.random.randint(1, 6+1) for _ in range(2)]
        # Record if it was a double, or reset double counter otherwise
        if diceRoll[0] == diceRoll[1]:
            self.doubleCounter += 1
        else:
            self.resetDoubleCounter()

        return sum(diceRoll)

    # Update and record position
    def updatePosition(self, newPosition):
        self.position = newPosition
        self.squareRecorder[newPosition] += 1
        # Record status at jail
        if newPosition == 10:
                if self.isInJail:
                    self.jailRecorder[1] += 1
                else:
                    self.jailRecorder[0] += 1

    # Reset double counter
    def resetDoubleCounter(self):
        self.doubleCounter = 0

    # Update the possession of jail free cards
    def updateJailFreeStatus(self, getOrUse, chanceOrCommunity):
        if chanceOrCommunity == 'Chance':
            if getOrUse == 'get':
                self.isJailFreeChance = True
            else:
                self.isJailFreeChance = False
        else:
            if getOrUse == 'get':
                self.isJailFreeCommunity = True
            else:
                self.isJailFreeCommunity = False

    # Update jail status
    def updateJailStatus(self, newState):
        self.isInJail = newState

    # Initialize a new game
    def newGame(self):
        self.position = 0
        self.doubleCounter = 0
        self.isInJail = False
        self.isJailFreeChance = False
        self.isJailFreeCommunity = False
















