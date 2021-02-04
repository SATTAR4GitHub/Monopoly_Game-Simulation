"""
Abdus Sattar Mia - 000394648
Dated: Nov 24, 2020

"""
from player import Player
from board import Board
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getNRoundStat(noOfOpponents):
    roundMean, roundSTD = 33, 3
    return roundMean, roundSTD


## Game simulation
noOfGames = 1000000
opponents = []
noOfOpponents = 3
noOfWin = 0

oRev = 967
rRev = 1067
yRev = 1167
gRev = 1317
bRev = 1750

roundMean, roundSTD = getNRoundStat(noOfOpponents)

# Create opponents in a list
for _ in range(noOfOpponents):
    opponents.append(Player())

# Simulate 1,000,000 games
for i in range(round(noOfGames)):
    # Create a new board and clean each player's states
    board = Board()
    for player in opponents:
        player.newGame()

    # Simulate a random number of rounds per game
    nRound = np.random.normal(roundMean, roundSTD)
    for j in range(round(nRound)):
        # Simulate each turn for each player
        for player in opponents:
            board.turn(player=player)

    # Compute number of lnding and probability
    sCount = list(map(sum, zip(*[x.squareRecorder for x in opponents])))
    sProb = [ x/sum(sCount)*100 for x in sCount ]
    orangeProb=sProb[16]+sProb[18]+sProb[19]
    redProb=sProb[21]+sProb[23]+sProb[24]
    yellowProb=sProb[26]+sProb[28]+sProb[29]
    greenProb=sProb[31]+sProb[32]+sProb[34]
    blueProb=sProb[37]+sProb[39]
    # Compute revenue for each property
    orangeRev = round(orangeProb * oRev - 2060)
    redRev = round(redProb * rRev - 2930)
    yellowRev = round(yellowProb * yRev - 3050)
    greenRev = round(greenProb * gRev - 3920)
    blueRev = round(blueProb * bRev - 2750)

    maxValue = max([orangeRev,redRev,yellowRev,greenRev,blueRev])
    # Winning number of orange property
    if(maxValue == orangeRev):
        noOfWin += 1

# Print output
print("\nWin:" + str(round(noOfWin/noOfGames * 100, 2)) + "%" + "           Number of game won: " + str(noOfWin) +" out of " + str(noOfGames) +" games. \n")



##  Landing Probability: M-C simulation
# set property colours
def setColour(squareName):
    if 'Go' in squareName:
        return '#C2F7B7'
    elif 'Brown' in squareName:
        return '#8b4513'
    elif 'Sky' in squareName:
        return '#87ceeb'
    elif 'Pink' in squareName:
        return '#ca2c92'
    elif 'Orange' in squareName:
        return '#ffa500'
    elif 'Red' in squareName:
        return '#ff0000'
    elif 'Yellow' in squareName:
        return '#FFEC00'
    elif 'Green' in squareName:
        return '#27AE60'
    elif 'Blue' in squareName:
        return '#1F47BD'
    elif 'Station' in squareName:
        return '#999999'
    elif 'Utility' in squareName:
        return '#F3F1B6'
    elif 'Jail' in squareName:
        return '#000000'
    else: #chance and community chest
        return '#E3CDEC'

board = Board()
squareName, squareNameText = board.squareName, board.squareNameText

# Add square counts of all players
squareCount = list(map(sum, zip(*[x.squareRecorder for x in opponents])))
jailCount = list(map(sum, zip(*[x.jailRecorder for x in opponents])))


squareProb = [ x/sum(squareCount)*100 for x in squareCount ]
squareProb[10] = jailCount[1]/sum(squareCount)*100
squareColour = [setColour(squareName) for squareName in squareName]


# Add just visiting bar on top
justVisiting = [0] * 40
justVisiting[10] = jailCount[0]/sum(squareCount)*100
justVisiting_colour = ['#FACBB8'] * 40

plt.figure(figsize=(16,10))
bottom = plt.bar(squareName, squareProb, color=squareColour)
top = plt.bar(squareName, justVisiting, bottom=squareProb, color=justVisiting_colour)

plt.axhline(y=2.5,linewidth=1, color='k', linestyle='--')

plt.title(f'M-C Simulation for Landing Probability', fontsize=14)
plt.xticks(rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.25)
plt.xlabel('Board Space', fontsize=14)
plt.ylabel('Probability (%)', fontsize=14)
plt.legend((bottom[10], top[10]), ('In Jail', 'Just Visiting'), prop={'size':12})

# Save M-C simulation bar diagram as PNG file
plt.savefig('landing-probability.png', bbox_inches = "tight")


# Find top 10 visited squares
df = pd.DataFrame(zip(squareName, squareNameText,
                      [ x/sum(squareCount)*100 for x in squareCount ]),columns=['Property Type', 'Property Name', 'Probability%'] )

# Print top 10 visited squares
print("\nTop 10 visited properties:")
print("\n", df.sort_values(by=['Probability%'], ascending=False).head(10))



## Profit comparison for each property
def calculateCost(board, colour, nohouse):
    houses = [ hp for n, hp in zip(board.squareName, board.housePrice) if colour in n ]
    lands = [ lp for n, lp in zip(board.squareName, board.propertyPrice) if colour in n ]
    return np.array(houses) * nohouse + np.array(lands)

def calculateRent(board, colour, nohouse, whole_set=True):
    if nohouse > 0:
        assert whole_set == True, 'Incompatible arguments'
    if nohouse == 0 and whole_set:
        rent = [ r[nohouse]*2 for n, r in zip(board.squareName, board.propertyRent) if colour in n ]
    else:
        rent = [ r[nohouse] for n, r in zip(board.squareName, board.propertyRent) if colour in n ]
    return np.array(rent)

def getBreakevenPoint(board, colour, nohouse, squareProb):

    cost = calculateCost(board, colour, nohouse)
    rent = calculateRent(board, colour, nohouse)
    prob = [ p for n, p in zip(board.squareName, squareProb) if colour in n ]

    return cost.sum() / (rent * prob).sum()

noOfHouses = range(1,6)
colours = ['Sky','Pink','Orange', 'Red', 'Yellow', 'Green', 'Blue']
squareProb = [ x/sum(squareCount) for x in squareCount ]
station_prob_sum = sum([p for lt, r, p in zip(board.propertyType, board.propertyRent, squareProb) if lt == 'station'])

fig, ax = plt.subplots(1,3, figsize=(16,7))
for i, n_oppo in enumerate(range(1,4)):
    ax[i%3].set_xticks(noOfHouses)
    ax[i%3].set_title(f'{n_oppo+1}-Players Game')
    if i == 0:
        ax[i%3].set_ylabel('Expected Profit ($)', fontsize=14)
    if i == 1:
        ax[i%3].set_xlabel('Number of Houses, 5 Means Hotel', fontsize=14)
    for c in colours:
        breakeven_vec = np.array([getBreakevenPoint(board, c, nohouse, squareProb) for nohouse in noOfHouses])
        costVector = np.array([calculateCost(board, c, nohouse).sum() for nohouse in noOfHouses])
        profit = costVector / breakeven_vec * (getNRoundStat(n_oppo)[0] * n_oppo) - costVector
        ax[i%3].plot(noOfHouses, profit, color=setColour(c), linestyle='--', label=f'{c} Set')

    # All 4 stations
    profitAllStations = 200 * station_prob_sum * (getNRoundStat(n_oppo)[0] * n_oppo) - 200*4
    ax[i%3].plot(noOfHouses, [profitAllStations]*len(noOfHouses), color=setColour('Station'), linestyle='--', label='4 Stations')

ax[2].legend(loc='upper center', bbox_to_anchor=(-1.0, 1.0))

plt.savefig('profit-analysis.png')
plt.show()



































