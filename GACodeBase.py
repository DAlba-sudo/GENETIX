from random import randint
from ChromoV3 import ChromoV3 as Chromo
from ChromoV3 import Gene

class GA:
    def __init__(self):
        pass

    def selectCrossOverPoint(self, length):
        return randint(1, (length-1))

    def crossOver(self, chromo1, chromo2):
        #select crossOver point
        chromo1_arr = chromo1.exportToArr(chromo1)
        chromo2_arr = chromo2.exportToArr(chromo2)

        crossPoint = self.selectCrossOverPoint(len(chromo1_arr))

        # splice both arrays
        preSplit1 = chromo1_arr[0:crossPoint]
        postSplit1 = chromo1_arr[crossPoint:]
        preSplit2 = chromo2_arr[0:crossPoint]
        postSplit2 = chromo2_arr[crossPoint:]

        # select from splices
        preSelector = randint(1,2)

        childPre = None
        childPost = None
	
        #combine according to selectors
        if (preSelector == 1):
            childPre = preSplit1
            childPost = postSplit2  
        else:
            childPre = preSplit2
            childPost = postSplit1

        child = Chromo(parent=(childPre + childPost))
        return child