import random
from operator import add, sub

class Gene:
    def __init__(self, gene_value, gene_name, gene_mutation = None, mutation_cap = None):
        self.value = gene_value
        self.name = gene_name

        # mutation cap setter
        if(mutation_cap is not None):
            self.mutation_cap = mutation_cap
        else:
            self.mutation_cap = 0.30

        # Parameter Error in case of user mistake
        if (mutation_cap is not None) and (gene_mutation is None):
            raise Exception("PARAMETER ERROR: mutation_cap is set but gene_mutation is None")
        elif ((mutation_cap is not None) and (gene_mutation is not None)):
            # guaranteed mutation of gene when gene_mutation parameter is set to TRUE
            if (gene_mutation):
                self.value = self.mutatedValue(self.value, max_mutation=self.mutation_cap)
            # if gene_mutation is set to FALSE
            elif (not gene_mutation):
                coin_guess = random.random()
                real_guess = random.random()
                # "random coin flip to see if mutation is applied"
                if (coin_guess > real_guess):
                    self.mutation_cap = 0.15
                    self.value(self.mutatedValue(self.value, max_mutation=self.mutation_cap))
                # if mutation fails to occur do nothing to the value
                else:
                    pass
        else:
            pass

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

class Chromo( object ):
    def __init__(self):
        self.GENES = {

        }

    def addGene(self, gene_name):
        self.GENES[gene_name] = Gene(None, gene_name)

    def display(self):
        for keys in self.GENES:
            print("%s -> %s" % (str(keys), str(self.GENES[keys].value)))

    def exportGeneToArray(self):
        tempMember = []

        # iterates through each GENE Object in our current member and appends it to the our
        # tempMember array which is used as an array representation of our Chromosome
        for itm in range(len(self.GENES.keys())):
            current_key_dict = self.GENES.keys()
            current_key = list(current_key_dict)[itm]

            tempMember.append(self.getValue(current_key))
        
        return tempMember


    
        

    
