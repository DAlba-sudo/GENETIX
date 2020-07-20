from chromosomeV2 import Gene
from chromosomeV2 import Chromo
from GACodeBase import GA

from sklearn import linear_model
import numpy as np

# This algorithm is made to control the gain values for the individual genes to create the chromosomes
# Kind of like the main settings files

geneticAlg = GA()

GLOBAL_SOLUTION_ARR = [26.0, 12.34, 5.64, 53.8]
GLOBAL_SOLUTION = Chromo(parent=GLOBAL_SOLUTION_ARR)

INITIAL_MUTATION = 0.20
STANDARD_MUTATION = 0.25

# GENE Specific Mutation
qCM = STANDARD_MUTATION
qWM = STANDARD_MUTATION
qSM = STANDARD_MUTATION
qMM = STANDARD_MUTATION

# Maps array to index for GENES
GENE_MAP = {
    "qCoffee": 0,
    "qWater": 1,
    "qSugar": 2,
    "qMilk": 3
}

# we need to be able to analyze the increase in specific gene values and their corresponding fitness 
# (decrease in sugar => increase in fitness; the program should take note of this)
GENE_MUTATION_MAP = {
    0: qCM,
    1: qWM,
    2: qSM,
    3: qMM
}


class LGModel:
    def __init__(self, train_x, train_y):
        self.LGM = linear_model.LinearRegression()
        self.train_x = np.array(train_x)
        self.train_y = np.array(train_y)

    def trainModel(self):
        self.LGM.fit(self.train_x.reshape(-1, 1), self.train_y)

    def predict(self, x):
        return self.LGM.predict(x)

class Population:
    def __init__(self): # create population of n individuals
        self.population = []


        self.qCVal = []
        self.qWVal = []
        self.qSVal = []
        self.qMVal = []

        self.fitnessVal = []

        self.valueMapper = {
            0: self.qCVal,
            1: self.qWVal,
            2: self.qSVal,
            3: self.qMVal
        }

        self.qCModel = LGModel(self.qCVal, self.fitnessVal)
        self.qWModel = LGModel(self.qWVal, self.fitnessVal)
        self.qSModel = LGModel(self.qSVal, self.fitnessVal)
        self.qMModel = LGModel(self.qMVal, self.fitnessVal)

    def retrain(self):
        self.qCModel.trainModel()
        self.qWModel.trainModel()
        self.qSModel.trainModel()
        self.qMModel.trainModel()

    def GeneAssignment(self):
        tempArr = []
        for i in range(len(GLOBAL_SOLUTION_ARR)):
            currentVal = GLOBAL_SOLUTION_ARR[i]
            tempGene = Gene(currentVal, max_mutation=GENE_MUTATION_MAP.get(i))
            tempArr.append(tempGene.gene_value)
            self.valueMapper.get(i).append(tempGene.gene_value)

        print(len(self.qCVal))        
        return tempArr
    
    def parseFitness(self):
        for obj in range(len(self.population)):
            currentObj = self.population[obj]
            try:
                if(self.fitnessVal[obj] == currentObj.fitness):
                    pass
                else:
                    self.fitnessVal.append(currentObj.fitness)
            except IndexError:
                self.fitnessVal.append(currentObj.fitness)

    def createIndividual(self, recipe, genFit, sweetFit, bitterFit):
        # create individual
        tempArr = recipe
        print("\n")
        print("Population Member: %s" % (str(tempArr)))

        tempChromosome = Chromo(parent=tempArr)
        tempChromosome.fitness = genFit
        tempChromosome.sweetFit = sweetFit
        tempChromosome.bitterFit = bitterFit

        self.population.append(tempChromosome)

        self.parseFitness()
        self.retrain()

    def recipeRequested(self):
        recipe = self.GeneAssignment()
        print("We've generated your recipe: %s" % (str(recipe)))
        # Do some logic stuff to actually get the recipe and create it 

        # GPIO talk to arduino

        # get fitness
        print("How would you rate your coffee on the scale of 1 - 10?")
        generalFitness = input(">>")

        print("How sweet would you rate your coffee on the scale of 1 - 5?")
        sweetFitness = input(">>")

        print("How bitter would you rate your coffee on the scale of 1 - 5?")
        bitterFitness = input(">>")

        self.createIndividual(recipe, generalFitness, sweetFitness, bitterFitness)


GEN1 = Population()
GEN1.recipeRequested()
GEN1.qCModel.predict([[27.8]])