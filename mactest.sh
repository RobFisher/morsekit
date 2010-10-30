#!/bin/bash
# Play morse on a mac
echo $1 | cwtext-0.96/cwpcm -w 20 -F 15 -lowrez | sox -b8 -u -r8000 -traw - -t wav tmp.wav lowpass 1500
afplay tmp.wav
rm tmp.wav

