import sys
import random
import platform
import os

# TODO: configure these
letters = "aiklmoprstuw"
minWordLength = 1
maxWordLength = 5
numWords = 20

random.seed()

operatingSystem = platform.system()

for w in range (0, numWords):
  wordLength = random.randrange(minWordLength, maxWordLength+1, 1)
  word = ""
  for x in range(0, wordLength):
    letterIndex = random.randrange(0, len(letters), 1)
    word += letters[letterIndex]

  # The gaps between words are already a bit too big.
  #word += " "

  # TODO: hitting ctrl-c does not work too well here
  if operatingSystem == "Darwin":
    os.system("./mactest.sh " + word)
  else:
    os.system("./lintest.sh " + word)

