import random

# TODO: configure these
minWordLength = 1
maxWordLength = 5

# after X should be <BT> but don't know how to get that in cwtext. See NOTES.
order = "KMRSUAPTLOWI.NJEF0Y,VG5/Q9ZH38B?427C1D6X!="

def getLetters(numLetters):
    return order[0:numLetters]

def maxLetters():
    return len(order)

def generateKochWords(numWords, letters):
    random.seed()
    
    words = ""
    
    for w in range (0, numWords):
        wordLength = random.randrange(minWordLength, maxWordLength+1, 1)
        word = ""
        for x in range(0, wordLength):
            letterIndex = random.randrange(0, len(letters), 1)
            word += letters[letterIndex]
        if w != 0:
            words += " "
        words += word

    return words


if __name__ == "__main__":
    letters = getLetters(12)
    words = generateKochWords(5,letters)
    import play
    play.play(words)

