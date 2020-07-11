import Random

#a gene is a specific attribute 

class Gene:
	def __init__(self, foreVal, bias=None):
		self.gene_value = setVal(foreVal)
		if(bias is None):
			self.bias  = 1.0
		else:
			self.bias = bias
		
	def setVal(self, foreVal):
		randVal = random()
		value = (randVal*foreVal) * self.bias
		return value
		
# --------------------------------------------

# chromosome is a recipe

# A recipe has to have the following:
#	- Quantity of Coffee, Water, Creamer/Sugar, Milk.
#	- Brew Rate (How fast the motor pulls water through)
#	- Fitness Rating
#	- Parent Information

# --------------------------------------------	

class Chromosome:
	def __init__(self, parentChromosome1=None, parentChromosome2=None, globalSolution=None):
		
		#Values being stored in the chromosome
		#Quantity related values
		self.qCoffee = None
		self.qWater = None
		self.qCreamer = None
		self.qSugar = None
		self.qMilk = None
		
		#Process related values
		self.brewRate = None
		
		#GA specific values
		self.fitnessRating = None
		self.primaryParent = None
		self.secondaryParent = None
				
		#assigning parents of chromosome
		#if globalSolution is supplied and no parents => create child through asexual reproduction
		if((globalSolution is not None and (parentChromosome1 is None)) and (globalSolution is not None and (parentChromosome2 is None))):
			workingChromosome = globalSolution
			inheritFromChromosome(workingChromosome)
		#if global solution is supplied with a parent => supply parent information 
		else if ((parentChromosome1 is not None) and (globalSolution is not None)):
			self.primaryParent = parentChromosome1
			self.secondaryParent = globalSolution
		else if ((parentChromosome2 is not None) and (globalSolution is not None)):
			self.primaryParent = parentChromosome2
			self.secondaryParent = globalSolution
		#if two parents are supplied => supply parent information
		else if ((parentChromosome1 is not None) and (parentChromosome2 is not None)):
			self.primaryParent = parentChromosome1
			self.secondaryParent = parentChromosome2
		#if no parents are supplied raise error
		else:
			raise Exception("Sorry, this is an event that we were not prepared for! Attempting to fix the problem as soon as possible...")
	
	#function for inheriting standard values from a parent through mutation
	def inheritFromChromosome(self, chromo):
		self.qCoffee = Gene(chromo.qCoffee)
		self.qWater = Gene(chromo.qWater)
		self.qCreamer = Gene(chromo.qCreamer)
		self.qSugar = Gene(chromo.qSugar)
		self.qMilk = Gene(chromo.qMilk)
		
		self.brewRate = Gene(chromo.brewRate)
	
