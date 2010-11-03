import sys
import os
import platform

operatingSystem = platform.system()

# TODO: call cwtext properly in a child process or something
# that we can interactively kill before it completes

def play(words):
    # splits up words and plays them one at a time.
    wordList = words.split()
    for word in wordList:
        playCharacters(word)

def playCharacters(characters):
    if operatingSystem == "Darwin":
        os.system("./mactest.sh " + characters)
    else:
        os.system("./lintest.sh " + characters)

def main(argv=None):
    if argv == None:
        argv = sys.argv
    play(argv[1])

if __name__ == "__main__":
    sys.exit(main())

