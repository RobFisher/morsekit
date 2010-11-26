import sys
import os
import platform
import optparse
import threading
import subprocess

operatingSystem = platform.system()
speed = 20
farnsworth = 15

# TODO: call cwtext properly in a child process or something
# that we can interactively kill before it completes

def setSpeed(_speed, _farnsworth=0):
    global speed
    global farnsworth
    speed = _speed
    if _farnsworth == 0:
        farnsworth = speed
    else:
        farnsworth = _farnsworth

def play(characters, callback=None):
    playThread = threading.Thread(target=playCharacters, args=(characters,callback,))
    playThread.start()

def playCharacters(characters, callback=None):
    command = 'echo "' + characters + '" | cwtext-0.96/cwpcm -w ' + str(speed) + ' -F ' + str(farnsworth) + ' -lowrez | ./sox-14.3.1/sox -b8 -u -r8000'
    if operatingSystem == "Darwin":
        command += ' -traw - -t wav /tmp/morsekit.wav lowpass 1500'
        os.system(command)
        os.system('afplay /tmp/morsekit.wav')
        os.system('rm /tmp/morsekit.wav')
    else:
        command += ' -traw - -t raw /dev/dsp lowpass 1500'
        subprocess.Popen(command, shell=True)
    if callback != None:
        callback()

def stop():
    # this is brutal; maybe there is a better way
    if operatingSystem == "Darwin":
        subprocess.Popen('killall afplay', shell=True)
    else:
        subprocess.Popen('killall sox', shell=True)

def main(argv=None):
    if argv == None:
        argv = sys.argv

    parser = optparse.OptionParser()
    parser.add_option('-s', '--speed', action='store', type='int', default=speed, help='Speed in words per minute')
    parser.add_option('-f', '--farnsworth', action='store', type='int', default=farnsworth, help='Farnsworth rate')
    (options, args) = parser.parse_args()
    setSpeed(options.speed, options.farnsworth)
    playCharacters(" ".join(args))

if __name__ == "__main__":
    sys.exit(main())
