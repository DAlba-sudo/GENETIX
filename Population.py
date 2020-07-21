# imports
from linearRegressionAlg import LinearRegression
from ChromoV3 import ChromoV3

class Population:
    def __init__(self):
        self.BIAS_TUNER = 0.7

        self.globalPopulation = [] # all individuals are stored here
        
        self.qCValues = [] # a list of all the coffee values
        self.qWValues = [] # a list of all the water values 
        self.qSValues = [] # a list of all the sugar quantity values
        self.qMValues = [] # a list of all the milk quantity values

        self.general_fitness = [] # A list of all the fitness
    
        self.qCModel = LinearRegression(x_values=self.qCValues, y_values=self.general_fitness)
        self.qWModel = LinearRegression(x_values=self.qWValues, y_values=self.general_fitness)
        self.qSModel = LinearRegression(x_values=self.qSValues, y_values=self.general_fitness)
        self.qMModel = LinearRegression(x_values=self.qMValues, y_values=self.general_fitness)

        self.COFFEE_MUTATION = self.calculateBias(self.qCModel)
        self.WATER_MUTATION = self.calculateBias(self.qWModel)
        self.SUGAR_MUTATION =self.calculateBias(self.qSModel)
        self.MILK_MUTATION =self.calculateBias(self.qMModel)
        
        self.GENE_MUTATION = {
            0: self.COFFEE_MUTATION,
            1: self.WATER_MUTATION,
            2: self.SUGAR_MUTATION,
            3: self.MILK_MUTATION
        }

        self.MODEL_MAPPER = {
            0: self.qCModel,
            1: self.qWModel,
            2: self.qSModel,
            3: self.qMModel
        }
        
    def calculateBias(self, model):
        # This function calculates the bias based on the slope of the LR model
        # meaning, the more steep (i.e, the more correlation) the more strength
        # and thus the more bias
        slope = model.b1
        print("This is the slope of the line: "+str(slope))
        return slope

    def addIndividual(self, indiv):
        # indiv is assumed to be a chromosome
        self.globalPopulation.append(indiv)
        self.qCValues.append(indiv.qCoffee)
        self.qWValues.append(indiv.qWater)
        self.qSValues.append(indiv.qSugar)
        self.qMValues.append(indiv.qMilk)
        self.general_fitness.append(indiv.fitness)

        self.qCModel = LinearRegression(x_values=self.qCValues, y_values=self.general_fitness)
        self.qWModel = LinearRegression(x_values=self.qWValues, y_values=self.general_fitness)
        self.qSModel = LinearRegression(x_values=self.qSValues, y_values=self.general_fitness)
        self.qMModel = LinearRegression(x_values=self.qMValues, y_values=self.general_fitness)

        for model in range(len(self.MODEL_MAPPER)):
            if(model == 0):
                pass
            if(model == 1):
                pass
            if(model == 2):
                self.qSModel.build_model()
                self.SUGAR_MUTATION = self.qSModel.b1
            if(model == 3):
                pass


chromo1 = ChromoV3(array=[0.08, .226, 7.21, 2.15, .3])
chromo2 = ChromoV3(array=[0.08, .226, 6.4, 21.5, .5])
chromo3 = ChromoV3(array=[0.08, .226, 5.7, 21.5, .6])
chromo4 = ChromoV3(array=[0.08, .226, 4.9, 21.5, .8])
chromo5 = ChromoV3(array=[0.08, .226, 2.9, 21.5, .7])
chromo6 = ChromoV3(array=[0.08, .226, 3.9, 21.5, .9])

GEN1 = Population()
GEN1.addIndividual(chromo1)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
GEN1.addIndividual(chromo2)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
GEN1.addIndividual(chromo3)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
GEN1.addIndividual(chromo4)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
GEN1.addIndividual(chromo5)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
GEN1.addIndividual(chromo6)
print("SUGAR Mutation %s" % GEN1.SUGAR_MUTATION)
