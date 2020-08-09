import random

from operator import add, sub
from math import floor
import copy
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from math import isnan, isinf
import os

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
    
    def mutate(self, pM, max_mutation=None):
        equilizer = random.random()
        if (equilizer < pM):
            max_mute = 1.0
            if(max_mutation is not None):
                max_mute = max_mutation 

            mutateFactor = random.random()
            while(mutateFactor > max_mute):
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

        self.line = None

        self.fitness = None

        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_FOLDER = os.path.join(self.BASE_PATH, "DATA/")

        # file information
        self.STEADY_POPULATION = os.path.join(self.DATA_FOLDER, "STEADY_POPULATION.txt")
        self.TEST_QUEUE = os.path.join(self.DATA_FOLDER, "TEST_QUEUE.txt")
        self.CEMENTARY = os.path.join(self.DATA_FOLDER, "CEMENTARY.txt")
        self.GLOBAL_POPULATION = os.path.join(self.DATA_FOLDER, "GLOBAL_POPULATION.txt")

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

    def forceMutation(self, key, max_mutation=None):
        self.GENES[key].mutate(1.0, max_mutation)
        return self.GENES[key].getAllele()

    def addGene(self, key, value=None):
        self.GENES[key] = Gene()
        if(value is not None):
            self.updateGene(key, value)

    def exportAllInfo(self):
        gene_values = self.geneArray()
        tempString = ""
        for val in range(len(gene_values)):
            current_val = gene_values[val]
            if val == 0:
                tempString += str(current_val)
            else:
                tempString += str("," + str(current_val))
            
        tempString += str("," + str(self.getFit()))
        tempString += "\n"

        return tempString

    def updateGene(self, key, value):
        self.GENES[key].updateAllele(value)

    def displayGene(self, key):
        return self.GENES[key].getAllele()
    
    def geneArray(self):
        tempArray = []
        for key in self.GENES:
            tempArray.append(self.GENES[key].getAllele())
        
        return tempArray

    def importFromFileData(self, data):
        length_of_data = len(data)
        gene_val = data[:(length_of_data-1)]
        self.importFromAllele(gene_val)
        self.updateFitness(data[length_of_data-1])

    def importFromAllele(self, allele_array):
        tempAlleleArray = []

        # converts standard floats to an allele
        for allele in range(len(allele_array)):
            current_val = allele_array[allele]
            tempAlleleArray.append(Allele(current_val))

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
            self.GENES[key] = tempGeneArray[itr]
            itr+=1

        self.updateFitness(None)

class Population:

    def __init__(self, nCap):
        self.size = nCap
        self.population = []
        self.testQueue = []
        self.deadIndividuals = []
        self.buildQueue = []

        # directory information
        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_FOLDER = os.path.join(self.BASE_PATH, "DATA/")

        # file information
        self.STEADY_POPULATION = os.path.join(self.DATA_FOLDER, "STEADY_POPULATION.txt")
        self.TEST_QUEUE = os.path.join(self.DATA_FOLDER, "TEST_QUEUE.txt")
        self.CEMENTARY = os.path.join(self.DATA_FOLDER, "CEMENTARY.txt")
        self.GLOBAL_POPULATION = os.path.join(self.DATA_FOLDER, "GLOBAL_POPULATION.txt")
        self.BUILD_QUEUE = os.path.join(self.DATA_FOLDER, "BUILD.txt")

        self.SELECT_FOR_TESTING = 0.25
        self.REPLACE = 0.34

    def clearFile(self, path):
        with open(path, "w+") as f:
            f.write("")

    def lenPopulation(self):
        return len(self.population)

    def addRoot(self, chromo):
        self.root = chromo

    def randomGenerate(self):
        for child in range(self.size):
            # create random child
            randChild = copy.deepcopy(self.root)

            for key in randChild.GENES:
                randChild.forceMutation(key, 0.5)
            
            randChild.line = child
            
            self.population.append(randChild)

    def displayPopulation(self):
        for item in range(self.lenPopulation()):
            current_item  = self.population[item]
            print(current_item.geneArray())

    def crossover(self, P1, P2):
        P1_arr = P1.geneArray()
        P2_arr = P2.geneArray()
        tempChild = []
        tempChildChromo = copy.deepcopy(self.root)

        for allele in range(len(P1_arr)):
            P1_current_allele = P1_arr[allele] # head (1)
            P2_current_allele = P2_arr[allele] # tail (0)

            # emulate coin flip
            coin_flip = random.randint(0, 1)
            if (coin_flip == 0):
                tempChild.append(P1_current_allele)
            else:
                tempChild.append(P2_current_allele)

        print("Crossover Results: " + str(tempChild))

        tempChildChromo.importFromAllele(tempChild)
        return tempChildChromo

    def fitSum(self):
        fitSum = 0
        for indiv in range(self.lenPopulation()):
            current_indiv = self.population[indiv]
            current_fit = current_indiv.getFit()
            if(current_fit is None):
                current_fit = 0
            fitSum += current_fit
        
        return fitSum

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

                if(current_fit is None):
                    current_fit = 0

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


            if(current_indiv_fitness is None):
                current_indiv_fitness = 0
            else:
                rel_fit = current_indiv_fitness / fit_sum

                try:
                    inverse_rel_fit = 1 / rel_fit
                except RuntimeWarning:
                    inverse_rel_fit = 0
                iFit += inverse_rel_fit

        pointer_index = None
        while(pointer_index is None):
            pointer = random.random()
            for itm in range(self.lenPopulation()):
                current_indiv = self.population[itm]
                current_indiv_fitness = current_indiv.getFit()
                
                if(current_indiv_fitness is None):
                    current_indiv_fitness = 0
                else:
                    rel_fit = current_indiv_fitness / fit_sum
                    inverse_rel_fit = 1 / rel_fit
                    
                    if(isinf(inverse_rel_fit)):
                        inverse_rel_fit = 1.0
                    adjusted_inverse_rel_fit = inverse_rel_fit / iFit

                    if ( pointer < adjusted_inverse_rel_fit ):
                        if (current_indiv.isFit()):
                            pointer_index = itm
                    else:
                        pass
        
        return pointer_index

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

    def GENE_VALUES(self):
        coffee = []
        sugar = []
        
        for i in range(len(self.buildQueue)):
            current_i = self.buildQueue[i]
            arr = current_i.geneArray()
            coffee.append(arr[0])
            sugar.append(arr[1])

        return coffee, sugar

    def getAllFitness(self):
        arr = []
        for i in range(len(self.testQueue)):
            current_i = self.testQueue[i]
            fit_ = current_i.getFit()
            arr.append(fit_)

        return arr

    def rangeClip(self, x, minC=None, maxC=None):        
        if (minC is not None) and (maxC is not None):
            if(x < minC):
                return minC
            elif (x > maxC):
                return maxC
            else:
                return x
        elif (minC is not None) and (maxC is None):
            if (x < minC):
                return minC
            else:
                return x
        elif (maxC is not None) and (minC is None):
            if(x > maxC):
                return maxC
            else:
                return x
        else:
            return x
            
    
    def fitEntirePopluation(self):
        for i in range(self.lenPopulation()):
            current_i = self.population[i]
            # if not fit apply fitness
            if(not current_i.isFit()):
                geneInfo = current_i.geneArray()

                coffee_val = np.array([geneInfo[0]])
                sugar_val = np.array([geneInfo[1]])

                coffee_val = coffee_val.reshape(-1, 1)
                sugar_val = sugar_val.reshape(-1, 1)

                coffee_val = self.qCPoly.fit_transform(coffee_val)
                sugar_val = self.qSPoly.fit_transform(sugar_val)

                qCFit = self.qCModel.predict(coffee_val)
                qSFit = self.qSModel.predict(sugar_val)
                avg = ( (qCFit[0][0]) + (qSFit[0][0]) ) / 2.0
                avg_ = self.rangeClip(avg, 0.1, 10.0)
                current_i.updateFitness(avg_)

    def fitModel(self, x1, x2, fitness_arr):
        X_qC = np.array(x1)
        X_qS = np.array(x2)
        Y = np.array(fitness_arr)

        X_qC = X_qC[:, np.newaxis]
        X_qS = X_qS[:, np.newaxis]
        Y = Y[:, np.newaxis]

        self.qCPoly = PolynomialFeatures(degree=4)
        self.qSPoly = PolynomialFeatures(degree=4)

        self.qCPoly_ = self.qCPoly.fit_transform(X_qC)
        self.qSPoly_ = self.qSPoly.fit_transform(X_qS)

        self.qCModel = LinearRegression()
        self.qSModel = LinearRegression()
        
        self.qCModel.fit(self.qCPoly_, Y)
        self.qSModel.fit(self.qSPoly_, Y)

    def writePopulation(self, path, population=None):
        population_array = None
        header_set = False
        
        if population is None:
            population_array = self.population
        else:
            population_array = population
        
        with open(path, "r+") as f:
            header = f.readline()
            header_titles = header.split(",")
            gene_names = list(self.root.GENES.keys())
            gene_names.append("fit\n")

            if(header_titles == gene_names):
                header_set = True
                
        if (not header_set):
            with open(path, "w+") as f:
                gene_names = list(self.root.GENES.keys())
                tempString = ""
                itr = 0
                for key in self.root.GENES:
                    if(itr > 0):
                        tempString += str("," + str(key))
                    else: 
                        tempString += str(str(key))                    
                    itr += 1
                tempString += ",fit\n"
                f.write(tempString)

        with open(path, "w+") as f:
            data = []
            for i in range(len(population_array)):
                current_i = population_array[i]
                i_info = current_i.exportAllInfo()
                data.append(i_info)
        
            f.writelines(data)
    
    def importChromosomeIntoArray(self, file, arr):
        
        with open(file, "r") as f:
            data = f.readlines()

            for d in range(len(data)):
                value_list = []
                current_data = data[d].strip('\n').split(",")
                for v in range(len(current_data)):
                    current_value = current_data[v]
                    try:
                        value_list.append(float(current_value))
                    except ValueError:
                        value_list.append(None)
                
                exampleChromo = copy.deepcopy(rootChromo)
                exampleChromo.importFromFileData(value_list)
                arr.append(exampleChromo)
            
            
    def performGA(self):
        for n in range(5):
            # random init if empty
            if(self.lenPopulation() == 0):
                self.randomGenerate()
            
            # Record Population Data
            self.writePopulation(self.STEADY_POPULATION)
            
            if(len(self.testQueue) == 0):
                # test x% of population
                self.selectForTesting(floor(self.size*self.SELECT_FOR_TESTING))

            # Record Testing Data
            self.writePopulation(self.TEST_QUEUE, self.testQueue)

            # data for training model from testQueue
            fit_arr = []

            while(len(self.testQueue) > 0):
                mem = 0

                current_mem = self.testQueue[mem]    
                os.system("clear")            
                print("There are still individuals in the testQueue that must be tested!")
                print("Before the GA can continue, you must first assign a fitness to these")
                print("individuals!")

                print("What would you like to do?")
                print("  1) Assign fitness")
                print("  2) Exit and Save")
                try:
                    opt = int(input(">> "))
                except ValueError:
                    os.sys.exit("Not an option, halting GA! Checking data...")

                # Assigning a fitness to the member
                if(opt == 1):
                    # Clearing for legibility
                    os.system("clear")
                    print(current_mem.geneArray())
                    while True:
                        try:
                            # get the fitness from user
                            input_fit = float(input("What would you rate this coffee?"))
                            break
                        except ValueError:
                            print("This is not an option! Try Again!")

                    # updating current members fitness
                    current_mem.updateFitness(input_fit)

                    # Transfering data from testQueue to buildQueue
                    self.buildQueue.append(current_mem)
                    self.testQueue.remove(current_mem)

                    # save data
                    self.writePopulation(self.BUILD_QUEUE, self.buildQueue)
                    self.writePopulation(self.TEST_QUEUE, self.testQueue)
                    self.writePopulation(self.STEADY_POPULATION)
                elif(opt == 2):
                    # saving all our data and exiting
                    self.writePopulation(self.STEADY_POPULATION)
                    self.writePopulation(self.TEST_QUEUE, self.testQueue)
                    self.writePopulation(self.BUILD_QUEUE, self.buildQueue)
                    os.sys.exit("Halting GA Procedure, data saved! Thanks!")
                else:
                    pass

            self.writePopulation(self.TEST_QUEUE, self.testQueue)
            self.writePopulation(self.BUILD_QUEUE, self.buildQueue)
            self.writePopulation(self.STEADY_POPULATION)    

            # preparing data from buildQueue for model training
            for itm in range(len(self.buildQueue)):
                current_itm = self.buildQueue[itm]
                fit_arr.append(current_itm.getFit())
            
            x1, x2 = self.GENE_VALUES()


            # fit polynomial model
            self.fitModel(x1=x1, x2=x2, fitness_arr=fit_arr)

            # fit entire population
            self.fitEntirePopluation()

            # Record Fitness of Population
            self.writePopulation(self.STEADY_POPULATION)
            print("------------------------------------------------------------")
            print("Data is about to change drastically, press enter when ready!")
            print("------------------------------------------------------------")
            input(">>")

            for j in range(floor(self.size*self.REPLACE)):
                # Parent Selection
                P1, P2 = self.parentSelection()

                # Child is created
                Child = self.crossover(P1, P2)

                # index for replacement is chosen
                index = self.replaceForDeath()

                print("[%s] has been chosen for death!" % (str(index)))

                # replacement occurs
                current_member = self.population[index]
                self.deadIndividuals.append(current_member)
                current_member.importFromAllele(Child.geneArray())
                self.writePopulation(self.STEADY_POPULATION)
                self.writePopulation(self.CEMENTARY, self.deadIndividuals)

            # Mutation occurs across entire population
            for i in range(self.lenPopulation()):
                current_i = self.population[i]
                current_i.mutateDriver()

            self.writePopulation(self.STEADY_POPULATION)
            self.writePopulation(self.TEST_QUEUE, self.testQueue)

            # TELEMETRY / LOGGING
            print("-------GENERATION-------")
            GA.displayPopulation()
            print("\n")

        


if __name__ == "__main__":
    GA = Population(70)
    rootChromo = Chromosome()
    rootChromo.line = 1
    rootChromo.addGene("qC", 30)
    rootChromo.addGene("qS", 12)
    GA.addRoot(rootChromo)

    # load in current steady population
    GA.importChromosomeIntoArray(GA.STEADY_POPULATION, GA.population)          

    # load in testQueue
    GA.importChromosomeIntoArray(GA.TEST_QUEUE, GA.testQueue)

    # load in buildQueue
    GA.importChromosomeIntoArray(GA.BUILD_QUEUE, GA.buildQueue)

    GA.performGA()