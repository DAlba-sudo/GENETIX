from Population import Population
from ChromoV3 import ChromoV3 as Chromo, Gene
from GACodeBase import GA
import os
from FileHandler import FileHandler

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation 
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


Window.clearcolor = (1, 1, 1, 1)

# class instantiation
fH = FileHandler()
ENVIRON = Population()
GENETIC_ALG = GA()

# Load all data from folders
BASE_DIR = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(BASE_DIR, "DATA/")
try:
    os.mkdir(DATA_FOLDER)
except FileExistsError:
    pass

POPULATION = os.path.join(DATA_FOLDER, "population.txt")

# Variable Assignment
start_recipe = [0.9, 0.12, 0.87, 0.65]

# acutal data is loading
with open(POPULATION, "r") as f:
    lines = f.readlines()

    for line in range(len(lines)):
        current_line = lines[line]
        left_bracket_removed = fH.elimFromString("[", current_line)
        right_bracket_removed = fH.elimFromString("]", left_bracket_removed)
        subString = right_bracket_removed.split(",")
        tempArr = []
        for gene in range(len(subString)):
            current_gene = subString[gene]
            tempArr.append(float(current_gene))
        ENVIRON.addIndividual(Chromo(array=tempArr))
    
    ENVIRON.updateData()

def create_individual(self):
        # step 1: generate recipe (slight adaption)
        current_recipe = None
        if(len(ENVIRON.globalPopulation) < 10):
            current_recipe = self.create_recipe(slightAdaption=True, max_mutation=0.10)
        else:
            parent_arrays = ENVIRON.stochastic_selection()
            P1 = parent_arrays[0]
            P2 = parent_arrays[1]

            current_recipe = GENETIC_ALG.crossOver(chromo1=P1, chromo2=P2)
        
        print("This is the current recipe: %s" %(str(current_recipe)))
        # step 2: use arduino to create recipe

        # step 3: get recipe feedback
        current_recipe.append(create_fitness())

        # step 4: save data
        ENVIRON.addIndividual(Chromo(array=current_recipe))
        ENVIRON.updateData()

class GENETIX(Screen):

    def create_recipe(self, slightAdaption, max_mutation):
        # Most Recent Member
        MRM = ENVIRON.globalPopulation[(len(ENVIRON.globalPopulation)-1)]
        tempCoffee = Gene(MRM.qCoffee.value, max_mutation=max_mutation, slightAdaption=slightAdaption)
        tempWater = Gene(MRM.qWater.value, max_mutation=max_mutation, slightAdaption=slightAdaption)
        tempSugar = Gene(MRM.qSugar.value, max_mutation=max_mutation, slightAdaption=slightAdaption)
        tempMilk = Gene(MRM.qMilk.value, max_mutation=max_mutation, slightAdaption=slightAdaption)
        
        tempArray = [tempCoffee.value, tempWater.value, tempSugar.value, tempMilk.value]

        return tempArray

    

    def create_individual(self):
        # step 1: generate recipe (slight adaption)
        current_recipe = None
        if(len(ENVIRON.globalPopulation) < 10):
            current_recipe = self.create_recipe(slightAdaption=True, max_mutation=0.10)
        else:
            parent_arrays = ENVIRON.stochastic_selection()
            P1 = parent_arrays[0]
            P2 = parent_arrays[1]

            current_recipe = GENETIC_ALG.crossOver(chromo1=P1, chromo2=P2)
        
        os.system('clear')
        print("This is the current recipe: %s" %(str(current_recipe)))
        print("\n")
        print("COFFEE: %s" % (str(current_recipe[0])))
        print("WATER: %s" % (str(current_recipe[1])))
        print("SUGAR: %s" % (str(current_recipe[2])))
        print("MILK: %s" % (str(current_recipe[3])))
        print("\n")
        # step 2: use arduino to create recipe

        
        # step 3: get recipe feedback
        current_recipe.append(float(input("What would you rate the coffee recipe?")))

        # step 4: save data
        ENVIRON.addIndividual(Chromo(array=current_recipe))
        ENVIRON.updateData()
    

class GenetixApp(App):

    def build(self):
        return GENETIX()

if __name__ == '__main__':
    GenetixApp().run()