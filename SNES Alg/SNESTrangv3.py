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

#given a cell, return a virustype based on the given cell type
#Assumes that a given cell is 2,3, or 4 
def CELLVIRUSTYPE(cell):
    if cell == CELL_REDVIRUS:
        return VIRUS_RED
    if cell == CELL_YELLOWVIRUS:
        return VIRUS_YELLOW
    if cell == CELL_BLUEVIRUS:
        return VIRUS_BLUE

#red, yellow, blue 
NUMVIRUSTYPES = 3

#The bottle should be 10x18 cells 
BOTTLE_WIDTH = 10
BOTTLE_HEIGHT = 18

#This will be used in the GenVirus() function 
#The function will try to place a virus in a location a maximum of three times before giving up and simply placing less viruses
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
#there is a separate bottle for each player
#This class keeps track of the location/color of the next virus to be placed 
class Player():
    def __init__(self):
        self.bottle = [CELL_EMPTY]*BOTTLE_WIDTH*BOTTLE_HEIGHT #an array of cells 
        self.virusLevel = 0 #current level 
        self.numViruses = [0]*NUMVIRUSTYPES 
        self.nextVirusType = 0 #starts with red
        self.topLevelVirusRow = 0 #number of possible cells a virus could be in
        self.occupiedVirusPosTable = [False]*((BOTTLE_WIDTH - 2) * TOPVIRUSROW) #keeps track of which nextVirusPosIndex are already occupied
        self.numGenViruses = 0 #number of generated viruses so far
        self.maxGenViruses = 0 #number of viruses we want to generate
        self.nextVirusPos = 0 #the index in the bottle to place new virus
        self.nextVirusPosIndex = 0 #the index in the nextVirusPosTable to get the nextVirusPos
        self.lastVirusPosIndex = 0 #the previous index used
        self.numFailedVirusGenAttempts = 0 #Number of attempts to place a virus so far

PLAYER1 = 0
PLAYER2 = 1
NUMPLAYERS = 2

Players = [0]*NUMPLAYERS
#fill in list of Players
for x in range(NUMPLAYERS):
    Players[x] = Player()

#Calculate the number of viruses to generate in the bottle 
def InitNumGenViruses():
    #the maximum number of viruses that can be generated is 23*4+4
    if Players[PlayerNum].virusLevel >= 23:
        Players[PlayerNum].maxGenViruses = 23*4+4
    else:
        Players[PlayerNum].maxGenViruses = Players[PlayerNum].virusLevel*4+4

    #Set the number of viruses generate to 0 
    Players[PlayerNum].numGenViruses = 0

#Calculate total number of possible locations of viruses in a given level (Based on a level's top row)
def InitGenVirusData():
    #use the topLevelVirusRow table to find the top row
    #the highest row is 13 (see topLevelVirusRow table)
    if Players[PlayerNum].virusLevel >= MAXVIRUSLEVEL:
        Players[PlayerNum].topLevelVirusRow = topLevelVirusRows[MAXVIRUSLEVEL]*8
    else:
        Players[PlayerNum].topLevelVirusRow = topLevelVirusRows[Players[PlayerNum].virusLevel]*8
    #initialize all the potential virus locations as unoccupied 
    for x in range((BOTTLE_WIDTH - 2) * TOPVIRUSROW):
        Players[PlayerNum].occupiedVirusPosTable[x] = False

#Rand function 
def Rand():
    global Seed
    Seed = (Seed * 5 + 28947) % 65536

#get the bottle location from the nextVirusPosTable 
def SetVirusPos(playerNum):
    #indexed into the possible positions of a virus
    Players[playerNum].nextVirusPos = nextVirusPosTable[Players[playerNum].nextVirusPosIndex]

#set nextVirusPosIndex to an unoccupied spot
def SetUnoccupiedVirusPos():
    foundUnoccupied = False
    while not foundUnoccupied:
        #while an unoccupied spot is not found increment the index 
        Players[PlayerNum].nextVirusPosIndex+=1
        #if nextVirusPosIndex is greater than the max row, start scanning for unoccupied spot from index 0
        if Players[PlayerNum].nextVirusPosIndex >= Players[PlayerNum].topLevelVirusRow:
            Players[PlayerNum].nextVirusPosIndex = 0
		# if a pos index is not occupied, a location was found 
        if not Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex]:
            foundUnoccupied = True
    
    SetVirusPos(PlayerNum)

#Radomize the seed and find a random index 
def GenNextVirusPosIndex():
    Rand()
    Players[PlayerNum].nextVirusPosIndex = (Seed + 1) % Players[PlayerNum].topLevelVirusRow

#create a new cell with the appropriate color and place it in the bottle 
def SetVirus():
    #set a cell to appro status
    if Players[PlayerNum].nextVirusType == VIRUS_YELLOW:
        Players[PlayerNum].numViruses[VIRUS_YELLOW]+=1
        virusCell = CELL_YELLOWVIRUS
    elif Players[PlayerNum].nextVirusType == VIRUS_BLUE:
        Players[PlayerNum].numViruses[VIRUS_BLUE]+=1
        virusCell = CELL_BLUEVIRUS
    else:
        Players[PlayerNum].numViruses[VIRUS_RED]+=1
        virusCell = CELL_REDVIRUS
    #add to bottle 
    Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] = virusCell
    Players[PlayerNum].numGenViruses+=1
    #set location to occupied 
    Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex] = True

    #consider next virus type in list red, yellow, blue
    #NOTE: the very first color considered is red
    Players[PlayerNum].nextVirusType = (Players[PlayerNum].nextVirusType+1)%NUMVIRUSTYPES

#used in ValidVirusPos 
def _checkNeighbor(virusPos):
    #is neighbor outside of bottle?
    beyondEnd = (virusPos >= (BOTTLE_HEIGHT - 1) * BOTTLE_WIDTH)
    #is the virusPos is divisible by 10 it is a wall 
    column = virusPos % 10

    #if the location is empty, a wall, or a different color return true (valid)
    return ( (beyondEnd or
    column == 0 or column == BOTTLE_WIDTH - 1 #is neighbor a cell wall?
    or Players[PlayerNum].bottle[virusPos] == CELL_EMPTY 
    or CELLVIRUSTYPE(Players[PlayerNum].bottle[virusPos]) != Players[PlayerNum].nextVirusType) )

def ValidVirusPos():
    valid = False
    #any space 2 spaces away from nextVirusPos must not have the same color 
    if (Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] == CELL_EMPTY):
        valid = (_checkNeighbor(Players[PlayerNum].nextVirusPos - BOTTLE_WIDTH * 2) and #up
            _checkNeighbor(Players[PlayerNum].nextVirusPos + BOTTLE_WIDTH * 2) and #down
            _checkNeighbor(Players[PlayerNum].nextVirusPos - 2) and #left
            _checkNeighbor(Players[PlayerNum].nextVirusPos + 2) ) #right
    return valid

#Generates a virus 
def GenVirus():
    #used to check if the virus was correctly placed 
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
    #Level is hard coded
    Players[PLAYER1].virusLevel = 21
    # Players[PLAYER2].virusLevel = 10
    # if CurrentPlayersMode != PLAYERSMODE_SINGLE and Players[PLAYER1].virusLevel == Players[PLAYER2].virusLevel and PlayerNum != PLAYER1:
    #     print("The two bottles for both players are the same: ")

    #initialize the walls of the bottle 
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
    #This doesn't work for me for some reason -JENN 
    '''
    if sys.argv[:2] != "0x":
        print("usage: python SNESTrangv3.py <hexSeed>")
        print("e.g. python SNESTrangv3.py 0x3400")
        exit()
    s = sys.argv[1][2:]
    
    Seed = int(s, 16)
    '''

    Seed = 0x3400
    CurrentPlayersMode = PLAYERSMODE_SINGLE
    PlayerNum = PLAYER1
    main()


