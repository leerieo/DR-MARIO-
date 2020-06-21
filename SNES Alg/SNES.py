#ENUMERATORS 
#MAY BE UNECESSARY IN PYTHON 

class Cell: 
    def __init__(self,status): 
        self.status = status 

        '''
            empty = 0x00,
            wall = 0x3A,
            red = 0x81,
            yellow = 0x82,
            blue = 0x83
        '''


bottleWidth = 10,
bottleHeight = 18,
matrixWidth = 16

VirusTypes = ["red","yellow","blue","numtypes"]

PlayersMode = ["PLAYERSMODE_SINGLE","PLAYERSMODE_VERSUS","PLAYERSMODE_2"]

PlayerIndex = ["PLAYER1","PLAYER2","NUMPLAYERS"]

# def cellVirusType(cell): ????????????

maxVirusGetAttempts = 4 
topVirusRow = 13 
maxVirusLevel = 29 

Temp = [] 

randDivisors = [
	# 0 ... 14
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	# 15 ... 16
	11, 11,
	# 17 ... 18
	12, 12,
	# 18 ... 29
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
        bottle = [] # Cell list 
        setVirus  = False 
        virusLevel = 0
        numViruses = [] #int list
        randDivisor = 0
        occupiedVirusPosTable = [] #bool list 
        numGenViruses = 0
        maxGenViruses = 0
        nextVirusPos = 0 
        nextVirusPosIndex = 0
        lastVirusPosIndex = 0
        numVirusGenAttempts = 0 

Players = [] #List of Players 
PlayerNum = 1 


def InitNumGenViruses(): 
    Players[PlayerNum].maxGenViruses = 23 if (Players[PlayerNum].virusLevel >= 23) else (Players[PlayerNum].virusLevel)
    Players[PlayerNum].maxGenViruses = Players[PlayerNum].maxGenViruses * 4 + 4 
    Players[PlayerNum].numGenViruses = 0


'''
void InitGenVirusData() {
	Players[PlayerNum].randDivisor =
		RandDivisors[
			Players[PlayerNum].virusLevel >= MAXVIRUSLEVEL ?
				MAXVIRUSLEVEL :
				Players[PlayerNum].virusLevel
		] << 3;

	Temp[0] = (BOTTLE_WIDTH - 2) * TOPVIRUSROW;
	for (size_t i = 0; Temp[0] != 0; i++, Temp[0]--) {
		Players[PlayerNum].occupiedVirusPosTable[i] = false;
	}

    void Rand() {
	Seed = Seed * UINT16_C(5) + UINT16_C(0x7113);
    }


    void SetVirusPos(PlayerIndex playerNum) {
	Players[playerNum].nextVirusPos = NextVirusPosTable[Players[playerNum].nextVirusPosIndex] + PlayerNum * sizeof(Player);
    }   
}
'''

def SetVirusPos(playerNum):
    Players[playerNum].nextVirusPos = NextVirusPosTable[Players[playerNum].nextVirusPosIndex]


