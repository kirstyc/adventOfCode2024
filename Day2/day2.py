# import numpy as np

class Q1():
    def __init__(self) -> None:
        self.data = [[]]

    def load_input(self, filename):
        data = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                levels = [int(val) for val in line.split()]
                data.append(levels)
        
        self.data = data

    def subprocess(self, report):
        # check if this is increasing or decreasing
        isIncreasing = True 
        if (report[1] - report[0] < 0):
            isIncreasing = False
        for idx, val in enumerate(report):
            try:
                nextVal = report[idx+1]
            except:
                return True
            diff = nextVal - val
            if diff >= 4:
                return False
            elif diff <= -4:
                return False
            elif diff == 0:
                return False
            elif isIncreasing and (diff < 0):
                return False
            elif not isIncreasing and (diff > 0):
                return False 
            
        return True 

    def process(self):
        numSafe = 0 
        for report in self.data:
            if (self.subprocess(report)):
                numSafe += 1
        return numSafe


class Q2():
    def __init__(self, data) -> None:
        self.data = data
        self.badIndex = -1

    def subprocess(self, report):
        # check if this is increasing or decreasing
        isIncreasing = True 
        if (report[1] - report[0] < 0):
            isIncreasing = False
        for idx, val in enumerate(report):
            try:
                nextVal = report[idx+1]
            except:
                return True
            diff = nextVal - val
            if diff >= 4 or diff <= -4:
                self.badIndex = idx
                return False
            elif diff == 0:
                self.badIndex = idx
                return False
            elif isIncreasing and (diff < 0):
                self.badIndex = idx
                return False
            elif not isIncreasing and (diff > 0):
                self.badIndex = idx
                return False 
            
        return True 
    
    def process(self):
        numSafe = 0 
        for report in self.data:
            if (self.subprocess(report)):
                numSafe += 1
            else:
                for i in range(len(report)):
                    copyReport = report[:]
                    copyReport.pop(i)
                    if (self.subprocess(copyReport)):
                        numSafe += 1
                        break

        return numSafe


def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(q1.data)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
