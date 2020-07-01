import sys

#types of cells
CELL_EMPTY = 0
CELL_WALL = 1
CELL_REDVIRUS = 2
CELL_YELLOWVIRUS = 3
CELL_BLUEVIRUS = 4

#types of viruses
VIRUS_RED = 0
VIRUS_YELLOW = 1
VIRUS_BLUE = 2

#given a cell, return virustype
def CELLVIRUSTYPE(cell):
    if cell == CELL_REDVIRUS:
        return VIRUS_RED
    if cell == CELL_YELLOWVIRUS:
        return VIRUS_YELLOW
    if cell == CELL_BLUEVIRUS:
        return VIRUS_BLUE

NUMVIRUSTYPES = 3

BOTTLE_WIDTH = 10
BOTTLE_HEIGHT = 18

MAXVIRUSGENATTEMPTS = 3
#highest possible row for viruses for all levels = 13 (lvl 18-29)
TOPVIRUSROW = 13
MAXVIRUSLEVEL = 29

#highest possible row for viruses in different levels
topLevelVirusRows = [0]*(MAXVIRUSLEVEL + 1)
#fill in table
#level 0 - 14
for x in range(14):
    topLevelVirusRows[x] = 10
#level 15-16
topLevelVirusRows[15] = 11
topLevelVirusRows[16] = 11
#level 17-18
topLevelVirusRows[17] = 12
topLevelVirusRows[18] = 12
#level 19-29
for x in range(19,30):
    topLevelVirusRows[x] = 13

#8*13: indices of bottle where a virus can be added
# [WALL][WALL][WALL][WALL][WALL][WALL][WALL][WALL][WALL][WALL]
# [WALL] 161,  162,  163,  164,  165,  166,  167,  168, [WALL]
# [WALL] 151,  152,  153,  154,  155,  156,  157,  158, [WALL]
#   ....
# [WALL]  41,  42,   43,   44,   45,   46,   47,   48,  [WALL]
nextVirusPosTable = [0]*8*13
firstRow = [161, 162, 163, 164, 165, 166, 167, 168]
for x in range(8):
    nextVirusPosTable[x] = firstRow[x]
for i in range(8,(8*13)):
            nextVirusPosTable[i] = nextVirusPosTable[i-8]-10

#PlayersMode
PLAYERSMODE_SINGLE = 0
PLAYERSMODE_VERSUS = 1
PLAYERSMODE_2 = 2

#Player
class Player():
    def __init__(self):
        self.bottle = [CELL_EMPTY]*BOTTLE_WIDTH*BOTTLE_HEIGHT
        self.virusLevel = 0
        self.numViruses = [0]*NUMVIRUSTYPES #red
        self.nextVirusType = 0 #red
        self.topLevelVirusRow = 0 #number of possible cells a virus could be in
        self.occupiedVirusPosTable = [False]*((BOTTLE_WIDTH - 2) * TOPVIRUSROW)
        self.numGenViruses = 0 #number of generated viruses so far
        self.maxGenViruses = 0 #number of viruses we want to generate
        self.nextVirusPos = 0 #use index to index into NextVirusPosTable
        self.nextVirusPosIndex = 0
        self.lastVirusPosIndex = 0
        self.numFailedVirusGenAttempts = 0 #so far

PLAYER1 = 0
PLAYER2 = 1
NUMPLAYERS = 2

Players = [0]*NUMPLAYERS
#fill in list of Players
for x in range(NUMPLAYERS):
    Players[x] = Player()

def InitNumGenViruses():
    if Players[PlayerNum].virusLevel >= 23:
        Players[PlayerNum].maxGenViruses = 23*4+4
    else:
        Players[PlayerNum].maxGenViruses = Players[PlayerNum].virusLevel*4+4
    Players[PlayerNum].numGenViruses = 0

def InitGenVirusData():
    if Players[PlayerNum].virusLevel >= MAXVIRUSLEVEL:
        Players[PlayerNum].topLevelVirusRow = topLevelVirusRows[MAXVIRUSLEVEL]*8
    else:
        Players[PlayerNum].topLevelVirusRow = topLevelVirusRows[Players[PlayerNum].virusLevel]*8
    for x in range((BOTTLE_WIDTH - 2) * TOPVIRUSROW):
        Players[PlayerNum].occupiedVirusPosTable[x] = False

def Rand():
    global Seed
    Seed = (Seed * 5 + 28947) % 65536

def SetVirusPos(playerNum):
    #indexed into the possible positions of a virus
    Players[playerNum].nextVirusPos = nextVirusPosTable[Players[playerNum].nextVirusPosIndex]

def SetUnoccupiedVirusPos():
    foundUnoccupied = False
    while not foundUnoccupied:
        Players[PlayerNum].nextVirusPosIndex+=1
        if Players[PlayerNum].nextVirusPosIndex >= Players[PlayerNum].topLevelVirusRow:
            Players[PlayerNum].nextVirusPosIndex = 0
        if not Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex]:
            foundUnoccupied = True
    SetVirusPos(PlayerNum)

def GenNextVirusPosIndex():
    Rand()
    Players[PlayerNum].nextVirusPosIndex = (Seed + 1) % Players[PlayerNum].topLevelVirusRow

def SetVirus():
    if Players[PlayerNum].nextVirusType == VIRUS_YELLOW:
        Players[PlayerNum].numViruses[VIRUS_YELLOW]+=1
        virusCell = CELL_YELLOWVIRUS
    elif Players[PlayerNum].nextVirusType == VIRUS_BLUE:
        Players[PlayerNum].numViruses[VIRUS_BLUE]+=1
        virusCell = CELL_BLUEVIRUS
    else:
        Players[PlayerNum].numViruses[VIRUS_RED]+=1
        virusCell = CELL_REDVIRUS
    Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] = virusCell
    Players[PlayerNum].numGenViruses+=1
    Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex] = True

    #consider next virus type in list red, yellow, blue
    #NOTE: the very first color considered is red
    Players[PlayerNum].nextVirusType = (Players[PlayerNum].nextVirusType+1)%NUMVIRUSTYPES

def _checkNeighbor(virusPos):
    #is neighbor outside of bottle?
    beyondEnd = (virusPos >= (BOTTLE_HEIGHT - 1) * BOTTLE_WIDTH)

    column = virusPos % 10

    return ( (beyondEnd or
    column == 0 or column == BOTTLE_WIDTH - 1 #is neighbor a cell wall?
    or Players[PlayerNum].bottle[virusPos] == CELL_EMPTY
    or CELLVIRUSTYPE(Players[PlayerNum].bottle[virusPos]) != Players[PlayerNum].nextVirusType) )

def ValidVirusPos():
    valid = False
    if (Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] == CELL_EMPTY):
        valid = (_checkNeighbor(Players[PlayerNum].nextVirusPos - BOTTLE_WIDTH * 2) and #up
            _checkNeighbor(Players[PlayerNum].nextVirusPos + BOTTLE_WIDTH * 2) and #down
            _checkNeighbor(Players[PlayerNum].nextVirusPos - 2) and #left
            _checkNeighbor(Players[PlayerNum].nextVirusPos + 2) ) #right
    return valid

def GenVirus():
    #can be set to whatever value st >= 13*8
    #(13*8 is the max number of virus for the highest level)
    Players[PlayerNum].firstAttemptVirusPosIndex = 0xF
    Players[PlayerNum].numFailedVirusGenAttempts = 0
    GenNextVirusPosIndex()
    while True:
        SetUnoccupiedVirusPos()
        #scanned through all empty spots in bottle,
        #no valid pos for a virus of virusType - must change to another virusType
        if (Players[PlayerNum].nextVirusPosIndex == Players[PlayerNum].firstAttemptVirusPosIndex):
            Players[PlayerNum].numFailedVirusGenAttempts+=1
            #have tried with all 3 virusTypes
            #stop placing viruses
            if (Players[PlayerNum].numFailedVirusGenAttempts >= MAXVIRUSGENATTEMPTS):
                Players[PlayerNum].maxGenViruses = Players[PlayerNum].numGenViruses
                return None
            Players[PlayerNum].nextVirusType=(Players[PlayerNum].nextVirusType+1)%NUMVIRUSTYPES
        else:
            #stored the first position that we tried to place a virus of virusType
            if (Players[PlayerNum].firstAttemptVirusPosIndex == 0xF):
                Players[PlayerNum].firstAttemptVirusPosIndex = Players[PlayerNum].nextVirusPosIndex
            if (ValidVirusPos()):
                Players[PlayerNum].numFailedVirusGenAttempts = 0
                #NOTE: SetVirus also changed virusType
                SetVirus()
                return None

def main():
    Players[PLAYER1].virusLevel = 21
    # Players[PLAYER2].virusLevel = 10
    # if CurrentPlayersMode != PLAYERSMODE_SINGLE and Players[PLAYER1].virusLevel == Players[PLAYER2].virusLevel and PlayerNum != PLAYER1:
    #     print("The two bottles for both players are the same: ")

    for x in range(BOTTLE_WIDTH):
        #bottom wall of bottle
        Players[PlayerNum].bottle[(BOTTLE_HEIGHT - 1) * BOTTLE_WIDTH + x] = CELL_WALL
    for y in range(BOTTLE_HEIGHT):
        #left wall
        Players[PlayerNum].bottle[y * BOTTLE_WIDTH + 0] = CELL_WALL
        #right wall
        Players[PlayerNum].bottle[y * BOTTLE_WIDTH + BOTTLE_WIDTH - 1] = CELL_WALL

    InitNumGenViruses()
    InitGenVirusData()
    print("max gen virus is " + str(Players[PlayerNum].maxGenViruses))
    for i in range(Players[PlayerNum].maxGenViruses):
        GenVirus()

    #print bottle
    resBottle = ""
    total = 0
    for y in range(BOTTLE_HEIGHT):
        for x in range(BOTTLE_WIDTH):
            if Players[PlayerNum].bottle[y * BOTTLE_WIDTH + x] == CELL_EMPTY:
                resBottle+= "."
            elif Players[PlayerNum].bottle[y * BOTTLE_WIDTH + x] == CELL_WALL:
                resBottle+= "#"
            elif Players[PlayerNum].bottle[y * BOTTLE_WIDTH + x] == CELL_REDVIRUS:
                resBottle+= "R"
                total+=1
            elif Players[PlayerNum].bottle[y * BOTTLE_WIDTH + x] == CELL_YELLOWVIRUS:
                resBottle+= "Y"
                total+=1
            elif Players[PlayerNum].bottle[y * BOTTLE_WIDTH + x] == CELL_BLUEVIRUS:
                resBottle+= "B"
                total+=1
        resBottle+="\n"
    print(resBottle)
    print("Total number of virus is "+ str(total))

if __name__ == "__main__":
    if sys.argv[:2] != "0x":
        print("usage: python SNESTrangv3.py <hexSeed>")
        print("e.g. python SNESTrangv3.py 0x3400")
        exit()
    s = sys.argv[1][2:]
    Seed = int(s, 16)
    CurrentPlayersMode = PLAYERSMODE_SINGLE
    PlayerNum = PLAYER1
    main()
