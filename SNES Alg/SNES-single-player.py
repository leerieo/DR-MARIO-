# Python implementation of the algorithm that generates viruses in Dr. Mario (SNES).
#
# This code is functionally the same as the original.
# For an implementation that is closer to the original game's 65C816 code,
# see nightmareci's C implementation.
# https://tetrisconcept.net/threads/dr-mario-virus-placement.2037/page-3

# BOTTLE:
# The filled bottle is represented as a list of cell rows.
# The rows are ordered in reverse order in comparison to the printed bottle.
# i.e. the bottom row of the printed bottle is the first element (or row) of the filled bottle
# In this implementation, the bottle refers to the filled bottle.
# CELL POSITION:
# Both (index) and (row, col) can be used to refer to a cell position in the filled bottle.

import sys
import random

# Create the 8 x 16 bottle to be filled
# Call the initVirusData function
def initBottle(levelNum):
    global bottle, bottleWidth, bottleHeight
    bottleWidth = 8
    bottleHeight = 17
    initVirusData(levelNum)
    #Create an array of arrays, each array in bottle is a row
    bottle = [[None for i in range(bottleWidth)] for j in range(bottleHeight)]

#Calculate virusGoal and virusRows based on a given level
def initVirusData(levelNum):
    global virusRows, virusGoal

    #number of viruses to be generated
    if levelNum >= 23: virusGoal = 23*4+4
    else: virusGoal = levelNum*4+4

    #number of rows where the viruses can be placed
    virusRows = 10
    if levelNum >= 15: virusRows += 1
    if levelNum >= 17: virusRows += 1
    if levelNum >= 19: virusRows += 1

#returns a random index into the bottle
def randomIndex():
    global seed, virusRows, bottleWidth
    seed = (seed * 5 + 28947) % 65536 #Randomization algorithm
    virusIndex = (seed + 1) % (virusRows*bottleWidth) #find a location within the possible virus positions
    return virusIndex

#given an index into the bottle, return row number
def rowPos(virusIndex):
    global bottleWidth
    return virusIndex // bottleWidth

#given an index into the bottle, return col number
def colPos(virusIndex):
    global bottleWidth
    return virusIndex % bottleWidth

#returns True iff a virus in virusColor can be placed into position (row, col)
#no location 2 squares away (in the up, down, left, right direction) can have the same virusColor
def validPos(virusIndex, virusColor):
    row = rowPos(virusIndex)
    col = colPos(virusIndex)
    #if the candidate cell is filled already
    if bottle[row][col] != None: return False
    return ( checkNeighbor(row+2,col,virusColor) #right
        and checkNeighbor(row-2,col,virusColor) #left
        and checkNeighbor(row,col-2,virusColor) #down
        and checkNeighbor(row,col+2,virusColor) ) #up

#return True iff the neighbor cell does not have the same virus as virusColor
def checkNeighbor(neighborRow, neighborCol, virusColor):
    #if the neighbor is outside the bottle return True
    if (neighborRow >= bottleHeight or neighborRow < 0 or
        neighborCol >= bottleWidth or neighborCol < 0):
        return True
    #if the neighbor is a different color return True
    return bottle[neighborRow][neighborCol] != virusColor

#given an index into the bottle, return an empty cell's index
def findEmptyCell(virusIndex):
    foundEmpty = False
    #scan to the end of bottle and loop back to find an empty cell
    #NOTE: this function assumes that the valid virus locations are never completely full.
    #Otherwise, the loop would run forever.
    while not foundEmpty:
        virusIndex=(virusIndex+1)%(virusRows*bottleWidth)
        #if a location in the bottle is unoccupied return the index
        if bottle[rowPos(virusIndex)][colPos(virusIndex)] == None:
            foundEmpty = True
    return virusIndex

#Place a virus in the bottle
def genVirus(virusRemain):
    global virusColor, bottle
    currentIndex = randomIndex()
    failed = 0 #keep track of the number of failed attempts
    initialIndex = 0xFF
    while True:
        currentIndex = findEmptyCell(currentIndex)
        #If we have scanned through bottle (got back to the beginning positiion)
        #and couldn't find a valid spot for this virus color,
        #cycle to another virus color
        #If there are no valid spots for any virus colors,
        #give up and generate fewer viruses than expected
        if currentIndex == initialIndex:
            failed += 1
            if failed >= 3:
                virusRemain = 0
                return virusRemain
            virusColor=(virusColor+1)%3
        else:
             #keep track of the intialIndex (i.e. first empty spot we found)
            if (initialIndex == 0xFF):
                initialIndex = currentIndex
            #we have found an empty spot at virusIndex
            if validPos(currentIndex,virusColor):
                failed = 0
                bottle[rowPos(currentIndex)][colPos(currentIndex)] = virusColor #place virus in the bottle
                virusColor=(virusColor+1)%3 #cycle to the next color
                virusRemain -= 1
                return virusRemain

#Call genVirus over and over
def fillBottle():
    global virusGoal
    #the number of viruses we still have to generate to meet the virus goal
    virusRemain = virusGoal
    while virusRemain > 0:
    # while virusGoal > 0:
        # nightmareci's comment:
        # The original code runs RealRand (a function that Rand calls) some random number of times
        # every frame.
        # Such calls to RealRand are ommited here, so this code can be compared to
        # the no-Rand-per-frame ROM hack.
        # The number of times RealRand is called is not governed by an explicit algorithm;
        # it just keeps running the randomizer after a frame has been updated,
        # so the number of times RealRand is run is proportional to how many CPU cycles remain after a frame update.
        # genVirus()
        virusRemain = genVirus(virusRemain)

#Print the bottle out
def printBottle():
    global bottle
    res = ""
    for row in reversed(bottle):
        res+="#"
        for value in row:
            if value == None: res+= "."
            if value == 0: res += "R"
            if value == 1: res += "Y"
            if value == 2: res += "B"
        res+="#"
        res+="\n"
    #bottom wall
    for _ in range(bottleWidth+2):
        res+="#"
    print(res)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage 1: python SNES-single-player.py <level> <hexSeed>")
        print("e.g. python SNES-single-player 21 0x3400")
        print("usage 2: python SNES-single-player.py <level>")
        print("the seed will be generated randomly")
        print("e.g. python SNES-single-player 21")
        exit()
    #if only the level is specified
    elif len(sys.argv) == 2:
        level = int(sys.argv[1])
        if (level > 29) or (level < 0):
            print("level number must be from 0 to 29")
        seed = random.randint(0,65535)
    #if a level is not specified, level is set to 20
    else:
        level = int(sys.argv[1])
        # if sys.argv[2][:2] != "0x":
        #     print("The seed is 16-bit and must be in heximal form (e.g. 0x3400, 0x28b8)")
        #     print("usage: python SNES-single-player.py <level> <hexSeed>")
        #     print("e.g. python SNES-single-player 21 0x3400")
        #     exit()
        # else:
        #     s = sys.argv[2][2
        s = sys.argv[2]
        seed = int(s, 16)

    #commented out so outputs can be compared
    # print("Level: "+ str(level))
    # print("Seed: "+ str(s))
    initBottle(level)
    virusColor = 0 #starts with red
    fillBottle()
    printBottle()
