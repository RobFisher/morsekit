import sys
import random
import optparse

# after X should be <BT> but don't know how to get that in cwtext. See NOTES.
order = "KMRSUAPTLOWI.NJEF0Y,VG5/Q9ZH38B?427C1D6X!="

def getLetters(numLetters):
    return order[0:numLetters]

def maxLetters():
    return len(order)

def generateKochWords(numWords, letters, minWordLength=1, maxWordLength=8):
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


def main(argv=None):
    if argv == None:
        argv = sys.argv

    parser = optparse.OptionParser()
    parser.add_option('-n', '--numletters', action='store', type='int', default=2, help='Number of different letters to train with')
    parser.add_option('-w', '--words', action='store', type='int', default=5, help='Number of words to play')
    parser.add_option('-s', '--speed', action='store', type='int', default=0, help='Speed in words per minute')
    parser.add_option('-f', '--farnsworth', action='store', type='int', default=0, help='Farnsworth rate')
    parser.add_option('--minwordlength', action='store', type='int', default=1, help='Minimum word length')
    parser.add_option('--maxwordlength', action='store', type='int', default=8, help='Maximum word length')
    parser.add_option('--letters', action='store', type='string', default=None, help='List of letters to train with')
    (options, args) = parser.parse_args()

    letters = options.letters
    if letters == None:
        letters = getLetters(options.numletters)

    words = generateKochWords(options.words, letters, options.minwordlength, options.maxwordlength)
    import play
    if options.speed > 0:
        if options.farnsworth == 0:
            play.setSpeed(options.speed)
        else:
            play.setSpeed(options.speed, options.farnsworth)
            
    play.play(words)

if __name__ == "__main__":
    main()
