"""
Abdus Sattar Mia - 000394648
Dated: Nov 16, 2020

"""
from player import Player
import numpy as np
np.random.seed(1)

class Board:
    def __init__(self):
        # Indicate the color set or a stattion or a utility
        self.squareName = ['Go', 'Brown 1', 'Community Chest 1', 'Brown 2', 'Income Tax',
                     'Station 1', 'Sky 1', 'Chance 1', 'Sky 2', 'Sky 3',
                     'Jail', 'Pink 1', 'Utility 1', 'Pink 2', 'Pink 3',
                     'Station 2', 'Orange 1', 'Community Chest 2', 'Orange 2', 'Orange 3',
                     'Free Parking', 'Red 1', 'Chance 2', 'Red 2', 'Red 3',
                     'Station 3', 'Yellow 1', 'Yellow 2', 'Utility 2', 'Yellow 3',
                     'Go To Jail', 'Green 1', 'Green 2', 'Community Chest 3', 'Green 3',
                     'Station 4', 'Chance 3', 'Blue 1', 'Luxury Tax', 'Blue 2']

        # Actual name of the properties
        self.squareNameText = ['Go', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax',
                        'Reading Railroad', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue',
                        'Jail', 'St. Charles Place', 'Electric Company', 'States Avenue', 'Virginia Avenue',
                        'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Avenue', 'New York Avenue',
                        'Free Parking', 'Kentucky Avenue', 'Chance', 'Indiana Avenue', 'Illinois Avenue',
                        'B. & O. Railroad', 'Atlantic Avenue', 'Ventnor Avenue', 'Water Works', 'Marvin Gardens',
                        'Go To Jail', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue',
                        'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']

        # Property type: land or station or something else
        self.propertyType = ['no', 'land', 'no', 'land', 'no', 'station', 'land', 'no', 'land', 'land',
                          'no', 'land', 'utility', 'land', 'land', 'station', 'land', 'no', 'land', 'land',
                          'no', 'land', 'no', 'land', 'land', 'station', 'land', 'land', 'utility', 'land',
                          'no', 'land', 'land', 'no', 'land', 'station', 'no', 'land', 'no', 'land']

        # -1 indicates the property has no price
        self.propertyPrice = [-1, 60, -1, 60, -1, 200, 100, -1, 100, 120,
                           -1, 140, 150, 140, 160, 200, 180, -1, 180, 200,
                           -1, 220, -1, 220, 240, 200, 260, 260, 150, 280,
                           -1, 300, 300, -1, 320, 200, -1, 350, -1, 400]

        self.housePrice = [-1, 50, -1, 50, -1, -1, 50, -1, 50, 50,
                            -1, 100, -1, 100, 100, -1, 100, -1, 100, 100,
                            -1, 150, -1, 150, 150, -1, 150, 150, -1, 150,
                            -1, 200, 200, -1, 200, -1, -1, 200, -1, 200]

         # -1 indicates the property has no rent
        self.propertyRent = [-1, (2,10,30,90,160,250), -1, (4,20,60,180,320,450), -1,
                     (25,50,100,200), (6,30,90,270,400,550), -1, (6,30,90,270,400,550), (8,40,100,300,450,600),
                     -1, (10,50,150,450,625,750), (4*7,10*7), (10,50,150,450,625,750), (12,60,180,500,700,900),
                     (25,50,100,200), (14,70,200,550,750,950), -1, (14,70,200,550,750,950), (16,80,220,600,800,1000),
                     -1, (18,90,250,700,875,1050), -1, (18,90,250,700,875,1050), (20,100,300,750,925,1100),
                     (25,50,100,200), (22,110,330,800,975,1150), (22,110,330,800,975,1150), (4*7,10*7), (24,120,360,850,1025,1200),
                     -1, (26,130,390,900,1100,1275), (26,130,390,900,1100,1275), -1, (28,150,450,1000,1200,1400),
                     (25,50,100,200), -1, (35,175,500,1100,1300,1500), -1, (50,200,600,1400,1700,2000)]

        # 16 Chance cards
        self.chanceDeck = ['Advance to Go', 'Advance to Red 3', 'Advance to Pink 1',
                            'Advance to nearest utility', 'Advance to nearest station',
                            'Bank pays you', 'Get out of Jail Free', 'Go back 3 spaces',
                            'Go to Jail', 'Make general repairs', 'Pay fine',
                            'Advance to Station 1', 'Advance to Blue 2',
                            'Elected chairman', 'Loan matures', 'Won crossword']

        # 16 Community Chest cards
        self.communityDeck = ['Advance to Go', 'Bank error', 'Doctors fees',
                               'Sale of stock', 'Get out of Jail Free', 'Go to Jail',
                               'Fund matures', 'Tax refund', 'Birthday', 'Insurance matures',
                               'Hospital fees', 'School fees', 'Receive consultancy fee',
                               'Street repairs', 'Beauty contest', 'Inherit']


        # Shuffle the cards
        np.random.shuffle(self.chanceDeck)
        np.random.shuffle(self.communityDeck)

    # Bound position in range [0..39] for 40 spaces
    def bound(self, position):
        return position % 40

    # Simulate a turn of a player
    def turn(self, player):
        rollAgain = True

        while rollAgain:
            rollAgain = False
            # Always use jail free cards if in jail
            if player.isInJail:
                if player.isJailFreeChance:
                    player.updateJailFreeStatus('use', 'Chance')
                    self.chanceDeck.append('Get out of Jail Free')

                elif player.isJailFreeCommunity:
                    player.updateJailFreeStatus('use', 'Community')
                    self.communityDeck.append('Get out of Jail Free')

                player.updateJailStatus(False)
            # Roll dice
            diceValue = player.rollDice()

            # Go to jail if three times double value
            if player.doubleCounter == 3:
                player.resetDoubleCounter()
                player.updateJailStatus(True)
                newPosition = 10
            else:
                # Walk to an interim position
                interimPosition = self.bound(player.position + diceValue)
                # if in the Chance square
                if interimPosition in [7,22,36]:
                    newPosition = self.moveWithChance(player, interimPosition)
                #  if in Community Chest square
                elif interimPosition in [2,17,33]:
                    newPosition = self.moveWithCommunity(player, interimPosition)
                # if stepped on Go to Jail
                elif interimPosition == 30:
                    player.updateJailStatus(True)
                    newPosition = 10
                else:
                    newPosition = interimPosition

            # update and record position
            player.updatePosition(newPosition)

            # roll again only if it is a double and the player is not in jail
            if player.doubleCounter > 0 and not player.isInJail:
                rollAgain = True

    # Move along with a Chance card
    def moveWithChance(self, player, interimPosition):
        pick = self.chanceDeck.pop(0)

        if pick == 'Get out of Jail Free':
            player.updateJailFreeStatus('get', 'Chance')
        else:
            self.chanceDeck.append(pick)

        # Move to new position as stated in the card
        if pick == 'Advance to Go':
            return 0
        elif pick == 'Advance to Red 3':
            return 24
        elif pick == 'Advance to Pink 1':
            return 11
        elif pick == 'Advance to nearest utility':
            if interimPosition > 12 and interimPosition <= 28:
                return 28
            else:
                return 12
        elif pick == 'Advance to nearest station':
            if interimPosition > 5 and interimPosition <= 15:
                return 15
            elif interimPosition > 15 and interimPosition <= 25:
                return 25
            elif interimPosition > 25 and interimPosition <= 35:
                return 35
            else:
                return 5
        elif pick == 'Go back 3 spaces':
            return self.bound(interimPosition - 3)
        elif pick == 'Go to Jail':
            player.updateJailStatus(True)
            return 10
        elif pick == 'Advance to Station 1':
            return 5
        elif pick == 'Advance to Blue 2':
            return 39
        else:
            return interimPosition

    # Move along with a Community Chest card
    def moveWithCommunity(self, player, interimPosition):
        pick = self.communityDeck.pop(0)

        if pick == 'Get out of Jail Free':
            player.updateJailFreeStatus('get', 'Community')
        else:
            self.communityDeck.append(pick)

        # Move to new position as stated in the card
        if pick == 'Advance to Go':
            return 0
        elif pick == 'Go to Jail':
            player.updateJailStatus(True)
            return 10
        else:
            return interimPosition
