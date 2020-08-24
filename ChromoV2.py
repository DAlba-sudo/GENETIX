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
        self.DIR = "DATA\\"
        self.avgFitPop = 0.0

        # Necessary Arrays
        self.population = []
        self.testQueue = []
        self.deadIndividuals = []
        self.buildQueue = []

        # directory information
        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_FOLDER = os.path.join(self.BASE_PATH, "DATA\\")

        # file information
        self.STEADY_POPULATION = os.path.join(self.DATA_FOLDER, "STEADY_POPULATION.txt")
        self.TEST_QUEUE = os.path.join(self.DATA_FOLDER, "TEST_QUEUE.txt")
        self.CEMENTARY = os.path.join(self.DATA_FOLDER, "CEMENTARY.txt")
        self.GLOBAL_POPULATION = os.path.join(self.DATA_FOLDER, "GLOBAL_POPULATION.txt")
        self.BUILD_QUEUE = os.path.join(self.DATA_FOLDER, "BUILD.txt")

        self.SELECT_FOR_TESTING = 0.25
        self.REPLACE = 0.34

    def updateFilePaths(self):
        self.STEADY_POPULATION = os.path.join(self.DATA_FOLDER, "STEADY_POPULATION.txt")
        self.TEST_QUEUE = os.path.join(self.DATA_FOLDER, "TEST_QUEUE.txt")
        self.CEMENTARY = os.path.join(self.DATA_FOLDER, "CEMENTARY.txt")
        self.GLOBAL_POPULATION = os.path.join(self.DATA_FOLDER, "GLOBAL_POPULATION.txt")
        self.BUILD_QUEUE = os.path.join(self.DATA_FOLDER, "BUILD.txt")

        while True:
            try:
                self.openFile(self.STEADY_POPULATION)
                self.openFile(self.TEST_QUEUE)
                self.openFile(self.CEMENTARY)
                self.openFile(self.GLOBAL_POPULATION)
                self.openFile(self.BUILD_QUEUE)
                break
            except FileNotFoundError:
                pass
        
    def openFile(self, file):
        with open(file, "a+") as f:
            f.close()

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


        tempChildChromo.importFromAllele(tempChild)
        return tempChildChromo

    def avgFitSum(self):
        fitSum = 0
        count = 0
        fitArr = []
        for indiv in range(self.lenPopulation()):
            current_indiv = self.population[indiv]
            current_fit = current_indiv.getFit()
            if(current_fit is not None):
                fitArr.append(current_fit)
                fitSum += current_fit
                count += 1
            else:
                pass
        q1 = np.quantile(fitArr, 0.25)
        q3 = np.quantile(fitArr, 0.75)
        IQR = q3 - q1
        lowerBound = q1 - (1.5 * IQR)
        upperBound = q3 + (1.5 * IQR)

        newFitArr = []
        for fit in range(len(fitArr)):
            current_f = fitArr[fit]
            if ((current_f < lowerBound) or (current_f > upperBound)):
                pass
            else:
                newFitArr.append(current_f)

        avgFit = np.average(newFitArr)
        return avgFit

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

    def migrateData(self, DIR1):
        # create DIR if not already existing
        while True:
            self.DIR = DIR1
            DATA_FOLDER = os.path.join(self.BASE_PATH, str(str(self.DIR) + "\\"))
            try:
                os.mkdir(str(DATA_FOLDER))
                break
            except FileExistsError:
                break
        self.DATA_FOLDER = DATA_FOLDER
        self.updateFilePaths()

        self.population = []
        self.testQueue = []
        self.buildQueue = []


        # load in current steady population
        self.importChromosomeIntoArray(self.STEADY_POPULATION, self.population)          

        # load in testQueue
        self.importChromosomeIntoArray(self.TEST_QUEUE, self.testQueue)

        # load in buildQueue
        self.importChromosomeIntoArray(self.BUILD_QUEUE, self.buildQueue)
        

    def importChromosomeIntoArray(self, file, arr):
        try:
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
                    
                    exampleChromo = copy.deepcopy(self.root)
                    exampleChromo.importFromFileData(value_list)
                    arr.append(exampleChromo)
        except FileNotFoundError:
            pass
        
    def randomSelection(self):
        choice = random.choice(self.population)
        for itm in range(self.lenPopulation()):
            if self.population[itm] == choice:
                return itm
            else:
                pass
        
        return -1
    
    def variate(self, x, pm):
        variation = (pm * random.random())
        ops = [add, sub]
        op = random.choice(ops)
        val = op(x, (x*variation))
        return val
            
    def performGA(self, var=None, rand_select=None, pT=None, pR=None):
        count = 0
        method = 0
        itr = 0

        # os.system('clear')
        # print("CURRENT WORKING GA => " + str(self.DIR))
        # print("\n")
        # print("What would you like to do?")
        # # Migrate Data
        # print("1) Change GA")

        # # Perform GA
        # print("2) Perform GA")

        # #Analyze Population
        # print("3) Analyze Population")

        # while True:
        #     try:
        #         user_input = int(input("\n>> "))
        #         break
        #     except ValueError:
        #         os.system('clear')
        #         print("CURRENT WORKING GA => " + str(self.DIR))
        #         print("\n")
        #         print("What would you like to do?")
        #         # Migrate Data
        #         print("1) Change GA")

        #         # Perform GA
        #         print("2) Perform GA")

        user_input = 2
        
        if(pT is not None) and (pR is not None):
            isVar = False
            isRan = False
            if(var == 1):
                isVar = True
            if(rand_select == 1):
                isRan = True
            
            ending = ""
            newEnding = ""
            if(isVar):
                ending += "var"
            if(isRan):
                ending += "-ran"

            if(len(ending) > 2):
                newEnding = "(" + ending + ")" 
            
            data_path = "%s-%s%s" % (str(pT), str(pR), str(ending))
            self.migrateData(data_path)
        if(user_input == 1):
            os.system('clear')
            print("What DIR would you like to migrate to?")
            DIR_DEST = input("\n>>")
            self.migrateData(DIR_DEST)
            self.performGA()
        elif(user_input == 2):
            count = 50
            method = 1
            
            if(var is None):
                os.system('clear')
                print("Would you like variation turned on? y(1)/n(0)")
                variation = int(input(">>"))
            else:
                variation = var
        
            if(rand_select is None):
                os.system('clear')
                print("Would you like random replacement turned on? y(1)/n(0)")
                rand_replacement = int(input(">>"))
            else:
                rand_replacement = rand_select
            if(pT is None):
                os.system('clear')
                print("What would you like the training percentage to be?")
                self.SELECT_FOR_TESTING = float(input(">>"))
            else:
                self.SELECT_FOR_TESTING = pT
            if(pR is None):
                os.system('clear')
                print("What would you like the generation gap to be?")
                self.REPLACE = float(input(">>"))
            else:
                self.REPLACE = pT
            

        elif(user_input == 3):
            os.system('clear')

            genNUM = int(input("How many generations?\n>>"))

            file_num = 0
            totalGen = []
            for f in range(genNUM):
                tempPop = []
                file_path = "tempSteady%s.txt" % (str(f))
                path = os.path.join(self.DATA_FOLDER, file_path)
                self.importChromosomeIntoArray(path, tempPop)
                totalGen.append(tempPop)
                file_num += 1

            for gen in range(len(totalGen)):
                current_gen = totalGen[gen]
                current_gen_fit_sum = 0
                current_gen_avg = 0
                for ind in range(len(current_gen)):
                    current_ind = current_gen[ind]
                    current_gen_fit_sum += current_ind.getFit()
                
                current_gen_avg = current_gen_fit_sum / (len(current_gen))
                print("GEN %s has an avg fit of %s" % (gen, current_gen_avg))
            
            print("Collect data, press enter when done!")
            input(">> ")
            self.performGA()

        else:
            pass

        # for u in range(50):
        #     if u == 0:
        #         pass
        #     else:
        #         path = os.path.join(self.DATA_FOLDER, str("tempSteady%s.txt" % (str(u))))
        #         with open(path, "r") as f:
        #             pass


        n = 0
        while (n < count):
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
                # if method is set to automatic
                if(method == 1):
                    # loading in data
                    qC = current_mem.displayGene("qC")
                    qS = current_mem.displayGene("qS")

                    # calculating fitness
                    prop = (float(qC) / float(qS))

                    yFit = ( prop * 10 ) / 1.667
                    if (yFit > 10):
                        yFit = (10) + (10 - yFit)
                    if (yFit < 0.1):
                        yFit = 0.1
                    
                    # add a little bit of guessing to simulate human error
                    if(variation == 1):
                        variated_yFit = self.variate(yFit, 0.10)
                        current_mem.updateFitness(variated_yFit) 
                    else: 
                        current_mem.updateFitness(yFit)                   

                    # Transfering data from testQueue to buildQueue
                    if(current_mem.getFit() is not None):
                        self.buildQueue.append(current_mem)
                        self.testQueue.remove(current_mem)
                    else: 
                        raise Exception("Ayo we got a NaN problem in 665")

                    # save data
                    self.writePopulation(self.BUILD_QUEUE, self.buildQueue)
                    self.writePopulation(self.TEST_QUEUE, self.testQueue)
                    self.writePopulation(self.STEADY_POPULATION)

            self.writePopulation(self.TEST_QUEUE, self.testQueue)
            self.writePopulation(self.BUILD_QUEUE, self.buildQueue)
            self.writePopulation(self.STEADY_POPULATION)    

            # members of buildQueue that have no fitness
            blacklist = []

            # preparing data from buildQueue for model training
            for itm in range(len(self.buildQueue)):
                current_itm = self.buildQueue[itm]
                if current_itm.getFit() is not None:
                    fit_arr.append(current_itm.getFit())
                else:
                    blacklist.append(current_itm)

            # remove members of buildQueue that have no fitness from blacklist
            for bl in range(len(blacklist)):
                current_bl = blacklist[bl]
                self.buildQueue.remove(current_bl)

            x1, x2 = self.GENE_VALUES()


            # fit polynomial model
            self.fitModel(x1=x1, x2=x2, fitness_arr=fit_arr)

            # fit entire population
            self.fitEntirePopluation()

            # Record Fitness of Population
            self.writePopulation(self.STEADY_POPULATION)

            # Record Intermediate Population
            while True:
                try:
                    tempSteady = os.path.join(self.DATA_FOLDER, str("tempSteady%s.txt" % (str(itr))))
                    tempBuild = os.path.join(self.DATA_FOLDER, str("tempBuild%s.txt" % (str(itr))))
                    tempTest = os.path.join(self.DATA_FOLDER, str("tempTest%s.txt" % (str(itr))))
                    tempCementary = os.path.join(self.DATA_FOLDER, str("tempCementary%s.txt" % (str(itr))))

                    self.writePopulation(tempSteady)
                    self.writePopulation(tempBuild, self.buildQueue)
                    self.writePopulation(tempTest, self.testQueue)
                    self.writePopulation(tempCementary, self.deadIndividuals)
                    itr += 1
                    break
                except FileNotFoundError:
                    self.openFile(tempSteady)
                    self.openFile(tempBuild)
                    self.openFile(tempTest)
                    self.openFile(tempCementary)

            for j in range(floor(self.size*self.REPLACE)):
                # Parent Selection
                P1, P2 = self.parentSelection()

                # Child is created
                Child = self.crossover(P1, P2)

                # index for replacement is chosen
                if(rand_replacement == 1):
                    index = self.randomSelection()
                else:
                    index = self.replaceForDeath()

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
            self.writePopulation(self.BUILD_QUEUE, self.buildQueue)

            self.avgFitPop = self.avgFitSum()

            # TELEMETRY / LOGGING
            n += 1
            os.system('clear')
            print("Current Directory => %s" % self.DIR)
            print("-------GENERATION %s-------" % (str(n)))
            print("GA Average Fitness => " + str(self.avgFitPop))
            print("\n")

    

        


if __name__ == "__main__":
    GA = Population(80)

    GA.SELECT_FOR_TESTING = 0.31
    GA.REPLACE = 0.64
    
    rootChromo = Chromosome()
    rootChromo.line = 1
    rootChromo.addGene("qC", 30)
    rootChromo.addGene("qS", 12)
    GA.addRoot(rootChromo)

    test_param_queue = [
        [0, 0, 0.20, 0.80],
        [1, 0, 0.20, 0.80],
        [1, 1, 0.20, 0.80],
        [0, 0, 0.10, 0.90],
        [1, 0, 0.10, 0.90],
        [1, 1, 0.10, 0.90]
    ]

    for param in range(len(test_param_queue)):
        c_ = test_param_queue[param]
        GA.performGA(c_[0], c_[1], c_[2], c_[3])