// This code is functionally the same as the original game's 65C816 code,
// rewritten in C.

// Comments like this
// Offset: 0x0000
// indicate the following data/function definition is located at the indicated
// memory offset in the original game.
// If the comment is on the end of a struct member, it's the offset from the
// start of the struct in the original game.

// Comments like this
// Size: 1
// indicate the number of bytes the data type takes up in the original game.

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <inttypes.h>

// Size: 1
typedef enum {
	CELL_EMPTY = 0x00,
	CELL_WALL = 0x3A,
	CELL_REDVIRUS = 0x81,
	CELL_YELLOWVIRUS = 0x82,
	CELL_BLUEVIRUS = 0x83
} Cell;

// Size: 1
typedef enum {
	VIRUS_RED,
	VIRUS_YELLOW,
	VIRUS_BLUE,
	NUMVIRUSTYPES
} VirusType;

#define CELLVIRUSTYPE(cell) ((VirusType)((cell & 3) - 1))

// Size: 1
typedef enum {
	BOTTLE_WIDTH = 10,
	BOTTLE_HEIGHT = 18,
	MATRIX_WIDTH = 16
} MatrixSize;

#define MAXVIRUSGENATTEMPTS 4

#define TOPVIRUSROW 13

#define MAXVIRUSLEVEL 29

// Offset: 0x0BB5
uint8_t Temp[2];

// Offset: 0x828234
uint8_t RandDivisors[MAXVIRUSLEVEL + 1] = {
	// 0 ... 14
	10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
	// 15 ... 16
	11, 11,
	// 17 ... 18
	12, 12,
	// 18 ... 29
	13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13
};

// Offset: 0x828252
size_t NextVirusPosTable[(BOTTLE_WIDTH - 2) * TOPVIRUSROW] = {
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
};

// Size: 1
typedef enum {
	PLAYERSMODE_SINGLE,
	PLAYERSMODE_VERSUS,
	PLAYERSMODE_2
} PlayersMode;
// Offset: 0x0B02
PlayersMode CurrentPlayersMode;

// Size: 0x500
typedef struct {
	Cell bottle[0x170]; // Offset: 0x000
	bool setVirus; // Offset: 0x20B
	uint8_t virusLevel; // Offset: 0x240
	uint8_t numViruses[NUMVIRUSTYPES]; // Offset: 0x267
	VirusType nextVirusType; // Offset: 0x27D
	uint8_t randDivisor; // Offset: 0x27E
	bool occupiedVirusPosTable[(BOTTLE_WIDTH - 2) * TOPVIRUSROW]; // Offset: 0x27F
	uint8_t numGenViruses; // Offset: 0x2E7
	uint8_t maxGenViruses; // Offset: 0x2E8
	size_t nextVirusPos; // Offset: 0x2E9
	uint8_t nextVirusPosIndex; // Offset: 0x2ED
	uint8_t lastVirusPosIndex; // Offset: 0x2EE
	uint8_t numVirusGenAttempts; // Offset: 0x2EF
} Player;

// Size: 1
typedef enum {
	PLAYER1,
	PLAYER2,
	NUMPLAYERS
} PlayerIndex;

// The original code had a variable better named PlayerOffset, that is the
// number of bytes offset from the start of the Players array for the player
// currently being processed. But, for cleaner C code, PlayerNum is used
// instead. PlayerOffset is at offset 0x0B00.
PlayerIndex PlayerNum;
// Offset: 0x0100
Player Players[NUMPLAYERS];

// Offset: 0x009E
uint16_t Seed;

void InitNumGenViruses() {
	Players[PlayerNum].maxGenViruses = (
		Players[PlayerNum].virusLevel >= 23 ?
			23 :
			Players[PlayerNum].virusLevel
	) * 4 + 4;
	Players[PlayerNum].numGenViruses = 0;
}

// Offset: 0x829765
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
}

// Offset: 0x808DBF
void Rand() {
	Seed = Seed * UINT16_C(5) + UINT16_C(0x7113);
}

// Offset: 0x829BDA
void SetVirusPos(PlayerIndex playerNum) {
	Players[playerNum].nextVirusPos = NextVirusPosTable[Players[playerNum].nextVirusPosIndex] + PlayerNum * sizeof(Player);
}

// Offset: 0x829BB7
void SetUnoccupiedVirusPos() {
	do {
		if (++Players[PlayerNum].nextVirusPosIndex >= Players[PlayerNum].randDivisor) {
			Players[PlayerNum].nextVirusPosIndex = 0u;
		}
	} while (Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex]);
	SetVirusPos(PlayerNum);
}

// Offset: 0x829BF1
void GenNextVirusPosIndex() {
	Rand();
	Players[PlayerNum].nextVirusPosIndex = (Seed + 1u) % Players[PlayerNum].randDivisor;
}

// Offset: 0x829C16
void SetVirus() {
	Cell virusCell;
	switch (Players[PlayerNum].nextVirusType) {
	default:
		Players[PlayerNum].numViruses[VIRUS_RED]++;
		virusCell = CELL_REDVIRUS;
		break;

	case VIRUS_YELLOW:
		Players[PlayerNum].numViruses[VIRUS_YELLOW]++;
		virusCell = CELL_YELLOWVIRUS;
		break;

	case VIRUS_BLUE:
		Players[PlayerNum].numViruses[VIRUS_BLUE]++;
		virusCell = CELL_BLUEVIRUS;
		break;
	}

	Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] = virusCell;
	Players[PlayerNum].setVirus = true;
	Players[PlayerNum].numGenViruses++;
	Players[PlayerNum].occupiedVirusPosTable[Players[PlayerNum].nextVirusPosIndex] = true;
	if (++Players[PlayerNum].nextVirusType >= NUMVIRUSTYPES) {
		Players[PlayerNum].nextVirusType = VIRUS_RED;
	}
}

// Size: 1
typedef enum {
	VIRUSCHECKDIR_UP,
	VIRUSCHECKDIR_DOWN,
	VIRUSCHECKDIR_LEFT,
	VIRUSCHECKDIR_RIGHT,
	VIRUSCHECKDIR_ALLVALID
} VirusCheckDirection;

// Offset: 0x82A7B9
bool ValidVirusPos() {
	if (Players[PlayerNum].bottle[Players[PlayerNum].nextVirusPos] == CELL_EMPTY) {
		Temp[0] = VIRUSCHECKDIR_UP;
		while (true) {
			size_t virusPos;
			switch (Temp[0]) {
			case VIRUSCHECKDIR_UP:
				virusPos = Players[PlayerNum].nextVirusPos - MATRIX_WIDTH * 2u;
				break;

			case VIRUSCHECKDIR_DOWN:
				virusPos = Players[PlayerNum].nextVirusPos + MATRIX_WIDTH * 2u;
				break;

			case VIRUSCHECKDIR_LEFT:
				virusPos = Players[PlayerNum].nextVirusPos - 2u;
				break;

			case VIRUSCHECKDIR_RIGHT:
				virusPos = Players[PlayerNum].nextVirusPos + 2u;
				break;

			case VIRUSCHECKDIR_ALLVALID:
			default: // The original game didn't have a default case and might crash in such a case.
				return true;
			}

			bool beyondEnd;
			if (PlayerNum == PLAYER1) {
				beyondEnd = virusPos >= (BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + PLAYER1 * sizeof(Player);
			}
			else {
				beyondEnd = virusPos >= (BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + PLAYER2 * sizeof(Player);
			}

			uint8_t column = virusPos & 0xF;
			// virusPos indexes player 1's bottle or player 2's.
			if (beyondEnd || column == 0u || column >= BOTTLE_WIDTH - 1u || Players->bottle[virusPos] == CELL_EMPTY || CELLVIRUSTYPE(Players->bottle[virusPos]) != Players[PlayerNum].nextVirusType) {
				Temp[0]++;
				continue;
			}
			return false;
		}
	}
	else {
		return false;
	}
}

// Offset: 0x829B46
void GenVirus() {
	if (CurrentPlayersMode != PLAYERSMODE_SINGLE && Players[PLAYER1].virusLevel == Players[PLAYER2].virusLevel && PlayerNum != PLAYER1) {
		Players[PlayerNum].nextVirusPosIndex = Players[PLAYER1].nextVirusPosIndex;
		SetVirusPos(PlayerNum);
		SetVirus();
		return;
	}

	Players[PlayerNum].lastVirusPosIndex = 0xFF;
	Players[PlayerNum].numVirusGenAttempts = 0u;
	GenNextVirusPosIndex();
	while (true) {
		SetUnoccupiedVirusPos();
		if (Players[PlayerNum].nextVirusPosIndex == Players[PlayerNum].lastVirusPosIndex) {
			if (++Players[PlayerNum].numVirusGenAttempts >= MAXVIRUSGENATTEMPTS) {
				Players[PlayerNum].maxGenViruses = Players[PlayerNum].numGenViruses;
				return;
			}
			else if (++Players[PlayerNum].nextVirusType >= NUMVIRUSTYPES) {
				Players[PlayerNum].nextVirusType = VIRUS_RED;
			}
		}
		else {
			if (Players[PlayerNum].lastVirusPosIndex == 0xFF) {
				Players[PlayerNum].lastVirusPosIndex = Players[PlayerNum].nextVirusPosIndex;
			}
			if (ValidVirusPos()) {
				Players[PlayerNum].numVirusGenAttempts = 0u;
				SetVirus();
				return;
			}
		}
	}
}

int main() {
	memset(Players, 0, sizeof(Players));
	for (int x = 0; x < BOTTLE_WIDTH; x++) {
		Players[PLAYER1].bottle[(BOTTLE_HEIGHT - 1) * MATRIX_WIDTH + x] = CELL_WALL;
	}
	for (int y = 0; y < BOTTLE_HEIGHT; y++) {
		Players[PLAYER1].bottle[y * MATRIX_WIDTH + 0] = CELL_WALL;
		Players[PLAYER1].bottle[y * MATRIX_WIDTH + BOTTLE_WIDTH - 1] = CELL_WALL;
	}
	Players[PLAYER1].virusLevel = 20;

	Seed = 0x3400;
	CurrentPlayersMode = PLAYERSMODE_SINGLE;
	InitNumGenViruses();
	InitGenVirusData();
	for (size_t i = 0, maxGenViruses = Players[PLAYER1].maxGenViruses; i < maxGenViruses; i++) {
		GenVirus();
		// The original code would run RealRand a pseudorandom number of times
		// (0 or greater) before the next call of GenVirus. Such calls of
		// RealRand are omitted here, so that this code can be compared to the
		// no-Rand-per-frame ROM hack.
	}

	for (int y = 0; y < BOTTLE_HEIGHT; y++) {
		for (int x = 0; x < BOTTLE_WIDTH; x++) {
			switch (Players[PLAYER1].bottle[y * MATRIX_WIDTH + x]) {
			case CELL_EMPTY: putchar('.'); break;
			case CELL_WALL: putchar('#'); break;
			case CELL_REDVIRUS: putchar('R'); break;
			case CELL_YELLOWVIRUS: putchar('Y'); break;
			case CELL_BLUEVIRUS: putchar('B'); break;
			}
		}
		putchar('\n');
	}

	return 0;
}
