# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import utils
import pickle
import logging
import argparse
from os.path import dirname, join
from number_to_store_name import showStoreName



parser = argparse.ArgumentParser()
parser.add_argument("-i","--iter", type=int, help="Iteration", default=300)
parser.add_argument("-t","--ttf", type=float, help="Temperature_Threshold_Factor", default=0.05)
parser.add_argument("-r","--trf", type=float, help="Temperature_Reduction_Factor", default=0.5)
parser.add_argument("-b","--bc", type=float, help="Boltzmann_Constant", default=1.)
parser.add_argument("--RandomInit", type=int, help="Random Initialization", default=0)
parser.add_argument("--BeginPoint", type=str, help="Choose a beginning point.", default='0')
args = parser.parse_args()

logging.basicConfig(format='%(message)s', level=logging.INFO)

# %% [markdown]
# ### Hyperparameters

# %%
Temperature_Reduction_Factor = args.trf
Boltzmann_Constant = args.bc
Iteration = args.iter
# determine the Temperature_Threshold 
Temperature_Threshold_Factor = args.ttf
Num_Location = 34
RandomInit = args.RandomInit
BeginPoint = args.BeginPoint

# ### Step 0 & 1

# %%
def initConfig():
    """
    Intialize design vector.
    """
    if RandomInit:
        designVector = np.arange(Num_Location)
        np.random.shuffle(designVector)
    else:
        designVector, _ = utils.redundantResolution(BeginPoint)
        designVector = np.array(designVector[:-1]).astype(int)
    return designVector


def initTemperature(numOfPt=4):
    """
    Initialize temperature.
    """
    temperatures = []
    for _ in range(numOfPt):
        designVector = initConfig()
        temperature = utils.evalTravDist(designVector)
        temperatures.append(temperature)
    return np.mean(temperatures)

# %% [markdown]
# ### Step 2

# %%
def perturbConfig(designVector):
    """
    Generate a new design point by swapping.
    """
    while True:
        n1 = int(np.random.randint(0,Num_Location,1))
        n2 = int(np.random.randint(0,Num_Location,1))
        if n1 != n2:
            break
    designVector[n1], designVector[n2] = designVector[n2], designVector[n1]
    return designVector

# %% [markdown]
# ### Step 3

# %%
def metropolisCriterion(newDesignVector, designVector, temperature):
    """
    Determine whether keep the higher desgin vector or not.
    """
    diff = computeEnergyDiff(designVector, newDesignVector)
    if diff<0:
        logging.debug('Accept: diff < 0')
        return newDesignVector
    
    uniRV = float(np.random.rand(1))
    p = np.exp(-diff/(Boltzmann_Constant*temperature))
    logging.debug('uniform RV: {:.4f}'.format(uniRV))
    logging.debug('the prob.: {:.4f}'.format(p))
    
    if uniRV<p:
        logging.debug('Accept: uniform RV < the prob.')
        return newDesignVector
    
    else:
        logging.debug('Reject')
        return designVector
    
    
def computeEnergyDiff(designVector, newDesignVector):
    f1, f2 = utils.evalTravDist(designVector), utils.evalTravDist(newDesignVector) 
    diff = f2-f1
    logging.debug('f1: {:.4f}'.format(f1))
    logging.debug('f2: {:.4f}'.format(f2))
    logging.debug('diff: {:.4f}'.format(diff))
    return diff

# %% [markdown]
# ### Step 5 & Main

# %%
def reduceTemperature(temperature):
    temperature = temperature*Temperature_Reduction_Factor
    return temperature


def main():
    # step 0 & 1
    iterationNumber = 1
    cycleNumber = 1
    temperature = initTemperature()
    Temperature_Threshold = temperature*Temperature_Threshold_Factor 
    designVector = initConfig()
    logging.debug('\n=== Step 0 & 1 ===')
    logging.debug('temperature: {}'.format(temperature))
    logging.debug('Temperature_Threshold: {}'.format(Temperature_Threshold))
    logging.debug('design vector: {}'.format(designVector))
    
    while temperature>=Temperature_Threshold: 
        
        logging.debug('\n=== Step 2 ===')
        newDesignVector = perturbConfig(designVector)
        logging.debug('new design vector: {}'.format(newDesignVector))
        
        logging.debug('\n=== Step 3 ===')
        designVector = metropolisCriterion(newDesignVector, 
                                           designVector,
                                           temperature)
        logging.debug('design vector: {}'.format(designVector))
        
        logging.debug('\n=== Step 4 ===')
        iterationNumber += 1
        logging.debug('iterationNumber {}'.format(iterationNumber))
        if iterationNumber<=Iteration:
            continue
        
        logging.debug('\n=== Step 5 ===') 
        cycleNumber +=1
        iterationNumber = 1
        temperature = reduceTemperature(temperature)
        logging.debug('temperature: {:.4f}'.format(temperature))
    
    logging.debug('\n=== Final ===')
    logging.debug('cycleNumber {}'.format(cycleNumber))
    logging.debug('design vector {}'.format(designVector))
    logging.debug('its energy {}'.format(utils.evalTravDist(designVector)))
    
    return list(designVector)
    


# %%
if __name__ == "__main__":
    designVector = main()
    logging.info('=== Parameters ===\n')
    logging.info(' Iteration: {}'.format(Iteration))
    logging.info(' Temperature_Threshold_Factor: {}'.format(Temperature_Threshold_Factor))
    logging.info(' Temperature_Reduction_Factor: {}'.format(Temperature_Reduction_Factor))
    logging.info(' Boltzmann_Constant: {}'.format(Boltzmann_Constant))
    logging.info('\n')
    logging.info('=== Results ===\n')
    logging.info(' bestValue: {}'.format(utils.evalTravDist(designVector)))

    logging.info(' bestPath:\n   {}'.format(designVector))
    logging.info('\n')
    logging.info('{}'.format(showStoreName(designVector)))