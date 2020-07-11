from chromosome import Chromosome

arr = [0.9, 81, 12, 23, 12, 15]

chromo = Chromosome(arr=arr)
print("Here is the original value: 0.9")
print("Here is the new value: " + str(chromo.qCoffee.gene_value))

