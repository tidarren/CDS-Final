import numpy as np
import pickle
import argparse
import utils
import logging
from os.path import dirname, join
from number_to_store_name import showStoreName

logging.basicConfig(format='%(message)s', level=logging.INFO)


parser = argparse.ArgumentParser()
parser.add_argument("-p","--pop", type=int, help="POPULATION_SIZE", default=300)
parser.add_argument("-g","--gen", type=int, help="NUM_GENERATION", default=300)
parser.add_argument("-c","--cp", type=float, help="CROSSOVER_PROBABILITY", default=0.5)
parser.add_argument("-m","--mp", type=float, help="MUTATION_PROBABILITY", default=0.5)
parser.add_argument("-r", "--RandomInit", type=int, help="Random Initialization", default=0)
parser.add_argument("-b", "--BeginPoint", type=str, help="Choose a beginning point.", default='0')
parser.add_argument("--InitPercent", type=float, help="Specify percent if not random init.", default=0.5)
args = parser.parse_args()

## Hyper parameters
GENE_LENGTH = 34
POPULATION_SIZE = args.pop
NUM_GENERATION = args.gen
CROSSOVER_PROBABILITY = args.cp
MUTATION_PROBABILITY = args.mp


def main():
    population = generatePopulation()

    for _ in range(NUM_GENERATION):
        fitnessValues = np.array(list(map(lambda x:utils.evalTravDist(x),population)))
        
        # reproduction
        population = reproduction(population, fitnessValues) 
        populationCopy = population.copy()
        for parent in population:
            parentCopy = parent.copy()
            # crossover
            child = crossover(parentCopy, populationCopy)  
            # mutation
            child = mutation(child)
            parent[:] = child  
    
    fitnessValues = np.array(list(map(lambda x:utils.evalTravDist(x),population)))
    
    return fitnessValues, population


def generatePopulation():
    """ 
    Generate 2-dim np.array designVariables
    of size (POPULATION_SIZE, GENE_LENGTH)
    """
    if args.RandomInit:
        return [list(np.random.permutation(GENE_LENGTH)) for _ in range(POPULATION_SIZE)]
    
    redundantResolution, distRedSol = utils.redundantResolution(args.BeginPoint)
    logging.debug('\nredundantResolution: {}'.format(redundantResolution))
    logging.debug('distRedSol: {}\n'.format(distRedSol))
    redundantResolution = list(map(lambda x:int(x), redundantResolution[:-1]))
    selfNum = int(POPULATION_SIZE*args.InitPercent)
    sel = [redundantResolution for _ in range(selfNum)]
    randomHalf = [list(np.random.permutation(GENE_LENGTH)) for _ in range(POPULATION_SIZE-selfNum)]
    return np.array(sel+randomHalf)


def reproduction(designVariables, fitnessValues, matingPoolSize=False):
    """
    Select mating pool. Remain good gene and remove bad gene.
    -----
    Args:
      designVariables (2-dim np.array): size (len(designVariables), geneLength)
      fitnessValues (1-dim np.array): corresponding fitness values
    
    Return:
      matingPool (2-dim np.array): size (len(designVariables), geneLength)
    """
    if not matingPoolSize:
        matingPoolSize = len(designVariables)  
    
    # target: shortest travelling distance
    # lower fitnessValue with larger prob. 
    prob = fitnessValues/fitnessValues.sum()
    proInv = 1-prob
    p = proInv/proInv.sum()
    
    idx = np.random.choice(np.arange(len(designVariables)),  
            size=matingPoolSize,
            replace=True,                        # allow sample with replacement
            p=p) # not uniform probablity 
    
    matingPool = designVariables[idx]
    return matingPool


def crossover(parent, designVariablesCopy):   
    """
    Ordered crossover. select substring from parent, 
    fill out the reminder in the order that 
    they are in designVariablesCopy 
    -----
    Args:
      parent (1-dim np.array): designVariable
      designVariablesCopy (2-dim np.array): copy of designVariables
    
    Return:
      parent (1-dim np.array): (crossovered) designVariable
    """
    if np.random.rand() < CROSSOVER_PROBABILITY:
        # select another parent
        mateIdx = np.random.randint(len(designVariablesCopy), size=1)  
        parent2 = designVariablesCopy[mateIdx,:].flatten()  

        # choose substring of parent
        geneA = int(np.random.rand() * GENE_LENGTH)
        geneB = int(np.random.rand()* GENE_LENGTH)
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        child1,child2 = [],[]
        for i in range(startGene, endGene):
            child1.append(parent[i])

        # ordered crossover    
        child2 = [item for item in parent2 if item not in child1]
        parent = child1 + child2
       
    return parent


def mutation(child):
    """
    swap mutation.
    -----
    Args:
      child (1-dim np.array): design variable
    
    Return:
      child (1-dim np.array): design variable
    """
    for swapped in range(len(child)):
        if np.random.rand() < MUTATION_PROBABILITY:
            swapWith = int(np.random.rand() * len(child))
            city1 = child[swapped]
            city2 = child[swapWith]
            child[swapped], child[swapWith] = city2, city1
    return child


def showAns(fitnessValues, population):
    bestValue = min(fitnessValues)
    bestIndex = np.argmin(fitnessValues)
    bestPath = list(population[bestIndex])
    
    logging.info('bestValue: {}'.format(bestValue))
    logging.info('bestPath:\n {}'.format(bestPath))
    logging.info('')
    showStoreName(bestPath)


if __name__ == "__main__":    
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.info('=== Parameters ===\n')
    logging.info(' POPULATION_SIZE: {}'.format(POPULATION_SIZE))
    logging.info(' NUM_GENERATION: {}'.format(NUM_GENERATION))
    logging.info(' CROSSOVER_PROBABILITY: {}'.format(CROSSOVER_PROBABILITY))
    logging.info(' MUTATION_PROBABILITY: {}'.format(MUTATION_PROBABILITY))
    logging.info(' RandomInit: {}'.format(args.RandomInit==1))
    logging.info(' ')
    logging.info('\n')
    logging.info('=== Results ===\n')
    fitnessValues, population = main()
    showAns(fitnessValues, population)