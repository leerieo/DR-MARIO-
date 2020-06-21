#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>


#define VIRUS_LEVEL 20
//level 1 -> 4 viruses, level 2 -> 8 viruses, etc.
uint8_t REM_VIRUSES = (VIRUS_LEVEL + 1) * 4;

uint8_t color, location;

//???
size_t bottle_start = 16;
//alocatting 1 byte for each possible position in the bottle 
uint8_t bottle[20 * 8];

// https://stackoverflow.com/questions/111928/is-there-a-printf-converter-to-print-in-binary-format
#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"

//BYTE_TO_BINARY(byte)
// returns '100001011'  
#define BYTE_TO_BINARY(byte)  \
    // this will be = to 1 if the leftmost bit is = to 1 
    //   10101000
    // & 10000000
  (byte & 0x80 ? '1' : '0'), \ 
  (byte & 0x40 ? '1' : '0'), \
  (byte & 0x20 ? '1' : '0'), \
  (byte & 0x10 ? '1' : '0'), \
  (byte & 0x08 ? '1' : '0'), \
  (byte & 0x04 ? '1' : '0'), \
  (byte & 0x02 ? '1' : '0'), \
  (byte & 0x01 ? '1' : '0')

//LFSR  
void rotate_bytes(uint8_t * data, uint8_t len) {
	uint8_t carry_0 = 0, carry_1 = 0;
	uint8_t x = 0;

'''
    data[0] = 10101010      data[1] = 00001111
            & 00000010              & 00000010
        ----------------    -------------------

'''
	if (((data[0] & 2) ^ (data[1] & 2)) != 0) {
		carry_0 = 1;
		carry_1 = 1;
	}
'''
data = 100010010
data >> 1 
        010010001

00000000 << 7 

00000001 << 7 
10000000


(data >> 1) | (00000001 << 7) 
    01001001
   |10000000
   ----------
   11001001
'''
	for (x = 0; x < len; x++) {
		carry_0 = data[x] & 1;
		data[x] = (carry_1 << 7) | data[x] >> 1;
		carry_1 = carry_0;
	}
}

//place one virus 
void generate_virus(uint8_t * seed) {
	uint8_t virus_pos_tbl_index;
	uint8_t virus_type;
	uint8_t virus_pos;
	uint8_t surrounding_viruses;
    // maximum row for given level 
	uint8_t virus_level_tbl[] = {
		0x9,0x9,0x9,0x9,0x9,0x9,0x9,
		0x9,0x9,0x9,0x9,0x9,0x9,0x9,
		0x9,0xA,0xA,0xB,0xB,0xC,0xC,
		0xC,0xC,0xC,0xC,0xC,0xC,0xC,
		0xC,0xC,0xC,0xC,0xC,0xC,0xC
	};
	uint8_t virus_pos_tbl[] = {
		0x78,0x70,0x68,0x60,0x58,0x50,0x48,0x40,
		0x38,0x30,0x28,0x20,0x18,0x10,0x08,0x00
	};
	uint8_t virus_type_tbl[] = {0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,1};
	uint8_t bit_tbl[] = {1,2,4,0};


    //find a spot to put a random virus at 
    // give me random vals until (virus_pos_tbl_index = seed[0] & 0xF) is a usuable row 
	//seed[0] & 0xF chopps value down to num btwn 0 and 15 
	do {
		rotate_bytes(seed, 2); 
	} while (virus_level_tbl[VIRUS_LEVEL] < (virus_pos_tbl_index = seed[0] & 0xF));
	virus_pos = virus_pos_tbl[virus_pos_tbl_index] + (seed[1] & 7);
    //check if virus is there? 
	virus_type = REM_VIRUSES & 3;
	if (virus_type == 3) {
		rotate_bytes(seed, 2);
		virus_type = virus_type_tbl[seed[1] & 0xF];
	}

	while (1) {
		if (bottle[bottle_start + virus_pos] == 0xFF)
			break;
try_again:
		if (++virus_pos >= 0x80)
			return;
	}

	surrounding_viruses = 0;
	surrounding_viruses |= bit_tbl[bottle[bottle_start + virus_pos - 16] & 3];
	surrounding_viruses |= bit_tbl[bottle[bottle_start + virus_pos + 16] & 3];
	if ((virus_pos & 7) >= 2)
		surrounding_viruses |= bit_tbl[bottle[bottle_start + virus_pos - 2] & 3];
	if ((virus_pos & 7) < 6)
		surrounding_viruses |= bit_tbl[bottle[bottle_start + virus_pos + 2] & 3];

	while (1) {
		if (surrounding_viruses == 7)
			goto try_again;
		if ((surrounding_viruses & bit_tbl[virus_type]) == 0)
			break;
		if (virus_type == 0)
			virus_type = 2;
		else
			virus_type--;
	}
    //set position to color of virus 

    // y  r  b 
    // D0 D1 D2
	bottle[bottle_start + virus_pos] = 0xD0 | virus_type;
	REM_VIRUSES--;
	//printf(""BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY(seed[0]));
	//printf(""BYTE_TO_BINARY_PATTERN"\n", BYTE_TO_BINARY(seed[1]));
}

int main(int argc, char ** argv) {
	size_t x, y;
	/* Be sure the seed is nonzero, or the virus generation function will
	 * loop endlessly. */
	uint8_t seed[2];
	unsigned int temp;

	if (argc < 2) {
		srand(time(NULL));
		seed[0] = rand();
		seed[1] = rand();
	}
	else {
		sscanf(argv[1], "%x", &temp);
		seed[0] = temp;
		sscanf(argv[2], "%x", &temp);
		seed[1] = temp;
	}
	printf("%02X, %02X\n", seed[0], seed[1]);

	/* The code judges 0xFF as an empty cell, so initialize the bottle here
	 * with 0xFF. */
	for (y = 0; y < 20; y++) {
		for (x = 0; x < 8; x++) {
			bottle[y*8 + x] = 0xFF;
		}
	}

	/* A call of generate_virus will fail sometimes, with REM_VIRUSES
	 * unchanged, so keep calling sub_9CFF until enough viruses have been
	 * generated.
	 * */
    //keep adding viruses until you run out 
	while (REM_VIRUSES > 0) {
		generate_virus(seed);
	}


    //print bottle function 
	/* The original 6502 code uses 0xD0, 0xD1, and 0xD2 for viruses, so
	 * code here must interpret the bytes properly.
	 *
	 * 0xD0 => Yellow virus
	 * 0xD1 => Red virus
	 * 0xD2 => Blue virus
	 * 0xFF => Empty cell */
	for (y = 2; y < 16 + 2; y++) {
		for (x = 0; x < 8; x++) {
			switch (bottle[y*8 + x]) {
			case 0xD0: putchar('Y'); break;
			case 0xD1: putchar('R'); break;
			case 0xD2: putchar('B'); break;
			case 0xFF: putchar('-'); break;
			}
		}
		putchar('\n');
	}

	return 0;

}