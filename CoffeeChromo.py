from Chromo import Chromo, Gene
import random
from operator import add, sub
from FileHandler import FileHandler
import os

class CoffeeChromo(Chromo):
    def __init__(self):
        Chromo.__init__(self)
        Chromo.addGene(self, "qC")
        Chromo.addGene(self, "qS")

    def getValue(self, key):
        return self.GENES[str(key)].value

    def updateValue(self, key, value, gene_mutation=None, mutation_cap=None):
        self.GENES[str(key)] = Gene(gene_value=value, gene_name=key, gene_mutation = gene_mutation, mutation_cap = mutation_cap)

    def displayAllGenes(self):
        print(self.GENES.keys())

