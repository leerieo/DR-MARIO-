#ENUMERATORS
#MAY BE UNECESSARY IN PYTHON
#
# class Cell:
#     def __init__(self,status):
#         self.status = status
#
#         '''
#             empty = 0x00,
#             wall = 0x3A,
#             red = 0x81,
#             yellow = 0x82,
#             blue = 0x83
#         '''

CELL_EMPTY = 0x00
CELL_WALL = 0x3A
CELL_REDVIRUS = 0x81
CELL_YELLOWVIRUS = 0x82
CELL_BLUEVIRUS = 0x83

BOTTLE_WIDTH = 10
BOTTLE_HEIGHT = 18
MATRIX_WIDTH = 16

#VirusTypes = ["red","yellow","blue","numtypes"]
VirusTypes = [0,1,2] #corresponding to red, yellow, blue
NUMVIRUSTYPES = 3

#PlayersMode = ["PLAYERSMODE_SINGLE","PLAYERSMODE_VERSUS","PLAYERSMODE_2"]
#PlayersMode
PLAYERSMODE_SINGLE = 0
PLAYERSMODE_VERSUS = 1
PLAYERSMODE_2 = 2

#PlayerIndex = ["PLAYER1","PLAYER2","NUMPLAYERS"]
# PlayerNum = [0,1]
NUMPLAYERS = 2

# def cellVirusType(cell): ????????????
def cellVirusType(cell):
    if cell == CELL_REDVIRUS:
        return 0
    elif cell == CELL_YELLOWVIRUS:
        return 1
    elif cell == CELL_BLUEVIRUS:
        return 2

MAXVIRUSGENATTEMPTS = 4
TOPVIRUSROW = 13
MAXVIRUSLEVEL = 29

Temp = [0]*(BOTTLE_WIDTH - 2) * TOPVIRUSROW

 #the highest row with viruses allowed in each level
randDivisors = [
	# level 0 ... 14
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	# level 15 ... 16
	11, 11,
	# level 17 ... 18
	12, 12,
	# level 18 ... 29
	13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13
]

NextVirusPosTable = [
    0x101, 0x102, 0x103, 0x104, 0x105, 0x106, 0x107, 0x108,
	0xF1,  0xF2,  0xF3,  0xF4,  0xF5,  0xF6,  0xF7,  0xF8,
	0xE1,  0xE2,  0xE3,  0xE4,  0xE5,  0xE6,  0xE7,  0xE8,
	0xD1,  0xD2,  0xD3,  0xD4,  0xD5,  0xD6,  0xD7,  0xD8,
	0xC1,  0xC2,  0xC3,  0xC4,  0xC5,  0xC6,  0xC7,  0xC8,
	0xB1,  0xB2,  0xB3,  0xB4,  0xB5,  0xB6,  0xB7,  0xB8,
	0xA1,  0xA2,  0xA3,  0xA4,  0xA5,  0xA6,  0xA7,  0xA8,
	0x91,  0x92,  0x93,  0x94,  0x95,  0x96,  0x97,  0x98,
	0x81,  0x82,  0x83,  0x84,  0x85,  0x86,  0x87,  0x88,
	0x71,  0x72,  0x73,  0x74,  0x75,  0x76,  0x77,  0x78,
	0x61,  0x62,  0x63,  0x64,  0x65,  0x66,  0x67,  0x68,
	0x51,  0x52,  0x53,  0x54,  0x55,  0x56,  0x57,  0x58,
	0x41,  0x42,  0x43,  0x44,  0x45,  0x46,  0x47,  0x48
]


class Player:
    def __init__(self):
        self.bottle = [CELL_EMPTY]*368 # Cell list
        self.setVirus  = False
        self.virusLevel = 0
        #keep track of number of viruses in each type
        self.numViruses = [0]*NUMVIRUSTYPES #int list
        self.nextVirusType = 0 #integer, 0 (red), 1(yellow) or 2(blue)
        #if all rows are filled w viruses
        self.randDivisor = 0 #max number of allowed virus given a level
        self.occupiedVirusPosTable = [False] * ((BOTTLE_WIDTH - 2) * TOPVIRUSROW) #bool list
        self.numGenViruses = 0 #number of generated virus so far
        self.maxGenViruses = 0
        self.nextVirusPos = 0
        self.nextVirusPosIndex = 0
        self.lastVirusPosIndex = 0
        self.numVirusGenAttempts = 0

sizePlayer = 1608
Players = [] #List of Players
#fill list with Player
for x in range(NUMPLAYERS):
    Players.append(Player())

PLAYER1 = 0
PLAYER2 = 1

#default
PlayerNum = 0


def InitNumGenViruses():
    # Players[PlayerNum].maxGenViruses = 23 if (Players[PlayerNum].virusLevel >= 23) else (Players[PlayerNum].virusLevel)
    # Players[PlayerNum].maxGenViruses = Players[PlayerNum].maxGenViruses * 4 + 4
    # Players[PlayerNum].numGenViruses = 0

    if Players[PlayerNum].virusLevel >= 23:
        Players[PlayerNum].maxGenViruses = 23 * 4 + 4
    else:
        Players[PlayerNum].maxGenViruses = Players[PlayerNum].virusLevel * 4 + 4
    Players[PlayerNum].numGenViruses = 0
    print("InitNumGenViruses: maxGenViruses is set to " +
    str(Players[PlayerNum].maxGenViruses) + "\n")

def InitGenVirusData():
    if Players[PlayerNum].virusLevel >= MAXVIRUSLEVEL:
        Players[PlayerNum].randDivisor = randDivisors[MAXVIRUSLEVEL]*8
    else:
        Players[PlayerNum].randDivisor = randDivisors[Players[PlayerNum].virusLevel]*8
    Temp[0] = (BOTTLE_WIDTH - 2) * TOPVIRUSROW #8*13
    #set all possible position of a virus to NOT occupied
    for i in range(Temp[0]):
        Players[PlayerNum].occupiedVirusPosTable[i] = False
    print("InitGenVirusData: randDivisor is set to " +
    str(Players[PlayerNum].randDivisor) + "\n")

#generates a random number from a given seed
def Rand(Seed):
    Seed = Seed * 5 + 28947
    print("Seed is " + str(Seed))

def SetVirusPos(playerNum):
    Players[playerNum].nextVirusPos = NextVirusPosTable[Players[playerNum].nextVirusPosIndex]+sizePlayer*playerNum

#set nextVirusPosIndex to an unoccupied spot
def SetUnoccupiedVirusPos():
    #if nextVirusPosIndex is not allowed, start scanning for unoccupied spot from index 0
    if Players[PlayerNum].nextVirusPosIndex >= (Players[PlayerNum].randDivisor-1):
        Players[PlayerNum].nextVirusPosIndex = 0
    while Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex]:
        Players[PlayerNum].nextVirusPosIndex += 1
    SetVirusPos(PlayerNum)

def GenNextVirusPosIndex():
    Rand(Seed)
    #?: why plus 1
    Players[PlayerNum].nextVirusPosIndex = (Seed + 1) % Players[PlayerNum].randDivisor
    print("GenNextVirusPosIndex: nextVirusPosIndex: " + str(Players[PlayerNum].nextVirusPosIndex) + "\n")

def SetVirus():
    #set a cell to appro status
    #yellow
    if Players[PlayerNum].nextVirusType == VIRUS_YELLOW:
        Players[PlayerNum].numViruses[VIRUS_YELLOW] += 1
        virusCell = CELL_YELLOWVIRUS
    #blue
elif Players[PlayerNum].nextVirusType == VIRUS_BLUE:
        Players[PlayerNum].numViruses[VIRUS_BLUE] += 1
        virusCell = CELL_BLUEVIRUS
    else: #red
        Players[PlayerNum].numViruses[VIRUS_RED] += 1
        virusCell = CELL_REDVIRUS

    Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] = virusCell
    Players[PlayerNum].setVirus = True
    Players[PlayerNum].numGenViruses += 1
    Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex] = True

    if (Players[PlayerNum].nextVirusType >= NUMVIRUSTYPES-1):
        Players[PlayerNum].nextVirusType = 0

#all directions that we have to check
VIRUSCHECKDIR_UP = 0
VIRUSCHECKDIR_DOWN = 1
VIRUSCHECKDIR_LEFT = 2
VIRUSCHECKDIR_RIGHT = 3
VIRUSCHECKDIR_ALLVALID = 4

def ValidVirusPos():
    if Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] == 0x00:
        Temp[0] = VIRUSCHECKDIR_UP
        while True:
            if Temp[0] == VIRUSCHECKDIR_UP:
                virusPos = Players[PlayerNum].nextVirusPos - MATRIX_WIDTH * 2
            elif Temp[0] == VIRUSCHECKDIR_DOWN:
                virusPos = Players[PlayerNum].nextVirusPos + MATRIX_WIDTH * 2
            elif Temp[0] == VIRUSCHECKDIR_LEFT:
                virusPos = Players[PlayerNum].nextVirusPos - 2
            elif Temp[0] == VIRUSCHECKDIR_RIGHT:
                virusPos = Players[PlayerNum].nextVirusPos + 2
            else:
                #WILL exit while loop
                return True
            if PlayerNum == PLAYER1:
                beyondEnd = (virusPos >= (BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + PLAYER1 * sizePlayer)
            else:
                beyondEnd = (virusPos >= (BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + PLAYER2 * sizePlayer)
            column = virusPos & 0xF
            if (beyondEnd or (column == 0) or (column >= BOTTLE_WIDTH - 1) or
                Players[PlayerNum].bottle[virusPos] == CELL_EMPTY or
                cellVirusType(Players[PlayerNum].bottle[virusPos]) != Players[PlayerNum].nextVirusType):
                Temp[0] += 1
                #loop back and check other directions
            else:
                return False
        #if this cell is not empty
        else:
            return False

def GenVirus():
    if (CurrentPlayersMode != PLAYERSMODE_SINGLE and
     Players[PLAYER1].virusLevel == Players[PLAYER2].virusLevel and PlayerNum != PLAYER1):
        Players[PlayerNum].nextVirusPosIndex = Players[PLAYER1].nextVirusPosIndex
        SetVirusPos(PlayerNum)
        SetVirus()
        print(Players[PlayerNum].bottle)
        return None

    Players[PlayerNum].lastVirusPosIndex = 0xFF
    Players[PlayerNum].numVirusGenAttempts = 0
    GenNextVirusPosIndex()
    while True:
        SetUnoccupiedVirusPos()
        if (Players[PlayerNum].nextVirusPosIndex == Players[PlayerNum].lastVirusPosIndex):
            if (Players[PlayerNum].numVirusGenAttempts >= MAXVIRUSGENATTEMPTS-1):
                Players[PlayerNum].maxGenViruses = Players[PlayerNum].numGenViruses + 1
                return None
            elif (Players[PlayerNum].nextVirusType >= NUMVIRUSTYPES-1):
                Players[PlayerNum].nextVirusType += 1
                Players[PlayerNum].nextVirusType = VIRUS_RED
        else:
            if (Players[PlayerNum].lastVirusPosIndex == 0xFF):
                Players[PlayerNum].lastVirusPosIndex = Players[PlayerNum].nextVirusPosIndex
            if (ValidVirusPos()):
                Players[PlayerNum].numVirusGenAttempts = 0
                SetVirus()
                return None

if __name__ == "__main__":
    for x in range(BOTTLE_WIDTH):
    	Players[PLAYER1].bottle[(BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + x] = CELL_WALL
    for y in range(BOTTLE_HEIGHT):
        Players[PLAYER1].bottle[y * MATRIX_WIDTH + 0] = CELL_WALL
        Players[PLAYER1].bottle[y * MATRIX_WIDTH + BOTTLE_WIDTH - 1] = CELL_WALL
    Players[PLAYER1].virusLevel = 20

    Seed = 0x3400
    CurrentPlayersMode = PLAYERSMODE_SINGLE

    InitNumGenViruses()
    InitGenVirusData()

    maxGenViruses = Players[PLAYER1].maxGenViruses
    for i in range(maxGenViruses):
        GenVirus()

    #print bottle
    # res = ""
    # for y in range(BOTTLE_HEIGHT):
    #     for x in range(BOTTLE_WIDTH):
    #         if (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x] == CELL_EMPTY):
    #             res += "."
    #         elif (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x] == CELL_WALL):
    #             res += "#"
    #         elif (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x] == CELL_REDVIRUS):
    #             res += "R"
    #         elif (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x] == CELL_YELLOWVIRUS):
    #             res += "Y"
    #         elif (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x] == CELL_BLUEVIRUS):
    #             res += "B"
    #     res += "\n"
    # print(res)
