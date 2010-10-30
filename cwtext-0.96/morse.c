/* morse.c - morse code 'engine' for cwtext
Copyright (C) 2001,2002 Randall S. Bohn

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

#include "cw.h"
#include "morse.h"

extern void dit(FILE *);
extern void dah(FILE *);
extern void err(FILE *);
extern void cspace(FILE *);
extern void wspace(FILE *);

/* returns the index of char c in string s */
int strpos(const char *s, char c) {
 int x = 0;
 while (s[x] != 0) {
  if (s[x] == c) return x;
  x++;
 }
 return -1;
}

/* get the code for char c. -1 if not found. */
char getCode(char c) {
 char place = strpos(plain, c);
 if (place >= 0) return code[place];
 else return -1;
}
/* generate morse code equivalent for each character */
void genMorse(char c, FILE *out) {
 char position, start, size, x;
 position = getCode(c);
 if (position != -1) {
  start = position & CWSTARTMASK;
  size = (position >> CWSIZESHIFT) & CWSIZEMASK;

  for (x = 0; x < size; x++) {
   char c = crypt[start+x];
   if (c == '.') dit(out);
   if (c == '-') dah(out);
  }
 } else {
  err(out);
 }
 //cspace(out);
}

/* prosign support by Steve Conklin http://www.morseresource.com */
void translate(FILE *in, FILE *out) {
 int prosign = 0;
 int ch;

 while ((ch = fgetc(in)) != EOF) {
  if (ch == '*') {
   prosign = !prosign;
   if (!prosign) cspace(out);
  } else {
   if (isspace(ch)) wspace(out);
   else {
    genMorse(tolower(ch), out);
    if (!prosign) cspace(out);
   }
  }
 }
}

