/* cwtext.c - text to International Morse Code converter 
Copyright (C) 2001 Randall S. Bohn

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
#include "morse.h"

/* morse-speak: */
void dit(FILE *out) {
 fputc('.', out);
}
void dah(FILE *out) {
 fputc('-', out);
}
void err(FILE *out) {
 fputc('x', out);
}

void cspace(FILE *out) {
 fputc(' ', out);
}
void wspace(FILE *out) {
 cspace(out);
}

int main(int argc, char **argv) {
 int ch, x;
 FILE *out = stdout;

/*
 while ((ch = fgetc(stdin)) != EOF) {
  if (isspace(ch)) wspace(out);
  else genMorse(tolower(ch), out);
 }
*/
 translate(stdin, out);

 fputc('\n', out);
 fflush(out);
 return 0;
}
