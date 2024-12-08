import logging 
import sys
from enum import Enum 

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod 
    def next(cls, dir):
        idx = dir.value+1
        if dir == Direction.LEFT:
            idx = 0 
        return Direction(idx)

    @classmethod
    def cursorToDir(cls, cursor):
        if cursor == "^":
            return Direction.UP
        elif cursor == "v":
            return Direction.DOWN
        elif cursor == ">":
            return Direction.RIGHT
        elif cursor == "<":
            return Direction.LEFT
        # none found 
        return None
    @classmethod
    def moveOneStep(cls, dir, posX, posY):
        # the (0,0) is top left and (row, col) is bottom right 
        if dir == Direction.UP:
            return [posX-1, posY] # subtract one to move up a row 
        elif dir == Direction.RIGHT:
            return [posX, posY+1]
        elif dir == Direction.DOWN:
            return [posX+1, posY]
        elif dir == Direction.LEFT:
            return [posX, posY-1]
        
class Q1():
    def __init__(self) -> None:
        self.rows = 0
        self.cols = 0 
        self.cursorPos = [-1,-1]
        self.obstacles = []
        self.direction = Direction.UP
        self.visited = []


    def load_input(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            self.rows = len(lines)
            self.cols = len(lines[0])
            for row, line in enumerate(lines):
                for col, c in enumerate(line):
                    if c == "#": # is obstacle?
                        self.obstacles.append((row,col))
                    if (self.cursorPos == [-1,-1]): # is cursor? 
                        direction = Direction.cursorToDir(c)
                        if (direction is not None):
                            self.direction = direction
                            self.cursorPos = [row, col]

    def isOutOfBounds(self, pos):
        if pos[0] >= self.rows or pos[0] < 0:
            return True
        if pos[1] >= self.cols or pos[1] < 0:
            return True
        return False
    
    def obstacleHit(self, pos: tuple):
        if (pos) in self.obstacles:
            self.direction = Direction.next(self.direction)
            return True 
        return False
    
    def isFinished(self, pos: tuple):
        if (self.isOutOfBounds(pos)):
            return True
        if (self.obstacleHit(pos)):
            return False 
        if pos not in self.visited:
            self.visited.append(pos)
        self.cursorPos = [pos[0], pos[1]]
        return False

    def process(self) -> int:
        # first visited position is the starting position 
        self.visited.append((self.cursorPos[0], self.cursorPos[1]))
        while True:
            newPos = Direction.moveOneStep(self.direction, self.cursorPos[0], self.cursorPos[1])
            if (self.isFinished((newPos[0], newPos[1]))):
                break
        return len(self.visited)

# this method isn't very good, takes a long time to compute 
class Q2(Q1):
    def __init__(self, startPos, startDir, q1) -> None:
        super(Q2, self).__init__()
        # inherrit from Q1
        self.cols = q1.cols
        self.rows = q1.rows
        self.obstacles = q1.obstacles
        self.visited = q1.visited 
        # to solve q2
        self.startPos = startPos
        self.startDir = startDir
        self.posResultInLoop = []

    def obstacleHit(self, pos, obstacles):
        if (pos[0], pos[1]) in obstacles:
            self.direction = Direction.next(self.direction)
            return True 
        return False

    def checkIfTrapped(self, obstructionPos):
        self.cursorPos = [self.startPos[0], self.startPos[1]]
        self.direction = self.startDir
        obstacleHitLog = {}
        while True:
            ret = Direction.moveOneStep(self.direction, self.cursorPos[0], self.cursorPos[1])
            newPos = (ret[0], ret[1])
            if (self.isOutOfBounds(newPos)):
                logger.debug(f"{obstructionPos} does not work")
                return False
            prevDir = self.direction
            if (self.obstacleHit(newPos, self.obstacles+[obstructionPos])):
                if (newPos in obstacleHitLog):
                    if prevDir in obstacleHitLog[newPos]:
                        # we are hitting the same object from the same direction 
                        # we are looping 
                        logger.debug("Loop found at {obstructionPos}")
                        return True
                    else:
                        obstacleHitLog[newPos].append(prevDir)
                else:
                    obstacleHitLog[newPos] = [prevDir]
            else:
                self.cursorPos = [newPos[0], newPos[1]]


    def process(self):
        for testPos in self.visited[1:]: # doesn't make sense to test the starting position 
            if (self.checkIfTrapped(testPos)):
                self.posResultInLoop.append(testPos)

        return len(self.posResultInLoop) 

def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    startPos = q1.cursorPos
    startDir = q1.direction
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(startPos=startPos, startDir=startDir, q1=q1)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
