import sys
import difflib

text1 = "abccd"
text2 = "abcd"

def splitToLines(s):
    result = ""
    for n in range(0, len(s)):
        result += s[n] + '\n'
    return result

def compare(t1, t2):
    t1 = t1.upper().strip()
    t2 = t2.upper().strip()
    t1 = splitToLines(t1)
    t2 = splitToLines(t2)
    d = difflib.Differ()
    c = d.compare(t1, t2)
    return list(c)

def makeComparisonString(comparison):
    cs = ""
    for line in comparison:
        if line[2] != '\n':
            if line[0] == ' ':
                cs += line[2]
            else:
                cs += line[0]
                cs += line[2]
    return cs

def countMistakes(comparisonString):
    missedChar = -1
    mistakes = 0
    n = 0
    for c in comparisonString:
        if c == '+':
            # wrong characters appear as '-A+B' and only count as one mistake
            if missedChar != (n-2):
                mistakes = mistakes + 1
        if c == '-':
            mistakes = mistakes + 1
            missedChar = n
        n = n + 1
    return mistakes

def main():
    comparison = compare(sys.argv[1], sys.argv[2])
    cs = makeComparisonString(comparison)
    print cs
    print countMistakes(cs)

if __name__ == '__main__':
    main()
