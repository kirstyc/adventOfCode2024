import logging 
import sys
import numpy as np

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

class Expression():
    def __init__(self, ans:int, vals:list):
        self.ans = ans
        self.vals = np.array(vals, dtype=int)
    
    def multiply(self, a, b):
        return a*b
    
    def truthTableSolve(self):
        numBits = len(self.vals)-1
        numPermutations = 2**(numBits)
        for testNum in range(1,numPermutations-1):
            binRep = bin(testNum).lstrip("0b").zfill(numBits)
            total = self.vals[0]
            idx = 1
            for c in binRep: # apply operations to next element 
                if (c == '0'):
                    total += self.vals[idx]
                    idx += 1
                else:
                    total *= self.vals[idx]
                    idx += 1
                if total > self.ans:
                    break # end early, impossible to solve at this point 

            if (total == self.ans):
                return True
        
        return False

    def solvable(self):
        # simple solution checks, starting with summation
        sum = np.sum(self.vals)
        if (sum == self.ans):
            return True
        # multiply all values 
        multi = self.vals[0]*self.vals[1]
        if (len(self.vals) > 2):
            for val in self.vals[2:]:
                multi = self.multiply(multi, val)
        if (multi == self.ans):
            return True
        # mixed operation check 
        if (len(self.vals)>2):
            return self.truthTableSolve()
        return False 
        

class Q1():
    def __init__(self) -> None:
        self.input = []
        self.unsolveable = []

    def load_input(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            for line in lines: 
                ans, nums = line.split(":")
                vals = [int(val) for val in nums.strip().split(" ")]
                self.input.append(Expression(ans=int(ans), vals=vals))
            
    def process(self) -> int:
        total = 0
        for exp in self.input:
            if (exp.solvable()):
                total += exp.ans
            else:
                self.unsolveable.append(exp)

        return total
    
class Q2():
    def __init__(self, input, prevTotal) -> None:
        self.input = input
        self.prevTotal = prevTotal

    def concatVals(self, vals):
        return int("".join(str(val) for val in vals))
    
    def subprocess(self, ans, vals):
        if (len(vals) == 2):
            if (self.concatVals(vals) == ans):
                return True
            if ((vals[0]+vals[1]) == ans):
                return True
            if ((vals[0] * vals [1]) == ans):
                return True
            return False

        splice = vals[1:]
        # concat 
        splice[0] = self.concatVals(vals[0:2])
        if (self.subprocess(ans, splice)):
            return True
        # add
        splice[0] = vals[0]+vals[1]
        if (self.subprocess(ans, splice)):
            return True
        # multiply
        splice[0] = vals[0]*vals[1]
        if (self.subprocess(ans, splice)):
            return True
        
        return False

    def process(self) -> int:
        total = 0 
        for exp in self.input:
            if (self.subprocess(exp.ans, exp.vals.tolist())):
                total += exp.ans
                
        return total + self.prevTotal


def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(q1.unsolveable, q1Ans)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()