from CoffeeChromo import CoffeeChromo
from operator import add, sub
from FileHandler import FileHandler
from math import floor
import random
import os

# Population Class Blueprint
class Population:
    def __init__(self, n):
        self.population_members = [] # population_members is a list where all members of population are stored
        self.n = n # n represents the number of members per population

        # PATH Configuration for the population to load and export data (need to add generalization features)
        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_FOLDER_PATH = os.path.join(self.BASE_PATH, "DATA/")

        self.PATHS = {
            "default": os.path.join(self.DATA_FOLDER_PATH, "population.txt")
        }

        self.fh = FileHandler()
    

    
    # this currently serves as our function to export data to the population.txt file
    # def exportPopulationToArray(self, path=None):
    #     tempArray = [] # tempArray holds our temporary population

    #     # iterates through each member of our current population
    #     for member in range(len(self.population_members)):
    #         current_member = self.population_members[member]
            
    #         tempMember = current_member.exportGeneToArray()

    #         # writes to the file
    #         try:
    #             if(path is not None):
    #                 with open(self.PATHS[path], "a+") as f:
    #                     f.write(str(tempMember) + "\n")
    #                     f.flush()
    #             else:
    #                 with open(self.PATHS['default'], "a+") as f:
    #                     f.write(str(tempMember) + "\n")
    #                     f.flush()
    #         except KeyError:
    #             self.PATHS[path] = os.path.join(self.DATA_FOLDER_PATH, (str(path) + ".txt"))

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
    def __init__(self, n, gen_path=None):
        Population.__init__(self, n) # initializes the population with n

        # Creates the already accepted solution with appropiate values
        self.accepted_solution = CoffeeChromo()
        self.accepted_solution.updateValue("qC", 15)
        self.accepted_solution.updateValue("qS", 17)

        # Max Mutation is how much the value is allowed to change
        self.MAX_MUTATION = 0.95
        # Mutation Tuner is used to fine-tune the mutation (lower values lower mutation)
        self.MUTATION_TUNER = 0.90

        # Method used to change max mutation
    def changeMaxMutation(self, value):
        self.MAX_MUTATION = value
    
    # method used to change mutation tuner 
    def changeMutationTuner(self, value):
        self.MUTATION_TUNER = value

    # override of the createMember from Population class
    def createMember(self, method, mutation_cap=None):
        # tempRecipe is created as placeholder
        temp_recipe = CoffeeChromo()
        
        # assigns mutations to each gene based off of the genes from the accepted solution
        for itm in range(len(temp_recipe.GENES.keys())):
            current_key_dict = temp_recipe.GENES.keys() # gets the current dictionary's keys
            current_key = list(current_key_dict)[itm] # this is the current key that the for loop is looking at
            # Updates the value of the temporary recipe's current key to match that of the mutated accepted solution's current key 
            temp_recipe.updateValue(key=current_key, value=self.accepted_solution.getValue(current_key), gene_mutation=True, mutation_cap=mutation_cap)           
        
        # TELEMETRY (NOT NEEDED)
        print("Here is an individual: ")
        temp_recipe.display()
        print("\n")

        return temp_recipe # returns the temporary recipe to be appended

    # create population is to be treated like an init for the population class
    # in this it's overriden in order to change the mutation and add a variation of 
    # simulated annealing
    def createPopulation(self, method):
        if(str(method).lower()=="asexual"):
            for i in range(self.n): # iterates until all individuals have been created
                # creates a member using rules outlined in the createMember method
                # difference here being that it uses slight annealing for mutation
                tempMember = self.createMember(method=method ,mutation_cap=(self.MAX_MUTATION - ((self.MUTATION_TUNER)*(self.MAX_MUTATION*(i/self.n))))) # find a way to set the mutation
                self.population_members.append(tempMember)
        elif(str(method).lower()=="crossover"):
            # import last population
            
            # 
            pass
        else:
            raise Exception("Unplanned Scenario for population creation")

    # logic choosing individuals to test
    def stochasticSelection(self, n):
        counter = 0
        tempPop = []
        n_counter = len(tempPop)
        while(n_counter < n):
            equilizer = random.random()
            target_index = floor((equilizer * (len(self.population_members))))
            target_member = (self.population_members[target_index])
            flag = False
            for mem in range(len(tempPop)):
                current_mem = tempPop[mem]
                if (target_member == current_mem):
                    flag = True
                else:
                    pass
            if(flag):
                pass
            else:
                tempPop.append(target_member)
                print("STOCHASTIC REPLICATED: ")
                target_member.display()
                print("\n")
            n_counter = len(tempPop)
        
        return tempPop


    
# Example of how it can be used!
if __name__ == "__main__":
    g = Generation(100)
    g.createPopulation(method="ASEXUAL")
    g.stochasticSelection(37)
    g.fh.exportToPath(path="TEST2", population=g.population_members)



     