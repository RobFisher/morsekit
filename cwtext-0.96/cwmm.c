/* cwpcm.c - text to International Morse Code converter 
Copyright (C) 2001-2003 Randall S. Bohn

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
/* cwmm - output XML morse code compatible with MorseMail. See
http://www.seanet.com/~harrypy/MorseMail/ for details. */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "morse.h"
/*#include "pcm.h"*/

/* to match MM we'll call a 1wpm dit=1188 msec mark, 1188 msec space */
#define tbase 1188

/* rates (character, word) for various speeds (slow|med|fast|extra) */
#define CSLOW 15
#define WSLOW 5
#define CMED 18
#define WMED 12
#define CFAST 18
#define WFAST 18
#define CEXTRA 20
#define WEXTRA 20

#define MMREADER "<readerURL>\nhttp://www.seanet.com/~harrypy/MorseMail/\n</readerURL>\n"

/* storage for space time (hi) */
int spaceAccumulator = 0;
/* dit time for characters, spaces */
int cTime, sTime;

int getCharacterTime(int c_rate) {
	return tbase/c_rate;
}
int getSpaceTime(int c_rate, int w_rate) {
	int t_total;
	int t_chars;
	int t_space;

	if (w_rate < 5) w_rate = 5;
	/* you can slow down the spaces, but you can't speed up.
	   if word rate > character rate just use character rate.
	 */
	if (w_rate >= c_rate) return getCharacterTime(c_rate);

	/* spaces take longer but how much longer? */
	/* there are 50 units in 'PARIS '
	   36 are in the characters,
	   14 are in the spaces. */
	t_total = getCharacterTime(w_rate) * 50;
	t_chars = getCharacterTime(c_rate) * 36;

	/* this is how long all the spaces take */
	t_space = t_total - t_chars;
	/* this is how long one space should take */
	return t_space / 14;
}


/* morsemail xml support */
void openMorseMail(FILE *out) {
 fputs("<MorseMail>", out);
 fputs(VERSION, out);
 fputs("\n", out); /* not mac friendly... */
}

void closeMorseMail(FILE *out) {
 fputs("</MorseMail>\n", out);
}

void addReaderInfo(FILE *out) {
 fputs(MMREADER, out);
}

/* morsemail mark and space */
/* have to save up spaces and just put out one,
	morsemail doesn't like having two spaces in a row.
	So, accumulate spaces, put the total time out before
	each mark. Be sure to call finish(out) to emit the
	final space (you will have final space!) */
void mark(int duration, FILE *out) {
 if (spaceAccumulator > 0) {
  fprintf(out, "%+d", -spaceAccumulator);
  spaceAccumulator = 0;
 }
 fprintf(out, "%+d", duration);
}
void space(int duration, FILE *out) {
 spaceAccumulator += duration;
}

void setup() {
 spaceAccumulator = 0;
}
void finish(FILE *out) {
 if (spaceAccumulator > 0) {
  fprintf(out, "%+d", -spaceAccumulator);
 }
 fputs("\n", out);
 fflush(out);
}

/* morse-speak: */
void dit(FILE *out) {
 mark(cTime, out);
 space(cTime, out);
}
void dah(FILE *out) {
 mark(cTime * 3, out);
 space(cTime, out);
}
void err(FILE *out) {
}

void cspace(FILE *out) {
 space(sTime*2, out);
}
void wspace(FILE *out) {
 space(sTime*4, out);
}


int getInt(char *s, int low, int high) {
	int ival;
	char *temp = malloc(6);

	if (s == NULL) return low;
	strncpy(temp, s, 5);
	if (strlen(s) > 5) *(temp+5) = '\0';
	ival = atoi(temp);
	free(temp);
	if (ival < low) return low;
	if (ival > high) return high;
	return ival;
}

int main(int argc, char **argv) {
 int ch, x;
 int cwpm;
 int wwpm;
 FILE *out = stdout;

 /* start the rates at zero */
 wwpm = 0;
 cwpm = 0;


 /* decode startup options */
 for (x = 1; x < argc; x++) {
  if (strncmp(argv[x], "-ss", 3)==0) {
   cwpm = CSLOW;
   wwpm = WSLOW;
  }
  if (strncmp(argv[x], "-sm", 3)==0) {
   cwpm = CMED;
   wwpm = WMED;
  }
  if (strncmp(argv[x], "-sf", 3)==0) {
   cwpm = CFAST;
   wwpm = WFAST;
  }
  if (strncmp(argv[x], "-sx", 3)==0) {
   cwpm = CEXTRA;
   wwpm = WEXTRA;
  }
  /* set the word rate wpm (cwpm also if not set) */
  if (ARG_IS("-w")) {
   if (++x < argc) {
    wwpm = getInt(argv[x], 5, 100);
    if (cwpm == 0) cwpm = wwpm;
   }
   continue;
  }
  if (ARG_IS("-F")) {
   if (++x < argc) cwpm = getInt(argv[x], 5, 100);
   continue;
  }


 }

 /* no speed set on command line? */
 if (cwpm == 0) cwpm = CFAST;
 if (wwpm == 0) wwpm = CFAST;
 cTime = getCharacterTime(cwpm);
 sTime = getSpaceTime(cwpm, wwpm);

 openMorseMail(out);
 setup();
/*
 while ((ch = fgetc(stdin)) != EOF) {
  if (isspace(ch)) wspace(out);
  else genMorse(tolower(ch), out);
 }
*/
 translate(stdin, out);

 finish(out);
 closeMorseMail(out);
 addReaderInfo(out);
 fflush(out);
 return 0;
}
