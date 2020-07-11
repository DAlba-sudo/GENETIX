import random
import numpy as np

#a gene is a specific attribute 

class Gene:
	def __init__(self, foreVal, bias=None):
		if(bias is None):
			self.bias  = 1.0
		else:
			self.bias = bias
			
		self.gene_value = self.setVal(foreVal)
	
	def rangeClip(self, val, minV, maxV):
		targetV = val
		if(val < minV):
			targetV = minV	
		if(val > maxV):
			targetV = maxV
		return targetV
	
	def setVal(self, foreVal):
		randVal = random.random()
		processedVal = self.rangeClip(randVal, 0.95, 1.05)
		print("value = " + str(processedVal))
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
	def __init__(self, arr=None, parentChromosome1=None, parentChromosome2=None, globalSolution=None):
		
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
		elif ((parentChromosome1 is not None) and (globalSolution is not None)):
			self.primaryParent = parentChromosome1
			self.secondaryParent = globalSolution
			
			self.createChild()
		elif ((parentChromosome2 is not None) and (globalSolution is not None)):
			self.primaryParent = parentChromosome2
			self.secondaryParent = globalSolution
			
			self.createChild()
		#if two parents are supplied => supply parent information
		elif ((parentChromosome1 is not None) and (parentChromosome2 is not None)):
			self.primaryParent = parentChromosome1
			self.secondaryParent = parentChromosome2
			
			self.createChild()
		elif (arr is not None):
			self.translateFromArray(arr)
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
	
	#translates geneInfo into an array containing only information needed to create the coffee
	def translateToRecipe(self, chromo=None):
		
		#if chromo is not supplied, assume you are translating yourself
		if (chromo is None):
			return [self.qCoffee, self.qWater, self.qCreamer, self.qSugar, self.qMilk, self.brewRate]
		#if chromo is supplied, assume you are translating the chromosome
		else:
			return [chromo.qCoffee, chromo.qWater, chromo.qCreamer, chromo.qSugar, chromo.qMilk, chromo.brewRate]

	def translateFromArray(self, arr):
		self.qCoffee = Gene(arr[0])
		self.qWater = Gene(arr[1])
		self.qCreamer = Gene(arr[2])
		self.qSugar = Gene(arr[3])
		self.qMilk = Gene(arr[4])
		self.brewRate = Gene(arr[5])
			

	#given the length of an array choose a random spot to split it
	def selectCrossoverPoint(self, lengthArr):
		minVal = 0; # this is minimum index we want to split at
		return np.random.randint(0, lengthArr)	
			
	
	def crossover(self):
		# arrays are assigned (this allows us to manipulate the vars)
		primArray = translateToRecipe(self.primaryParent)
		secondArray = translateToRecipe(self.secondaryParent)
		
		#pick crossover point
		crossOverPoint = selectCrossoverPoint(len(primArray))
		
		#create sublists of each array
		preSplit1 = primArray[0:crossOverPoint]
		postSplit1 = primArray[crossOverPoint:]
		preSplit2 = secondArray[0:crossOverPoint]
		postSplit2 = secondArray[crossOverPoint:]
		
		#pick one of primary and one of remainder and create child
		preSelector = np.random.randint(1,3)
		postSelector = np.random.randint(1,3)
		
		childPre = None
		childPost = None
	
		#combine according to selectors
		if (preSelector == 1):
			childPre = preSplit1
		else:
			childPre = preSplit2
		
		if (postSelector == 1):
			childPost = postSplit1
		else:
			childPost = postSplit2
		
		return childPre + childPost
		
		
	#function used to create the child from the two parents
	def createChild(self):
		#if there are two parents do the following:
		if((self.primaryParent is not None) and (self.secondaryParent is not None)):
			newRecipeArr = crossover()
			translateFromArray(newRecipeArr)
		else:
			raise Exception("Can't create child. Need two parents!")
			 
