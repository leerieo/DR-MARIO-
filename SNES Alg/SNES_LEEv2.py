#CELL 
CELL_EMPTY = "."
CELL_WALL = "#"
CELL_REDVIRUS = "R"
CELL_YELLOWVIRUS = "Y"
CELL_BLUEVIRUS = "B"

#BOTTLE
BOTTLE_WIDTH = 10
BOTTLE_HEIGHT = 18
MATRIX_WIDTH = 16

#VIRUS COLORS 
VIRUS_RED =  0 
VIRUS_YELLOW = 1 
VIRUS_BLUE = 2 
NUMVIRUSTYPES = 3  

#GAME MODES 
PLAYERSMODE_SINGLE = 0
PLAYERSMODE_VERSUS = 1
PLAYERSMODE_2 = 2

#PLAYER1 + PLAYER2 
NUMPLAYERS = 2

def cellVirusType(cell):
    if cell == CELL_REDVIRUS:
        return VIRUS_RED
    if cell == CELL_YELLOWVIRUS:
        return VIRUS_YELLOW
    if cell == CELL_BLUEVIRUS:
        return VIRUS_BLUE

MAXVIRUSGENATTEMPTS = 4
MAXVIRUSLEVEL = 29

CurrentPlayersMode = PLAYERSMODE_SINGLE


def levelMaxRow(level):
    if level <= 14: 
        return 10 
    elif level <= 16: 
        return 11 
    elif level <= 18: 
        return 12
    else: 
        return 13 


# Where to put the next virus, all positions in memory where a virus can be stored
NextVirusPosTable = [
	#BASE (CELL WALLS)

#0	#ROW 1 					#9 
	#1, 2, 3, 4, 5, 6, 7, 8, 

	#ROW2
#10								   #19
	11, 12, 13, 14, 15, 16, 17, 18, 

	#ROW3 
#20									#29 
	21, 22, 23, 24, 25, 26, 27, 28, 

	#ROW4 
#30								   #39
	31, 32, 33, 34, 35, 36, 37, 38, 

	#ROW5
#40								   #49
	41, 42, 43, 44, 45, 46, 47, 48,  

	#ROW6
#50								   #59
	51, 52, 53, 54, 55, 56, 57, 58, 

	#ROW7
#60								   #69
	61, 62, 63, 64, 65, 66, 67, 68,  

	#ROW8
#70 							   #79
	71, 72, 73, 74, 75, 76, 77, 78, 

	#ROW9
#80								   #89
	81, 82, 83, 84, 85, 86, 87, 88, 

	#ROW10 
#90							   	   #99 
	91, 92, 93, 94, 95, 96, 97, 98, 

	#ROW11
#100										#109
	101, 102, 103, 104, 105, 106, 107, 108, 

	#ROW12
#110										#119 
	111, 112, 113, 114, 115, 116, 117, 118,  

	#ROW13
#120										#129 
	121, 122, 123, 124, 125, 126, 127, 128,  
	#ROW14
#130										#139
	131, 132, 133, 134, 135, 136, 137, 138, 
]

#Player Class 
class Player:
    def __init__(self):
        self.bottle = [CELL_EMPTY]*BOTTLE_HEIGHT*BOTTLE_WIDTH # Cell list
        self.setVirus  = False
        self.virusLevel = 0 #Level being played 
        #keep track of number of viruses in each type
        self.numViruses = [0]*NUMVIRUSTYPES #int list
        self.nextVirusType = 0 #integer, 0 (red), 1(yellow) or 2(blue)
        #if all rows are filled w viruses
        self.maxVirusLocs = 0 #max number of allowed virus given a level
        #self.occupiedVirusPosTable = [False] * ((BOTTLE_WIDTH - 2) * TOPVIRUSROW) #bool list
        self.numGenViruses = 0 #number of generated virus so far
        self.maxGenViruses = 0
        self.nextVirusPos = 0
        self.nextVirusPosIndex = 0
        self.lastVirusPosIndex = 0
        self.numVirusGenAttempts = 0

Players = [] #List of Players

#fill list with Player
for x in range(NUMPLAYERS):
    Players.append(Player())

#Player numbers 
PLAYER1 = 0
PLAYER2 = 1

#default
PlayerNum = 0

#Calculate the number of viruses to generate 
#Set the number of viruses generate to 0 
def InitNumGenViruses():

    Players[PlayerNum].maxGenViruses = levelMaxRow(Players[PlayerNum].virusLevel)* 4 + 4

    Players[PlayerNum].numGenViruses = 0

    print("PLAYER ",(PlayerNum+1)," InitNumGenViruses: maxGenViruses is set to ",Players[PlayerNum].maxGenViruses)


def InitGenVirusData():
	#Calculate total number of possible locations of viruses in a given level 
    print("PLAYER",(PlayerNum+1)," TOP ROW", levelMaxRow(Players[PlayerNum].virusLevel)) 
    Players[PlayerNum].maxVirusLocs = levelMaxRow(Players[PlayerNum].virusLevel)*8
    print("PLAYER ",(PlayerNum+1)," InitGenVirusData: maxVirusLocs is set to ",Players[PlayerNum].maxVirusLocs)


#generates a random number from a given seed
Seed = 0  

#Radomization Algorithm 
def Rand():
	global Seed 
	Seed = (Seed * 5 + 28947) % 65536

#Get the virus position from the table 
def SetVirusPos(playerNum):
	Players[playerNum].nextVirusPos = NextVirusPosTable[Players[playerNum].nextVirusPosIndex]
	#print("nextVirusPos",Players[playerNum].nextVirusPos)

#set nextVirusPosIndex to an unoccupied spot
def SetUnoccupiedVirusPos():
    #if nextVirusPosIndex is not allowed, start scanning for unoccupied spot from index 0
    spotFound = False
    while(not spotFound):
        Players[PlayerNum].nextVirusPosIndex += 1
		#if nextVirusPosIndex is greater than maxVirusLocs make the index 0 
        if Players[PlayerNum].nextVirusPosIndex >= (Players[PlayerNum].maxVirusLocs):
            Players[PlayerNum].nextVirusPosIndex = 0
		# if a pos index is not occupied, a location was found 
        # get bottle location and check if it's an empty location 
        bottleLoc = NextVirusPosTable[Players[PlayerNum].nextVirusPosIndex]
        if Players[PlayerNum].bottle[bottleLoc] == CELL_EMPTY:
            spotFound = True
    
    SetVirusPos(PlayerNum)

#Radomize the seed and find a random index 
def GenNextVirusPosIndex():
    Rand()
    #?: why plus 1
    Players[PlayerNum].nextVirusPosIndex = (Seed + 1) % Players[PlayerNum].maxVirusLocs
    #print("GenNextVirusPosIndex: nextVirusPosIndex: " + str(Players[PlayerNum].nextVirusPosIndex) + "\n")

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
    #red
	else: 
		Players[PlayerNum].numViruses[VIRUS_RED] += 1
		virusCell = CELL_REDVIRUS

	# Put cell in the bottle 
	Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] = virusCell
	Players[PlayerNum].setVirus = True
	Players[PlayerNum].numGenViruses += 1
	
	# Cycle to the next color 
	Players[PlayerNum].nextVirusType += 1
	if (Players[PlayerNum].nextVirusType >= NUMVIRUSTYPES):
		Players[PlayerNum].nextVirusType = 0

	#printBottle()



def checkNeighbor(virusPos): 
    return (virusPos < 0 or #outside the bottle 
        (virusPos >= len(Players[PlayerNum].bottle)) or #outside the bottle
        Players[PlayerNum].bottle[virusPos] == CELL_EMPTY or 
        Players[PlayerNum].bottle[virusPos] == CELL_WALL or 
        cellVirusType(Players[PlayerNum].bottle[virusPos]) != Players[PlayerNum].nextVirusType) # is diff color


#Check that no location 2 spaces away has the same color 
def ValidVirusPos():
    if (Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] == CELL_EMPTY):
        if (checkNeighbor(Players[PlayerNum].nextVirusPos + 20) and #up
            checkNeighbor(Players[PlayerNum].nextVirusPos - 20) and #down
            checkNeighbor(Players[PlayerNum].nextVirusPos + 2) and #right
            checkNeighbor(Players[PlayerNum].nextVirusPos - 2)): #left 
            return True
    
    return False



def GenVirus():
	#print(Players[PlayerNum].nextVirusType)

	#Player 2 index calculator 
	if (CurrentPlayersMode != PLAYERSMODE_SINGLE and
	Players[PLAYER1].virusLevel == Players[PLAYER2].virusLevel and PlayerNum != PLAYER1):
		Players[PlayerNum].nextVirusPosIndex = Players[PLAYER1].nextVirusPosIndex
		SetVirusPos(PlayerNum)
		SetVirus()
		#print(Players[PlayerNum].bottle)
		return None
	
	Players[PlayerNum].lastVirusPosIndex = 0xFF
	Players[PlayerNum].numVirusGenAttempts = 0
	GenNextVirusPosIndex()
	
	while True:
		SetUnoccupiedVirusPos()
		#print("GEN VIRUS LOOP VIRUS INDEX: ",Players[PlayerNum].nextVirusPosIndex)
		#print("GEN VIRUS LOOP VIRUS POS: ",Players[PlayerNum].nextVirusPos)
		if (Players[PlayerNum].nextVirusPosIndex == Players[PlayerNum].lastVirusPosIndex):
			Players[PlayerNum].numVirusGenAttempts = Players[PlayerNum].numVirusGenAttempts + 1
			
			if (Players[PlayerNum].numVirusGenAttempts >= MAXVIRUSGENATTEMPTS-1):
				Players[PlayerNum].maxGenViruses = Players[PlayerNum].numGenViruses + 1
				print("GOT STUCK GOT STUCK !!!!!!!!!!")
				return None
			#Change next color 
			else: 
				Players[PlayerNum].nextVirusType+=1
				if(Players[PlayerNum].nextVirusType>=NUMVIRUSTYPES):
					
					Players[PlayerNum].nextVirusType = VIRUS_RED
		else:
			
			if (Players[PlayerNum].lastVirusPosIndex == 0xFF):
				Players[PlayerNum].lastVirusPosIndex = Players[PlayerNum].nextVirusPosIndex
			if (ValidVirusPos()):
				Players[PlayerNum].numVirusGenAttempts = 0
				SetVirus()
				return None

				

#print the bottle 
def printBottle(playerNum): 
	res = ""
	counter = 0 
	temp = ""

	for c in range(len(Players[playerNum].bottle)): 
		if (Players[playerNum].bottle[c] == CELL_EMPTY):
				temp += "."
		elif (Players[playerNum].bottle[c] == CELL_WALL):
				temp += "#"
		elif (Players[playerNum].bottle[c] == CELL_REDVIRUS):
				temp += "R"
		elif (Players[playerNum].bottle[c] == CELL_YELLOWVIRUS):
				temp += "Y"
		elif (Players[playerNum].bottle[c] == CELL_BLUEVIRUS):
				temp += "B"
		counter+=1
		if counter == 10: 
			res = temp + "\n" + res
			temp = ""
			counter = 0
	
	print(res)


if __name__ == "__main__":


	CurrentPlayersMode = int(input("Player Mode: "))

	if CurrentPlayersMode == 0: 
		print("PLAYERSMODE_SINGLE")
	elif CurrentPlayersMode == 1: 
		print("PLAYERSMODE_VERSUS")
	else: 
		print("PLAYERSMODE_2")
	

	#CurrentPlayersMode = 0 
	Players[PLAYER1].virusLevel = int(input("PLAYER 1 Virus Level: "))
	Players[PLAYER2].virusLevel = Players[PLAYER1].virusLevel

	if CurrentPlayersMode == PLAYERSMODE_2: 
		Players[PLAYER2].virusLevel = int(input("PLAYER 2 Virus Level: "))

	Seed = 0x074E
	#Seed = input("Seed: ")

	#initialize the walls of the bottle for PLAYER1 
	for x in range(1, BOTTLE_WIDTH+1):
		Players[PLAYER1].bottle[x] = CELL_WALL

	for y in range(BOTTLE_HEIGHT):
		Players[PLAYER1].bottle[y*10] = CELL_WALL
		Players[PLAYER1].bottle[y*10+9] = CELL_WALL
	
	#initialize the walls of the bottle for PLAYER2

	if CurrentPlayersMode != PLAYERSMODE_SINGLE: 
		for x in range(1, BOTTLE_WIDTH+1):
			Players[PLAYER2].bottle[x] = CELL_WALL

		for y in range(BOTTLE_HEIGHT):
			Players[PLAYER2].bottle[y*10] = CELL_WALL
			Players[PLAYER2].bottle[y*10+9] = CELL_WALL
		

	InitNumGenViruses()
	InitGenVirusData()

	if CurrentPlayersMode == PLAYERSMODE_2: 
		PlayerNum = PLAYER2
		InitNumGenViruses()
		InitGenVirusData()
		Players[PLAYER2].maxGenViruses = Players[PLAYER1].maxGenViruses
		PlayerNum = PLAYER1
		

	

	# if CurrentPlayersMode == PLAYERSMODE_2: 
	# 	PlayerNum = PLAYER1
	# 	count1 = 0 
	# 	while count1 < Players[PLAYER1].maxGenViruses: 
	# 		GenVirus()
	# 		count1+=1
		
	# 	PlayerNum = PLAYER2
	# 	count2 = 0 
	# 	while count2 < Players[PLAYER2].maxGenViruses: 
	# 		GenVirus()
	# 		count2+=1
	# else: 

	count = 0 
	
	while count < Players[PLAYER1].maxGenViruses: 
		GenVirus()
		if CurrentPlayersMode != PLAYERSMODE_SINGLE: 
			PlayerNum = PLAYER2
			GenVirus()
			PlayerNum = PLAYER1
		count+=1
	

	print("PLAYER 1")
	print("------------------------------------------")
	print("PLAYER1 MAX GEN VIRUSES", Players[PLAYER1].maxGenViruses)
	print("PLAYER1 NUM GEN VIRUSES", Players[PLAYER1].numGenViruses)
	print(" ")
	printBottle(PLAYER1)
	if CurrentPlayersMode != PLAYERSMODE_SINGLE: 
		print("PLAYER 2")
		print("------------------------------------------")
		print("PLAYER2 MAX GEN VIRUSES", Players[PLAYER2].maxGenViruses)
		print("PLAYER2 NUM GEN VIRUSES", Players[PLAYER2].numGenViruses)
		printBottle(PLAYER2)	

    

