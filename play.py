import sys
import os
import platform

operatingSystem = platform.system()
speed = 20
farnsworth = 15

# TODO: call cwtext properly in a child process or something
# that we can interactively kill before it completes

def play(words):
    # splits up words and plays them one at a time.
    wordList = words.split()
    for word in wordList:
        playCharacters(word)

def playCharacters(characters):
    command = 'echo "' + characters + '" | cwtext-0.96/cwpcm -w ' + str(speed) + ' -F ' + str(farnsworth) + ' -lowrez | sox -b8 -u -r8000'
    if operatingSystem == "Darwin":
        command += ' -traw - -t wav tmp.wav lowpass 1500'
        os.system(command)
        os.system('afplay tmp.wav')
        os.system('rm tmp.wav')
    else:
        command += ' -traw - -t raw /dev/dsp lowpass 1500'
        os.system(command)

def main(argv=None):
    if argv == None:
        argv = sys.argv
    play(argv[1])

if __name__ == "__main__":
    sys.exit(main())
