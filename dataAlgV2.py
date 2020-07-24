# This will observe the data found in a population
# 
# Functions include:
# - Create Linear Regression algorithms to control bias of each type of gene
#    * Steps needed to achieve this:
#         - Before creating a linear regression algorithm we first need data
#                  - When creating an individual we need to "rebuild" the LR model 

from Population import Population
from ChromoV3 import ChromoV3 as Chromo
from ChromoV3 import Gene

GENERON = Population()
general_solution = [Gene(.14, slightAdaption=False), Gene(.72, slightAdaption=False), Gene(.87, slightAdaption=False), Gene(.12, slightAdaption=False), 0]
CHGeneral = Chromo(array=general_solution)
GENERON.addIndividual(CHGeneral)


def create_recipe():
    # Most Recent Member
    MRM = GENERON.globalPopulation[(len(GENERON.globalPopulation)-1)]
    tempCoffee = Gene(MRM.qCoffee.value, max_mutation=0.3, slightAdaption=True)
    tempWater = Gene(MRM.qWater.value, max_mutation=0.3, slightAdaption=True)
    tempSugar = Gene(MRM.qSugar.value, max_mutation=0.3, slightAdaption=True)
    tempMilk = Gene(MRM.qMilk.value, max_mutation=0.3, slightAdaption=True)

    # create the recipe IRL
    # arduinoStuff()

    # get fitness 
    fitness = input("How was the recipe?")
    fitness = int(fitness)
    
    tempArray = [tempCoffee, tempWater, tempSugar, tempMilk, fitness]
    tempChromo = Chromo(tempArray)

    GENERON.addIndividual(tempChromo)