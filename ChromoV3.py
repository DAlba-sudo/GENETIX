from operator import add, sub
import random

class Gene:
    def __init__(self, value, bias=None, max_mutation=None, slightAdaption=None):
        # value => (float) the value that is being passed into the gene
        # bias => (float) used to determine if mutation should be applied positively or negatively
        # max_mutation => (float) determines the maximum mutation (i.e, the max change allowed for said value in the form of a percent)
        # slightAdaption => (bool) determines if mutation will be applied
        
        tempVal = 0
        tempMutation = 0
        tempBias = 0
        # sets the bias
        if(bias is not None):
            tempBias = bias
        else:
            tempBias = 0.0
        self.bias = tempBias

        # sets the mutations
        if(max_mutation is not None):
            tempMutation = max_mutation
        else:
            tempMutation = 0.10
        self.MAX_MUTATION = tempMutation

        # sets the adaption factor / value
        if(slightAdaption is not None):
            # we want to include a mutation
            tempVal = self.setVal(value)
        else:
            # we want to simply pass in the value
            tempVal = value
        self.value = tempVal

    def setPercent(self):
        randFloat = random.random()
        while(randFloat > self.MAX_MUTATION):
            randFloat = random.random()
        
        return randFloat

    # checks to see if an item is within a min and max range
    def within(self, randFloat, min_range, max_range):
        minTest = False
        maxTest = False
        if(randFloat < max_range):
            maxTest = True
        if(randFloat > min_range):
            minTest = True
        
        return minTest and maxTest

    # Used for incorporating a bias to the selection process (add or subtraction)
    def arrayRandSelector(self, arr, bias=None):
        len_arr = len(arr)
        if(bias is not None):
            randFloat = random.random() + bias
        else:
            randFloat = random.random()
        for index in range(len_arr):
            min_range = index/len_arr
            diff = 1/len_arr
            max_range = min_range + diff

            if(self.within(randFloat, min_range, max_range)):
                return index
            else:
                pass


    # sets the value of the gene accounting for slight adaption techniques
    def setVal(self, value):
        percent = self.setPercent()
        ops = [add, sub]
        returnedIndex = self.arrayRandSelector(ops, self.bias)
        op = ops[returnedIndex]
        value = op(value, (value*percent))
        return value

class ChromoV3:
    def __init__(self, array=None, parent=None):
        self.qCoffee = None
        self.qWater = None
        self.qSugar = None
        self.qMilk = None

        self.fitness = None
        self.sweetFit = None
        self.bitterFit = None

        if(parent is not None):
            # if a parent is passed we need to inherit genes
            self.inheritFromParent(parent)

        elif(array is not None):
            # chromosome is passed in array format signifying translation from array
            self.translateFromArray(array)

        else:
            raise Exception("Corrupt Chromosome Created, procedure aborted.")

        # inherits genomic values from a single parent
        def inheritFromParent(self, parentChromo):
            self.qCoffee = parentChromo.qCoffee
            self.qWater = parentChromo.qWater
            self.qSugar = parentChromo.qSugar
            self.qMilk = parentChromo.qMilk

        # collects genomic information in the form of an array and creates an individual from that information
        def translateFromArray(self, arr):
            self.qCoffee = arr[0]
            self.qWater = arr[1]
            self.qSugar = arr[2]
            self.qMilk = arr[3]
            try:
                self.fitness = arr[4]
            except IndexError:
                pass
        
        # translates current genomic information to an array
        def translateToArray(self):
            return [self.qCoffee, self.qWater, self.qSugar, self.qMilk]           
        