import logging 
import sys
import numpy as np

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout,level=logging.INFO)

class Q1():
    def __init__(self) -> None:
        self.pageOrders = {}
        self.pageSets = []
        self.unorderedSets = [] # for question 2 

    def load_input(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                # look for page orders
                ret = line.split("|")
                if (len(ret) == 2):
                    importantPage = int(ret[0])
                    page = int(ret[1])
                    if importantPage in self.pageOrders:
                        self.pageOrders[importantPage].append(page)
                    else:
                        self.pageOrders[importantPage] = [page]
                else:
                    # found page set 
                    ret = line.split(",")
                    if (len(ret)>1):
                        self.pageSets.append([int(page) for page in ret])

    def checkCorrectOrder(self, pageSet):
        sortedSet = [pageSet[0]]
        for page in pageSet[1:]:
            if page in self.pageOrders:
                for test in sortedSet:
                    if test in self.pageOrders[page]: # page has a higher priority then test 
                        return False
                    
            sortedSet.append(page)
        logger.debug("set is sorted")
        return True
    
    @classmethod
    def getMiddle(cls, pageSet):
        return pageSet[len(pageSet)//2]
            
    def process(self) -> int:
        total = 0
        for set in self.pageSets:
            if(self.checkCorrectOrder(set)):
                total += Q1.getMiddle(set)
            else:
                self.unorderedSets.append(set)
        
        return total                

class Q2():
    def __init__(self, unorderedSets, orderingRules) -> None:
        self.pageOrders = orderingRules
        self.sets = unorderedSets

    def sortSets(self, set):
        sorted = [set[0]] # gotta start somewhere
        for page in set[1:]:
            if page in self.pageOrders:
                for idx,test in enumerate(sorted):
                    if test in self.pageOrders[page]:
                        # page should come before test in the sorted list 
                        sorted.insert(idx, page)
                        break
            if page not in sorted:
                sorted.append(page)
                
        return sorted


    def process(self):
        total = 0
        for set in self.sets:
            sorted = self.sortSets(set)
            logger.debug(f"sorted:{sorted}")
            middle = Q1.getMiddle(sorted)
            logger.debug(f"middle:{middle}")
            total += middle

        return total 

def run():
    # run program 
    q1 = Q1()
    q1.load_input("input.txt")
    q1Ans = q1.process()
    print(f"Question 1 Answer: {q1Ans}")

    q2 = Q2(q1.unorderedSets, q1.pageOrders)
    q2Ans = q2.process()
    print(f"Question 2 Answer: {q2Ans}")

if __name__=="__main__":
    run()
