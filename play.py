import sys
import os
import platform
import optparse

operatingSystem = platform.system()
speed = 20
farnsworth = 15

# TODO: call cwtext properly in a child process or something
# that we can interactively kill before it completes

def setSpeed(_speed, _farnsworth):
    global speed
    global farnsworth
    speed = _speed
    farnsworth = _farnsworth

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

    parser = optparse.OptionParser()
    parser.add_option('-s', '--speed', action='store', type='int', default=speed, help='Speed in words per minute')
    parser.add_option('-f', '--farnsworth', action='store', type='int', default=farnsworth, help='Farnsworth rate')
    (options, args) = parser.parse_args()
    setSpeed(options.speed, options.farnsworth)
    play(" ".join(args))

if __name__ == "__main__":
    sys.exit(main())
