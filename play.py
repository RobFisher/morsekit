import sys
import os
import platform

operatingSystem = platform.system()

def playCharacters(characters):
    # TODO: do this properly with a child process or something
    # that we can kill before it completes
    if operatingSystem == "Darwin":
        os.system("./mactest.sh " + characters)
    else:
        os.system("./lintest.sh " + characters)

def main(argv=None):
    if argv == None:
        argv = sys.argv
    playCharacters(argv[1])

if __name__ == "__main__":
    sys.exit(main())

