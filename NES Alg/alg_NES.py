
import sys    # command-line arguments
import random # generating a random seed

VIRUS_LEVEL = 20 
REM_VIRUSES = (VIRUS_LEVEL + 1) * 4 

bottle_start = 16
bottle = []

data = []

#Initialization 
def byteToBinary(byte):
	# decimal valure to binary bit list 
	data =  [int(b) for b in bin(byte)[2:]]

	#padding if less than 16 bits 
	zeros = 16 - len(byte)
	data = zeros*[0] + data 

#LSFR
def LSFR():
	# tap bit 7 and bit 15
	bit9 = data[6]
	bit1 = data[14]
	newbit = bit1 ^ bit9

	# rotate in the new output bit
	data = [newbit] + data[0:15]



def generate_virus(): 
	maxRow = [
		0x9,0x9,0x9,0x9,0x9,0x9,0x9,
		0x9,0x9,0x9,0x9,0x9,0x9,0x9,
		0x9,0xA,0xA,0xB,0xB,0xC,0xC,
		0xC,0xC,0xC,0xC,0xC,0xC,0xC,
		0xC,0xC,0xC,0xC,0xC,0xC,0xC
	]
	virusPosTable = [
		0x78,0x70,0x68,0x60,0x58,0x50,0x48,0x40,
		0x38,0x30,0x28,0x20,0x18,0x10,0x08,0x00
	]
	virusTypeTable = [0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,1]
	bit_tbl = [1,2,4,0]

	while True: 
		LSFR()
		rowIndex = data[0] & 0xF 
		if maxRow[VIRUS_LEVEL] > rowIndex: 
			break 

	virus_pos = virusPosTable[rowIndex] + (data[1] & 7) 

	virusType = REM_VIRUSES & 3
	if virusType == 3: 
		LSFR()
		virus_type = virusTypeTable[data[1] & 0xF]

	
