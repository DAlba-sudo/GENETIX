from random import randint
from chromosomeV2 import Chromo

class GA:
    def __init__(self):
        pass

    def selectCrossOverPoint(self, length):
        return randint(1, (length-1))

    def crossOver(self, chromo1, chromo2):
        #select crossOver point
        chrom1_arr = chromo1.exportToArr(chromo1)
        chromo2_arr = chromo2.exportToArr(chromo2)

        crossPoint = self.selectCrossOverPoint(len(chromo1_arr))

        print("CrossOver Point = %s" % (crossPoint))

        # splice both arrays
        preSplit1 = chromo1_arr[0:crossPoint]
        print("preSplit1 = " + str(preSplit1)) 
        postSplit1 = chromo1_arr[crossPoint:]
        print("postSplit1 = " + str(postSplit1)) 
        preSplit2 = chromo2_arr[0:crossPoint]
        print("preSplit2 = " + str(preSplit2))
        postSplit2 = chromo2_arr[crossPoint:]
        print("postSplit2 = " + str(postSplit2))

        # select from splices
        preSelector = randint(1,2)
        print("preSelector = " + str(preSelector))

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

        print("\n")
        print("childPre is = %s; childPost is = %s" % (str(childPre), str(childPost)))

        return child


if __name__ == "__main__":
    chromo1_arr = [10.2, 20.4, 30.9, 40.1]
    chromo2_arr = [80.0, 43.2, 28.5, 11.2]

    chromo1 = Chromo(chromo1_arr)
    chromo2 = Chromo(chromo2_arr)

    gA = GA()
    child = gA.crossOver(chromo1, chromo2)
    print("\n")
    print("Child: "+str(child.exportToArr(child)))
    print("\n")
    print("Parents: " + str(chromo1.exportToArr(chromo1)))
    print("Parents: " + str(chromo2.exportToArr(chromo2)))


