# imports
from ChromoV3 import ChromoV3
import os

class Population:
    def __init__(self):

        self.globalPopulation = [] # all individuals are stored here
        
        self.qCValues = [] # a list of all the coffee values
        self.qWValues = [] # a list of all the water values 
        self.qSValues = [] # a list of all the sugar quantity values
        self.qMValues = [] # a list of all the milk quantity values

        self.general_fitness = [] # A list of all the fitness

        # Load all data from folders
        self.BASE_DIR = os.path.dirname(__file__)

        self.DATA_FOLDER = os.path.join(self.BASE_DIR, "DATA/")
        try:
            os.mkdir(self.DATA_FOLDER)
        except FileExistsError:
            pass

        self.POPULATION = os.path.join(self.DATA_FOLDER, "population.txt")

    def addIndividual(self, indiv):
        # indiv is assumed to be a chromosome
        self.globalPopulation.append(indiv)
        self.qCValues.append(indiv.qCoffee.value)
        self.qWValues.append(indiv.qWater.value)
        self.qSValues.append(indiv.qSugar.value)
        self.qMValues.append(indiv.qMilk.value)
        self.general_fitness.append(indiv.fitness)

    def updateData(self):
        with open(self.POPULATION, "w") as f:
            for obj in range(len(self.globalPopulation)):
                indiv = self.globalPopulation[obj]
                f.write(str(indiv.translateToArray()))
                f.write("\n")
                f.flush()
# Example Init of above class



