from chromosomeV2 import Gene
from chromosomeV2 import Chromo
from GACodeBase import GA

# This algorithm is made to control the gain values for the individual genes to create the chromosomes
# Kind of like the main settings files

GLOBAL_SOLUTION_ARR = [26.0, 12.34, 5.64, 53.8]
GLOBAL_SOLUTION = Chromo(parent=GLOBAL_SOLUTION_ARR)

# Maps array to index for GENES
GENE_MAP = {
    "qCoffee": 0,
    "qWater": 1,
    "qSugar": 2,
    "qMilk": 3
}

#we need to be able to analyze the increase in specific gene values and their corresponding fitness (decrease in sugar => increase in fitness; the program should take note of this)



INITIAL_MUTATION = 0.20

geneticAlg = GA()

class Population:
    def __init__(self, n): # create population of n individuals
        self.population = []
        while (len(self.population) != n):
            # create individual
            tempArr = []

            for i in range(len(GLOBAL_SOLUTION_ARR)):
                currentVal = GLOBAL_SOLUTION_ARR[i]
                tempArr.append(Gene(currentVal, max_mutation=INITIAL_MUTATION).gene_value)
            
            self.population.append(Chromo(parent=tempArr))
            print("Current Population Member: %s" % str(tempArr))


generation1 = Population(10)
par1 = generation1.population[0]
par2 = generation1.population[1]

child = geneticAlg.crossOver(par1, par2)
print(child.exportToArr())

                