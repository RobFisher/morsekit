/* cwpcm.c - text to International Morse Code converter 
Copyright (C) 2001-2007 Randall S. Bohn

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
/* envelope support by Steve Conklin http://www.morseresource.com */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "morse.h"
#include "pcm.h"


//#define SAMPLERATE 8000
#define SAMPLERATE 44100

#define RISETIME 10
#define FALLTIME 10

/* tbase (dit time in samples) is 1200 msec * 8 samples per msec */
//#define tbase 9600 // for 8000 Samples per second

/* 900 Hz */
#define PITCH 800
/* volume on 0..100 percent */
#define VOLUME 70

/* rates (character, word) for various speeds (slow|med|fast|extra) */
#define CSLOW 15
#define WSLOW 5
#define CMED 18
#define WMED 12
#define CFAST 18
#define WFAST 18
#define CEXTRA 20
#define WEXTRA 20

/* program settings */
int pcm = 1;
int hvox = 0;
/* character time, space time (in samples) */
int cTime, sTime;
/* sample rate (samples per second) */
int sample_rate=44100;

/* get the dit-time for characters */
int getCharacterTime(int c_rate) {
	// dit time is 1200 msec at 1 WPM
	// this returns the number of samples per dit
	// at the desired character rate
	float tbase = sample_rate/1000.0 * 1200;
	return (int)(tbase/c_rate);
}

/* get the dit-time for space between characters */
int getSpaceTime(int c_rate, int w_rate) {
	/* NONB helped with this section. Thanks Nate! */
	int t_total;
	int t_chars;
	int t_space;

	if (w_rate < 5) w_rate = 5;
	if (w_rate >= c_rate) return getCharacterTime(c_rate);

	/* spaces take longer but how much longer? */
	t_total = getCharacterTime(w_rate) * 50;
	t_chars = getCharacterTime(c_rate) * 36;

	t_space = t_total - t_chars;
	return t_space / 14;
}

/* morse-speak: */
void dit(FILE *out) {
 mark(hvox, cTime, out);
 space(hvox, cTime, out);
}
void dah(FILE *out) {
 mark(hvox, cTime * 3, out);
 space(hvox, cTime, out);
}
void err(FILE *out) {
}

void cspace(FILE *out) {
 space(hvox, sTime*2, out);
}
void wspace(FILE *out) {
 space(hvox, sTime*4, out);
 fflush(out);
}

void setupVoice(int hz, int amp) {
  /* freq, amplitude, zero, sample rate */
 hvox = voiceFactory(hz, amp, 128, sample_rate);
 setRisetime(hvox, RISETIME);
 setFalltime(hvox, FALLTIME);
}

int getInt(char *s, int low, int high) {
	int ival;
	char *temp = malloc(6);
	strncpy(temp, s, 5);
	if (strlen(s) > 5) *(temp+5) = '\0';
	ival = atoi(temp);
	free(temp);
	if (ival < low) return low;
	if (ival > high) return high;
	return ival;
}

int main(int argc, char **argv) {
 int ch, lastch, x, pitch, volume;
 int cwpm;
 int wwpm;
 int verbose = 0;
 int prosign = 0;

 pitch = PITCH;
 volume = VOLUME;
 cwpm = 0;
 wwpm = 0;
 /* decode startup options */
 for (x = 0; x < argc; x++) {
  if (ARG_IS("-ss")) {
   cwpm = CSLOW;
   wwpm = WSLOW;
  }
  if (ARG_IS("-sm")) {
   cwpm = CMED;
   wwpm = WMED;
  }
  if (ARG_IS("-sf")) {
   cwpm = CFAST;
   wwpm = WFAST;
  }
  if (ARG_IS("-sx")) {
   cwpm = CEXTRA;
   wwpm = WEXTRA;
  }
  if (ARG_IS("-f:")) {
   pitch = getInt(argv[x]+3, 40, 3200);
  } else if (ARG_IS("-f")) {
   if (++x < argc) {
    pitch = getInt(argv[x], 40, 3200);
   }
   continue;
  }
  if (ARG_IS("-vol:")) {
   volume = getInt(argv[x]+5, 0, 100);
  } else if (ARG_IS("-v")) {
   if (++x < argc) {
    volume = getInt(argv[x], 0, 100);
   }
   continue;
  }
  if (ARG_IS("-w")) {
   if (++x < argc) {
    wwpm = getInt(argv[x], 5, 100);
    if (cwpm == 0) cwpm = wwpm;
   }
   continue;
  }
  if (ARG_IS("-F")) {
   if (++x < argc)
    cwpm = getInt(argv[x], 5, 100);
   continue;
  }
  if (ARG_IS("-d")) {
   verbose=1;
  }
  if (ARG_IS("-lowrez")) {
   // cd quality rate
   sample_rate = 8000;
  }
 }
 /* speed not set? */
 if (cwpm == 0) cwpm = CFAST;
 if (wwpm == 0) wwpm = CFAST;

 cTime = getCharacterTime(cwpm);
 sTime = getSpaceTime(cwpm, wwpm);
 setupVoice(pitch, volume*127/100);
 // you might want to adjust falltime for high rates:
 // if (cwpm > 20) setFalltime(hvox, 0);



 if (verbose) {
   fprintf(stderr, "Pitch: %d Volume: %d%%\n", pitch, volume);
   fprintf(stderr, "WPM: %d Farnsworth: %d\n", wwpm, cwpm);
 }

 translate(stdin, stdout);
 return 0;
}
