/* cwpcm.h - audio generation for cwtext
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

#define MAXVOX (3)

void mark(int hvox, int duration, FILE *out);
void space(int hvox, int duration, FILE *out);
int setRisetime(int hvox, int risetime);
int setFalltime(int hvox, int falltime);
int setFrequency(int hvox, int hz, int rate);
int getFrequency(int hvox, int rate);
int setAmplitude(int hvox, int amp);
int voiceFactory(int hz, int amp, int zero, int samplerate);
void freeVoice(int hvox);

