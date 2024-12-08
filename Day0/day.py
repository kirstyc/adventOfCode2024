import logging 
import sys

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

class Q1():
    def __init__(self) -> None:
        pass

    def load_input(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            self.data = lines
            
    def process(self) -> int:
        
        return 0
    
class Q2():
    def __init__(self) -> None:
        pass
            
    def process(self) -> int:
        
        return 0


def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2()
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()