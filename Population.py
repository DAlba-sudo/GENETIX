from CoffeeChromo import CoffeeChromo
from operator import add, sub
from FileHandler import FileHandler
import random
import os

# Population Class Blueprint
class Population:
    def __init__(self, n):
        self.population_members = [] # population_members is a list where all members of population are stored
        self.n = n # n represents the number of members per population

        # PATH Configuration for the population to load and export data (need to add generalization features)
        BASE_PATH = os.path.dirname(__file__)
        DATA_FOLDER_PATH = os.path.join(BASE_PATH, "DATA/")

        self.PATHS = {
            "default": os.path.join(DATA_FOLDER_PATH, "population.txt")
        }

        self.fh = FileHandler()
    
    # this currently serves as our function to export data to the population.txt file
    def exportPopulationToArray(self, path=None):
        tempArray = [] # tempArray holds our temporary population

        # iterates through each member of our current population
        for member in range(len(self.population_members)):
            tempMember = []
            current_member = self.population_members[member]

            # iterates through each GENE Object in our current member and appends it to the our
            # tempMember array which is used as an array representation of our Chromosome
            for itm in range(len(current_member.GENES.keys())):
                current_key_dict = current_member.GENES.keys()
                current_key = list(current_key_dict)[itm]

                tempMember.append(current_member.getValue(current_key))

            # writes to the file
            if(path is not None):
                with open(self.PATHS[path], "a+") as f:
                    f.write(str(tempMember) + "\n")
                    f.flush()
            else:
                with open(self.PATHS['default'], "a+") as f:
                    f.write(str(tempMember) + "\n")
                    f.flush()

    # Defines rules for creating members of the population (Must be overwritten)
    def createMember(self):
        raise Exception("Declaration Error: createMember function must be overriden!")
    
    # Method called to create population
    def createPopulation(self):
        for i in range(self.n):
            tempMember = self.createMember()
            self.population_members.append(tempMember)

# Example of how a generation would be created
class Generation(Population):
    def __init__(self, n):
        Population.__init__(self, n)

        self.accepted_solution = CoffeeChromo()
        self.accepted_solution.updateValue("qC", 15)
        self.accepted_solution.updateValue("qS", 17)
        self.accepted_solution.updateValue("qW", 150)

        # Mutation Tuner
        self.MAX_MUTATION = 0.95
        self.MUTATION_TUNER = 0.90

    def changeMaxMutation(self, value):
        self.MAX_MUTATION = value
    
    def changeMutationTuner(self, value):
        self.MUTATION_TUNER = value

    def createMember(self, mutation=None):
        temp_recipe = CoffeeChromo()
            
        for itm in range(len(temp_recipe.GENES.keys())):
            current_key_dict = temp_recipe.GENES.keys()
            current_key = list(current_key_dict)[itm]
            temp_recipe.updateValue(key=current_key, value=self.mutatedValue(self.accepted_solution.getValue(current_key), max_mutation=mutation))            
        
        print("Here is an individual: ")
        temp_recipe.display()
        print("\n")

        return temp_recipe

    def createPopulation(self):
        for i in range(self.n):
            tempMember = self.createMember(self.MAX_MUTATION - ((self.MUTATION_TUNER)*(self.MAX_MUTATION*(i/self.n)))) # find a way to set the mutation
            self.population_members.append(tempMember)

    def mutatedValue(self, value, max_mutation = None):
        ops = [add, sub]
        if (max_mutation is None):
            mutation = random.random()
            while(mutation > 0.33):
                mutation = random.random()
            
            op = random.choice(ops)
            print("Here is the mutation: " + str(mutation))
            return op(value, (value*mutation))
        else :
            mutation = random.random()
            while(mutation > max_mutation):
                mutation = random.random()
            
            op = random.choice(ops)
            print("Here is the mutation: " + str(mutation))
            return op(value, (value*mutation))
    
# if __name__ == "__main__":
#     g = Generation(100)
#     g.createPopulation()
#     g.exportPopulationToArray()




     