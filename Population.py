# imports
from ChromoV3 import ChromoV3
import os
import random

class Population:
    def __init__(self):

        self.globalPopulation = [] # all individuals are stored here
        self.intermediatePopulation = [] # all individuals before recombination

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
                f.write(str(indiv.translateToArrayFit()))
                f.write("\n")
                f.flush()

    def within(self, randFloat, min_range, max_range):
        return ((randFloat<max_range) and (randFloat>min_range))

    def populateIntermediate(self):
        self.intermediatePopulation = []
        rel_fit = 0
        for fit in range(len(self.general_fitness)):
            current_fit = self.general_fitness[fit]
            rel_fit += current_fit
        
        rel_fit = rel_fit / len(self.general_fitness)

        while( len(self.intermediatePopulation) < (2*( len(self.globalPopulation) )) ):
            for j in range(len(self.globalPopulation)):
                current_indiv = self.globalPopulation[j]
                current_indiv_rel_fit = current_indiv.fitness/rel_fit
                equilizer = random.random()
                if(current_indiv_rel_fit > equilizer):
                    self.intermediatePopulation.append(current_indiv)
                else:
                    pass

    def create_rel_fit(self):
        rel_fit = 0
        for fit in range(len(self.general_fitness)):
            current_fit = self.general_fitness[fit]
            rel_fit += current_fit
        
        rel_fit = rel_fit / len(self.general_fitness)
        return rel_fit

    def calculate_artificial_fitness(self, recipe):
        starting_point = [28.0, 2.4, 1.4, 0.9, 0.4]
        ideal_formula = [35, 3, 0.1, 0.1]

        stnd_error = 0
        recipe_error = 0

        for recipe_itm in range(len(recipe)):
            current_recipe_itm = recipe[recipe_itm]
            stnd_err = (starting_point[recipe_itm] - ideal_formula[recipe_itm])/ideal_formula[recipe_itm]
            recipe_err = (current_recipe_itm - ideal_formula[recipe_itm])/ideal_formula[recipe_itm]

            stnd_error += stnd_err
            recipe_error += recipe_err
        
        stnd_err_avg = stnd_error / (len(recipe))
        recipe_err_avg = recipe_error / len(recipe)

        error_dif = abs((stnd_err_avg) - (recipe_err_avg))
        return 0.4*error_dif

    def randomSelectFromArray(self, arr):
        equilizer = random.random()
        for itm in range(len(arr)):
            min_thresh = itm/len(arr)
            diff_thresh = 1/len(arr)
            max_thresh = min_thresh + diff_thresh

            if(self.within(equilizer, min_thresh, max_thresh)):
                return arr[itm]
            else:
                pass

    def stochastic_selection(self):
        self.populateIntermediate()

        P1 = self.randomSelectFromArray(self.intermediatePopulation)
        P2 = self.randomSelectFromArray(self.intermediatePopulation)
        while(P1 is P2):
            P2 = self.randomSelectFromArray(self.intermediatePopulation)

        return [P1, P2]
# Example Init of above class



