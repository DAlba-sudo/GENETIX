import random

from operator import add, sub
from math import floor
import copy

class Allele:

    def __init__(self, value=None):
        if(value is None):
            self.value = None
        else:
            self.value = value

    def getValue(self):
        return self.value

    def updateValue(self, updated_value):
        self.value = updated_value

class Gene:
    
    def __init__(self):
        self.allele = Allele()
        self.min_constraint = None
        self.max_constraint = None

    def updateAllele(self, value):
        clipped_allele = self.rangeClip(value, self.min_constraint, self.max_constraint)
        self.allele.updateValue(clipped_allele)
    
    def getAllele(self):
        return self.allele.getValue()

    def rangeClip(self, x, minC=None, maxC=None):
        if(minC is not None):
            if(x < minC):
                return minC
        if(maxC is not None):
            if(x > maxC):
                return maxC
        else:
            return x

    def setConstraints(self, min_constraint = None, max_constraint = None):
        if(min_constraint is not None):
            self.min_constraint = min_constraint
        if(max_constraint is not None):
            self.max_constraint = max_constraint
        
        clipped_allele = self.rangeClip(self.getAllele(), self.min_constraint, self.max_constraint)
        self.allele.updateValue(clipped_allele)
    
    def mutate(self, pM):
        equilizer = random.random()
        if (equilizer < pM):

            mutateFactor = random.random()
            delta = self.getAllele() * mutateFactor

            ops = [add, sub]
            op = random.choice(ops)
            mutated_value = op(self.getAllele(), delta)
           
        self.updateAllele(mutated_value)

class Chromosome:
    
    def __init__(self):
        self.GENES = {

        }

        self.fitness = None

    def getFit(self):
        return self.fitness

    def updateFitness(self, fitness):
        self.fitness = fitness

    def isFit(self):
        return (self.fitness != None)

    def mutateDriver(self):
        for key in self.GENES:
            current_gene = self.GENES[key]
            current_gene.mutate(0.1)

    def forceMutation(self, key):
        self.GENES[key].mutate(1.0)
        return self.GENES[key].getAllele()

    def addGene(self, key, value=None):
        self.GENES[key] = Gene()
        if(value is not None):
            self.updateGene(key, value)

    
    def updateGene(self, key, value):
        self.GENES[key].updateAllele(value)

    def displayGene(self, key):
        return self.GENES[key].getAllele()
    
    def geneArray(self):
        tempArray = []
        for key in self.GENES:
            tempArray.append(self.GENES[key].getAllele())
        
        return tempArray

    def importFromAllele(self, allele_array):
        tempAlleleArray = []
        # converts standard floats to an allele
        for allele in range(len(allele_array)):
            current_val = allele_array[allele]
            tempArray.append(Allele(current_val))

        tempGeneArray = []
        # converst Allele to Genes
        for gene in range(len(tempAlleleArray)):
            current_allele = tempAlleleArray[gene]
            tempGene = Gene()
            tempGene.allele = current_allele
            tempGeneArray.append(tempGene)

        # replaces key value with allele values
        itr = 0
        for key in self.GENES:
            current_targeted_gene = self.GENES[key]
            current_targeted_gene = tempGene[itr]
            itr+=1

class Population:

    def __init__(self, nCap):
        self.size = nCap
        self.population = []
        self.testQueue = []

        if(self.lenPopulation() == 0):
            self.randomGenerate()

    def lenPopulation(self):
        return len(self.population)

    def addRoot(self, chromo):
        self.root = chromo

    def randomGenerate(self):
        # Not supposed to be here, but will be until fix is provided for init to include adding root
        root = Chromosome() 
        root.addGene("qC", 30.9)
        root.addGene("qS", 12.3)
        self.addRoot(root)

        for child in range(self.size):
            # create random child
            randChild = copy.deepcopy(self.root)

            for key in randChild.GENES:
                randChild.forceMutation(key)
            
            self.population.append(randChild)

    def displayPopulation(self):
        for item in range(self.lenPopulation()):
            current_item  = self.population[item]
            print(current_item.geneArray())

    def crossover(self, P1, P2):
        P1_arr = P1.geneArray()
        P2_arr = P2.geneArray()
        tempChild = []
        tempChildChromo = Chromosome()

        for allele in range(len(P1_arr)):
            P1_current_allele = P1_arr[allele] # head (1)
            P2_current_allele = P2_arr[allele] # tail (0)

            # emulate coin flip
            coin_flip = random.randint(0, 1)
            if (coin_flip == 0):
                tempChild.append(P1_current_allele)
            else:
                tempChild.append(P2_current_allele)

        tempChildChromo.importFromAllele(tempChild)
        return tempChildChromo

    def fitSum(self):
        fitSum = 0
        for indiv in range(self.lenPopulation()):
            current_indiv = self.population[indiv]
            fitSum += current_indiv.getFit()

    def parentSelection(self):
        fit_sum = self.fitSum()

        P1 = None
        P2 = None

        while((P1 is None) or (P2 is None)):
            p1_pointer = random.random()
            p2_pointer = random.random()

            for indiv in range(self.lenPopulation()):
                current_indiv = self.population[indiv]
                current_fit = current_indiv.getFit()

                rel_fit = current_fit / fit_sum

                # if p1_pointer is less than rel_fit this is a parent
                if((p1_pointer < rel_fit) and (p1_pointer is not None)):
                    # check to make sure it is not the same as P2
                    P1 = self.population[indiv]
                    if(P1 == P2):
                        P1 = None
                
                # if p2_pointer is less than rel_fit this is a parent
                elif((p2_pointer < rel_fit) and (p2_pointer is not None)):
                    P2 = self.population[indiv]
                    if(P1 == P2):
                        P2 = None

                # if none qualified then do this
                else:
                    pass
        
        # returns a tuple
        return P1, P2
        
    # inverse fitness selection for deletion
    def replaceForDeath(self):
        fit_sum = self.fitSum()

        iFit = 0

        for indiv in range(self.lenPopulation()):
            current_indiv = self.population[indiv]
            current_indiv_fitness = current_indiv.getFit()

            rel_fit = current_indiv_fitness / fit_sum
            inverse_rel_fit = 1 / rel_fit
            iFit += inverse_rel_fit

        pointer = random.random()
        for itm in range(self.lenPopulation()):
            current_indiv = self.population[indiv]
            current_indiv_fitness = current_indiv.getFit()

            rel_fit = current_indiv_fitness / fit_sum
            inverse_rel_fit = 1 / rel_fit
            adjusted_inverse_rel_fit = inverse_rel_fit / iFit

            if ( pointer < adjusted_inverse_rel_fit ):
                return itm # returns the index of the member of the population that will be replaced
            else:
                pass

    def isInArray(self, x, array):
        flag = False
        for itm in range(len(array)):
            current_itm = array[itm]
            if (current_itm == x):
                flag = True
            else:
                pass
        
        return flag

    def selectForTesting(self, n):
        len_testQueue = len(self.testQueue)
        while(len_testQueue < n):
            
            equilizer = random.random()
            target_index = floor((equilizer * (self.lenPopulation())))
            target_member = (self.population[target_index])

            # test to see if in array
            if (not self.isInArray(target_member, self.testQueue)):
                self.testQueue.append(target_member)
            else: 
                pass

            len_testQueue = len(self.testQueue)
            
    def fitEntirePopluation(self):
        pass

    def fitModel(self):
        pass

if __name__ == "__main__":
    GA = Population(100)
    GA.displayPopulation()