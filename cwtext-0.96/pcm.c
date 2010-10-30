/*
cwpcm - pcm audio generator for cwtext
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

#include <math.h>
#include <stdio.h>

#include "pcm.h"

			   //#define VERBOSE

#define voxref(n) (vox[n-1])
#define PI 3.14159
#define TWOPI 6.28

typedef struct voice {
 /* frequency is cycles/sample */
 float frequency;
 int samplerate;
 int amplitude;
 int risesamples; // in samples
 int fallsamples; // in samples
 int ZERO;
 // next three use to track attack and decay
 int fallsamplesremaining;
 int falloffset;
 int offset;
} tVoice;

// allocate three voices
tVoice vox[MAXVOX];
int voxmap[MAXVOX] = {0,0,0};

int valid(int hvox) {
 if (hvox > MAXVOX) return 0;
 if (hvox < 1) return 0;
 if (voxmap[hvox-1] == 0) return 0;
 return 1;
}

int mStoSamples(int hVox, int time) {
  // time in mS
  float timelen;
  float samples;
  float fsr;
  
  if (!valid(hVox)) return;

  timelen = (float) time;
  fsr = (float) voxref(hVox).samplerate;

  samples = (fsr / 1000.0) * timelen;
#ifdef VERBOSE
  fprintf(stderr, "mStoSamples: hvox=%d, time=%d, samples=%d\n", hVox, time, (int) samples);
  fflush(stderr);
#endif
  return (int) samples;
}
 
unsigned char wavepoint(int hvox, int pos, float gain) {
  float tv;
  float tv2;
  unsigned char retval;
  tv = gain * sin((float)pos*TWOPI*(float)voxref(hvox).frequency);

  tv2 = ((float) voxref(hvox).amplitude * tv) + (float) voxref(hvox).ZERO;

  retval = (unsigned char) tv2;
#ifdef VERBOSE
  fprintf(stderr, "wavepoint: %d from tv=%f, tv2 = %f, pos=%d, amp=%d, gain=%f\n",
	  retval, tv, tv2, pos, voxref(hvox).amplitude, gain);
  fflush(stderr);
#endif
  return retval;
}

char zeropoint(int hvox) {
 return voxref(hvox).ZERO;
}

void mark(int hvox, int duration, FILE *out) {
  int x;
  int sample;
  int part;
  float gain;

  if (!valid(hvox)) return;

  //
  // We're emulating a transmitter, so duration includes risetime and
  // hold time, but not falltime

  // Risetime
  sample = 0;

  if (duration < voxref(hvox).risesamples)
    part = duration;
  else
    part = voxref(hvox).risesamples;

  for (x=0; x <= part; x++) {
    gain = 0.5 + (-0.5 * cos((PI * sample)/voxref(hvox).risesamples));
    fputc(wavepoint(hvox, sample, gain), out);
    sample++;
  }
  duration = duration - part;

  // done with risetime, do middle part (if any)
  for (x=0; x <= duration; x++) {
    fputc(wavepoint(hvox, sample, 1.0), out);
    sample++;
  }
  
  voxref(hvox).fallsamplesremaining = voxref(hvox).fallsamples;
  voxref(hvox).offset = sample;
  voxref(hvox).falloffset = 0;
}

void space(int hvox, int duration, FILE *out) {
  int x;
  int part;
  float gain;

  if (!valid(hvox)) return;

  if (duration < voxref(hvox).fallsamples)
    part = duration;
  else
    part = voxref(hvox).fallsamples;

  while (duration) {
    if(voxref(hvox).fallsamplesremaining) {
      // wer'e still in the falltime
      gain = 0.5 + (0.5 * cos((PI * voxref(hvox).falloffset)/voxref(hvox).fallsamples));
      fputc(wavepoint(hvox, voxref(hvox).offset, gain), out);
      voxref(hvox).offset++;
      voxref(hvox).fallsamplesremaining--;
      voxref(hvox).falloffset--;
    } else {
      // Done with the falltime
      fputc(zeropoint(hvox), out);
    }
    duration--;
  }
}

int setAmplitude(int hvox, int amp) {
 if (!valid(hvox)) return 0;
 voxref(hvox).amplitude = amp;
 return hvox;
}

int setRisetime(int hvox, int risetime) {
  // supplied in mS, convert to samples
  if (!valid(hvox)) return 0;
  voxref(hvox).risesamples = mStoSamples(hvox, risetime);
  return hvox;
}

int setFalltime(int hvox, int falltime) {
  if (!valid(hvox)) return 0;
  voxref(hvox).fallsamples = mStoSamples(hvox, falltime);
  return hvox;
}

int setFrequency(int hvox, int hz, int rate) {
 if (!valid(hvox)) return 0;
 /* if we can't give you the frequency we'll give the highest possible,
  * based on the sample rate */
 if (hz > rate/4) hz = rate/4;
 voxref(hvox).frequency = hz/(float)rate;
 return hvox;
}

int getFrequency(int hvox, int rate) {
  if (!valid(hvox)) return 0;
  /* convert samples/cycle to samples/sec */
  return voxref(hvox).frequency*rate;
}

int nextFreeVoice() {
 int x;
 for (x = 0; x < MAXVOX; x++) {
  if (voxmap[x] == 0) {
   voxmap[x] = 1;
   return x+1;
  }
 }
 return 0;
}

void freeVoice(int hvox) {
 if (valid(hvox)) {
  voxmap[hvox-1] = 0;
 }
}
int voiceFactory(int freq, int amplitude, int zero, int samplerate) {
  int hvox = nextFreeVoice();
#ifdef VERBOSE
  fprintf(stderr, "voiceFactory entered\n");
  fflush(stderr);
#endif
  if (hvox == 0) return 0;
  voxref(hvox).amplitude = amplitude;
  voxref(hvox).ZERO = zero;
  voxref(hvox).risesamples = mStoSamples(hvox, 10); // 10 mS
  voxref(hvox).fallsamples = mStoSamples(hvox, 10); // 10 mS
  voxref(hvox).samplerate = samplerate;
  setFrequency(hvox, freq, samplerate);
  return hvox;
}
