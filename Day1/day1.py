import numpy as np

class Q1():
    def __init__(self) -> None:
        self.data = np.array(0)

    def load_input(self, filename):
        data = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                val1, val2 = line.split()
                data.append([int(val1), int(val2)])
        
        self.data = np.array(data)

    def process(self):
        list1 = np.sort(self.data[:,0])
        list2 = np.sort(self.data[:,1])
        diff = np.abs(list1 - list2)
        total = np.sum(diff)
        return int(total)

class Q2():
    def __init__(self, data) -> None:
        self.data = data
    
    def process(self):
        # make a dictionary from the second list counting the number of occurances 
        valDict = {}
        for val in self.data[:,1]:
            if val in valDict:
                valDict[val] += 1
            else:
                valDict[val] = 1
        score = 0
        for val in self.data[:,0]:
            if val in valDict:
                score += (val*valDict[val])
        
        return score


def run():
    # run program 
    q1 = Q1()
    q1.load_input("example.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(q1.data)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
