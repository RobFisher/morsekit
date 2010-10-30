/* testpcm.c - test PCM code 
Copyright (C) 2004 Randall S. Bohn

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.  

*/
#include <stdio.h>
#include "pcm.h"

/* basic unit test definitions */
#define FAIL 1
#define PASS 0
int Fail(char *where) {
	printf("FAIL %s\n", where);
	return FAIL;
}

/* the tests */
#define ZEROBIAS 128
#define RATE 44100
int testFrequency() {
	int result = PASS;
	int hvox = voiceFactory(60, 64, ZEROBIAS, RATE);
	float freq;
	int hz;
	int voxFreq;
	/* look inside the box */
	for (freq = 60; freq < 3200; freq *= 1.1) {
		hz = (int) freq;
		setFrequency(hvox, hz, RATE);
		voxFreq = getFrequency(hvox, RATE);
		if (abs(hz - voxFreq) > 20) result = FAIL;
		printf("Test frequency: %i", hz);
		printf("\tVoice Frequency: %i", voxFreq);
		printf("\n");
	}

	freeVoice(hvox);
	return result;
}

int makeTone(int freq) {
	char *filename = "test_tone.raw";
	int hvox = voiceFactory(freq, 64, ZEROBIAS, RATE);
	FILE * out = fopen(filename, "w");
	mark(hvox, 1 * RATE, out);
	fclose(out);
	printf("Test tone of %d Hz created in %s\n", freq, filename);
	return 0;
}

int testAmplitudePct() {
	int x;
	for (x = 0; x <= 100; x+=5) {
		printf("%i %i %i\n", 
			x, 
			x*127/100, 
			128+x*127/100);
	}
} 

int main(int argc, char **argv) {

 if (testFrequency() > 0) Fail("testFrequency");

 makeTone(440);
 testAmplitudePct();
 return PASS;
}
