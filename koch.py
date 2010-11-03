import random

# TODO: configure these
minWordLength = 1
maxWordLength = 5

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
    words = generateKochWords(5, "aiklmoprstuw")
    import play
    play.play(words)

