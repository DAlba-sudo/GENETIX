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
    tempCoffee = Gene(MRM.qCoffee.value, GENERON.COFFEE_MUTATION, 0.3, True)
    tempWater = Gene(MRM.qWater.value, GENERON.WATER_MUTATION, 0.3, True)
    tempSugar = Gene(MRM.qSugar.value, GENERON.SUGAR_MUTATION, 0.3, True)
    tempMilk = Gene(MRM.qMilk.value, GENERON.MILK_MUTATION, 0.3, True)

    # create the recipe IRL
    # arduinoStuff()

    # get fitness 
    fitness = input("How was the recipe?")
    fitness = int(fitness)
    
    tempArray = [tempCoffee, tempWater, tempSugar, tempMilk, fitness]
    tempChromo = Chromo(tempArray)

    GENERON.addIndividual(tempChromo)

def displayAll():
    for itm in range(len(GENERON.general_fitness)):
        current_population_member = GENERON.globalPopulation[itm]
        print("Population Memebr #%s" % str(itm))
        print("\n")
        print("Coffee Value: " + str(current_population_member.qCoffee.value))
        print("Water Value: " + str(current_population_member.qWater.value))
        print("Sugar Value: " + str(current_population_member.qSugar.value))

def main():
    print("Here are your options: ")
    print("    (1): Create New Recipe")
    print("    (2): Display Population Data")
    print("    (3): Exit")
    print("")
    opt = input("What would you like to do: ")
    if(int(opt) == 1):
        create_recipe()
    elif(int(opt)== 2):
        displayAll()
    else:
        main()
    main()
    
if __name__ == "__main__":
    main()