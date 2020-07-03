import sys

def initBottle(levelNum):
    global bottle, bottleWidth, bottleHeight
    bottleWidth = 8
    bottleHeight = 16
    initVirusData(levelNum)
    bottle = [[None for i in range(bottleWidth)] for j in range(bottleHeight)]

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
    seed = (seed * 5 + 28947) % 65536
    virusPos = (seed + 1) % (virusRows*bottleWidth)
    return virusPos

#given an index into the bottle, return row number
def rowPos(virusIndex):
    return virusIndex // 8

#given an index into the bottle, return col number
def colPos(virusIndex):
    return virusIndex % 8

#returns True iff a virus in virusColor can be placed into position (row, col)
def validPos(virusIndex, virusColor):
    row = rowPos(virusIndex)
    col = colPos(virusIndex)
    #if the candidate cell is filled already
    if bottle[row][col] != None: return False
    return ( checkNeighbor(row+2,col,virusColor)
        and checkNeighbor(row-2,col,virusColor)
        and checkNeighbor(row,col-2,virusColor)
        and checkNeighbor(row,col+2,virusColor) )

#return True iff the neighbor cell does not have the same virus as virusColor
def checkNeighbor(neighborRow, neighborCol, virusColor):
    #if the neighbor is outside the bottle
    if (neighborRow >= bottleHeight or neighborRow < 0 or
        neighborCol >= bottleWidth or neighborCol < 0):
        return True
    return bottle[neighborRow][neighborCol] != virusColor

#given an index into the bottle
#return an empty cell's index
def findEmptyCell(virusIndex):
    foundEmpty = False
    while not foundEmpty:
        virusIndex=(virusIndex+1)%(virusRows*bottleWidth)
        # print(virusIndex)
        if bottle[rowPos(virusIndex)][colPos(virusIndex)] == None:
            foundEmpty = True
    # print(str(rowPos(virusIndex))+","+str(colPos(virusIndex)))
    return virusIndex

#add one virus to the bottle
def genVirus():
    global total
    global virusGoal, virusColor
    failed = 0
    currentIndex = randomIndex()
    initialIndex = currentIndex + 1

    #failed colors 

    while True:
        currentIndex = findEmptyCell(currentIndex)
        #if we have scanned thru bottle and couldnt find an empty spot
        if currentIndex == initialIndex:
            failed += 1
            if failed >= 3:
                virusGoal = 0
                return None
            virusColor=(virusColor+1)%3
        #we have found an empty spot at virusIndex
        else:
            if validPos(currentIndex,virusColor):
                failed = 0
                bottle[rowPos(currentIndex)][colPos(currentIndex)] = virusColor
                # print("viruspos "+str(rowPos(virusIndex))+","+str(colPos(virusIndex))+", color is "+str(virusColor))
                virusColor=(virusColor+1)%3
                virusGoal-=1
                total+=1
                return None
    # while True:
    #     current

def fillBottle():
    while virusGoal > 0:
        genVirus()

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


seed = 0x074e
initBottle(21)
virusColor = 0
total = 0
fillBottle()
print(total)
printBottle()
