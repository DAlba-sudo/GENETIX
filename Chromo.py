class Gene:
    def __init__(self, gene_value, gene_name):
        self.value = gene_value
        self.name = gene_name

class Chromo( object ):
    def __init__(self):
        self.GENES = {

        }

    def addGene(self, gene_name):
        self.GENES[gene_name] = Gene(None, gene_name)

    def display(self):
        for keys in self.GENES:
            print("%s -> %s" % (str(keys), str(self.GENES[keys].value)))


    
        

    
