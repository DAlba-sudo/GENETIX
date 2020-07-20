import random
from operator import add, sub

#Gene class controls the logic for the individual control values 
class Gene:

    # the init takes in a foreVal, i.e the predetermined value and slightly adapts it 
    def __init__(self, foreVal, bias=None, max_mutation=None):
        #parameter handling for the mutation cap
        if(max_mutation is not None):
            self.MAX_ADAPTION = max_mutation
        else:
            self.MAX_ADAPTION = 0.05

        # sets bias (bias is the programs way of minimizing adaption or maximizing adaption)
        if(bias is None):
            self.bias  = 1.0
        else:
            self.bias = bias
			
        self.gene_value = self.setVal(foreVal)
        self.foreVal = foreVal
	
    # rangeClip clips the range of the item passed through the val paramater
    def rangeClip(self, val, minV, maxV):
        targetV = val
        if(val < minV):
        	targetV = minV	
        if(val > maxV):
        	targetV = maxV
        return targetV
	
    # sets the actual mutation factor
    def setPercent(self):
        randFloat = random.random()
        while(randFloat > self.MAX_ADAPTION):
            randFloat = random.random()
        
        return randFloat
    # sets the value of the gene accounting for slight adaption techniques
    def setVal(self, foreVal):
        percent = self.setPercent()
        ops = [add, sub]
        op = random.choice(ops)
        value = op(foreVal, (foreVal*percent)) * self.bias
        return value

# Chromosome class (Asexual Reproduction)
class Chromo:
    def __init__(self, parent=None):
        self.qCoffee = None
        self.qWater = None
        self.qSugar = None
        self.qMilk = None

        if(parent is not None):
            try:
                self.inheritFromParent(parent)
            except AttributeError:
                try:
                    self.retrieveFromArr(parent)
                except IndexError:
                    raise Exception("Something went wrong! Parent parameter must be array or Chromo type")
        
        self.fitness = None
        self.sweetFit = None
        self.bitterFit = None


    def inheritFromParent(self, parent):
        self.qCoffee = Gene(parent.qCoffee.gene_value)
        self.qWater = Gene(parent.qWater.gene_value)
        self.qSugar = Gene(parent.qSugar.gene_value)
        self.qMilk = Gene(parent.qMilk.gene_value)

    def retrieveFromArr(self, arr):
        self.qCoffee = Gene(arr[0])
        self.qWater = Gene(arr[1])
        self.qSugar = Gene(arr[2])
        self.qMilk = Gene(arr[3])

    def exportToArr(self, chromo=None):
        if(chromo is not None):
            return [chromo.qCoffee.gene_value, chromo.qWater.gene_value, chromo.qSugar.gene_value, chromo.qMilk.gene_value]
        else:
            return[self.qCoffee.gene_value, self.qWater.gene_value, self.qSugar.gene_value, self.qMilk.gene_value]

    def setFitness(self, fitness):
        self.fitness = fitness
