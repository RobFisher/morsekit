#!/bin/bash
# Play morse on a mac
echo $1 | cwtext-0.96/cwpcm -w 20 -F 15 -lowrez | sox -b8 -u -r8000 -traw - -t raw /dev/dsp lowpass 1500

