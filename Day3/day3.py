import logging 
import sys
import re

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.INFO)

class Q1():
    def __init__(self) -> None:
        self.data = ""

    def load_input(self, filename):
        with open(filename) as f:
            # input is one long line 
            self.data = f.read() 

    def process(self):
        # search for "mul(x,y)"" where x,y can be 1-3 digits
        regexMatch = "mul\(\d{1,3},\d{1,3}\)"
        matches = re.findall(regexMatch, self.data)
        sum = 0
        for match in matches:
            logger.debug(f"{match}")
            # get just the two numbers to multiply
            d1, d2 = re.findall("\d{1,3}", match)
            sum += int(d1)*int(d2)

        return sum



class Q2():
    def __init__(self) -> None:
        pass

    def process(self, data):
        # also look for don'() and do() functions 
        regexMatch = "mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)"
        matches = re.findall(regexMatch, data)
        sum = 0
        do = True
        for match in matches:
            logger.debug(f"{match}")
            if match == "don't()":
                do = False
            elif match == "do()":
                do = True
            else:
                d1, d2 = re.findall("\d{1,3}", match)
                if (do):
                    sum += int(d1)*int(d2)
                    logger.debug(f"sum={sum}")

        return sum



def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2()
    q2Ans = q2.process(q1.data)
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
