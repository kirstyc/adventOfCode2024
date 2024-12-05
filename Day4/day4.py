import logging 
import sys
import numpy as np

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.INFO)

class Q1():
    def __init__(self) -> None:
        self.data = ""
        self.word = ""
        self.lettersDict = {}

    def load_input(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            chars = [list(line) for line in lines]

            self.data = np.array(chars, dtype='<U1') # matrix of chars
    @classmethod
    def add(cls, coordinate1, coordinate2):
        return (coordinate1[0]+coordinate2[0], coordinate1[1]+ coordinate2[1])

    def searchWord(self, coordinate, direction, idx):
        if (idx > len(self.word)-1): # are we at the end of the word?
            logger.debug("Found word")
            return True
        checkCoordinate = Q1.add(coordinate,direction)
        letter = self.word[idx]
        if (checkCoordinate in self.lettersDict[letter]):
            # keep looking in this direction with the next letter
            return self.searchWord(checkCoordinate, direction, idx+1)
        else:
            return False

    def process(self, searchWord: str) -> int:
        self.word = searchWord
        # create a dict of coordinates for the letters of interest 
        self.lettersDict = {}
        for coordinates, letter in np.ndenumerate(self.data):
            if letter in searchWord:
                if letter in self.lettersDict:
                    self.lettersDict[letter].append(coordinates)
                else:
                    self.lettersDict[letter] = [coordinates]
        
        # find how many of these starting letters have the subsequent letter 
        startLetter = searchWord[0]
        directions = [(-1,-1), # NW 
                      (-1, 0), # North
                      (-1,1),  # NE
                      (0,-1),  # West
                      (0, 1),  # East
                      (1,-1),  # SW
                      (1,0),   # South
                      (1,1)    # SE
                      ]
        total = 0
        for coordinate in self.lettersDict[startLetter]:
            searchWordIdx = 0
            for direction in directions:
                if(self.searchWord(coordinate, direction, searchWordIdx+1)):
                    total += 1

        return total 
                

class Q2():
    def __init__(self, lettersDict) -> None:
        self.lettersDict = lettersDict

    def process(self):
        # Look for "MAS" in the shape of an X 
        # M S     M M     S S    S M
        #  A   or  A  or   A  or  A
        # M S     S S     M M    S M
        
        directionPairs = [[(-1,-1),(1,1)], # first diagonal
                        [(1,-1), (-1, 1)], # second diagonal
                        ]
        total = 0
        # start at "a"
        for start in self.lettersDict['A']:
            success = True
            for mod1, mod2 in directionPairs:
                found = False
                first = Q1.add(start, mod1)
                second = Q1.add(start, mod2)
                if first in self.lettersDict['M']:
                    if second in self.lettersDict['S']:
                        found = True
                elif first in self.lettersDict['S']:
                    if second in self.lettersDict['M']:
                        found = True
                success &= found # only true if found in both directions of the diagonal

            if (success):
                total += 1
        
        return total



def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process("XMAS")
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(q1.lettersDict)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
