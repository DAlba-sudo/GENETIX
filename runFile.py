from Population import Population
from ChromoV3 import ChromoV3 as Chromo, Gene
from GACodeBase import GA
import os
from FileHandler import FileHandler

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

Window.clearcolor = (1, 1, 1, 1)

# class instantiation
fH = FileHandler()
ENVIRON = Population()

# Load all data from folders
BASE_DIR = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(BASE_DIR, "DATA/")
try:
    os.mkdir(DATA_FOLDER)
except FileExistsError:
    pass
POPULATION = os.path.join(DATA_FOLDER, "population.txt")

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

class GENETIX(FloatLayout):
    pass

class GenetixApp(App):
    def build(self):
        return GENETIX()

if __name__ == '__main__':
    GenetixApp().run()