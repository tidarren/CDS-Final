'''
Reference:
https://hackmd.io/@Ndq-1n37SsOOaoWO_pGkRQ/rJo0NHELL#4-Particle-Swarm-Optimization-in-Discrete-Domain
'''

import numpy as np
import logging
import utils
import math
import argparse
from number_to_store_name import showStoreName

def move(pos, vel):
    """
    Add velocity to position.

    Parameters:
    -----------
        :pos: (list of int): traveling path without the start city at the end of path
            e.g. [0,1,2,....,33]
        :vel: (list of tuple): each tuple indicate swap two elements e.g. [(1,2)]
    
    Return:
    -------
        :pos: (list of int): traveling path without the start city at the end of path
    """
    for city1, city2 in vel:
        idx1 = pos.index(city1)
        idx2 = pos.index(city2)
        #swap
        pos[idx1], pos[idx2] = pos[idx2], pos[idx1]

    return pos 


def posSub(pos2,pos1):
    """
    Position substraction for deriving velocity

    Parameters:
    -----------
        :pos2: (list of int): e.g. [2,1,3]
        :pos1: (list of int): e.g. [1,2,3]
    
    Return:
    -------
        :vel: (list of tuples): each tuple indicate swap two elements e.g. [(1,2)]
    """
    vel = []
    while pos1!=pos2:
        for idx1, p1 in enumerate(pos1):
            idx2 = pos2.index(p1)
            if idx2==idx1:
                continue
            logging.debug('pos1: {}'.format(pos1))
            pos1[idx1], pos1[idx2] = pos1[idx2], pos1[idx1]
            vel.append((pos1[idx1], pos1[idx2]))
            break

    return vel


def velMult(weight, vel):
    """
    Velocity multiplication

    Parameters:
    -----------
        :weight: (float): scale velocity
        :vel: (list of tuples): each tuple indicate swap two elements e.g. [(1,2)]
    
    Return:
    -------
        :vel: (list of tuples): each tuple indicate swap two elements e.g. [(1,2)]
    """
    if weight==0 or vel==[]:
        return []
    logging.debug('vel: {}'.format(vel))
    velLen = len(vel)
    if weight>0 and weight<=1:
        leftLen = int(math.floor(weight*velLen))
        return vel[:leftLen]
    if weight>1:
        _int = math.floor(weight)
        _float = weight-_int
        return vel*_int+velMult(_float, vel)


class ParticleSwarmOptimization:
    def __init__(self, args):
        self.numOfSwarm = args.swarm
        self.numOfCities = args.cities
        self.positions = self.initPos(args)
        self.localBestPos = self.positions.copy()
        self.globalBestPos = min(self.localBestPos, 
                                 key=lambda x:self.evalObjFunc(x))
        self.c1 = 1; self.c2 = 1; self.w = 1
        self.velocitys = [ [] for _ in range(self.numOfSwarm)]
        self.values = [self.evalObjFunc(position) 
                       for position in self.positions]
        self.iteration = 1
        
        
    def initPos(self, args):
        if args.RandomInit:
            return [list(np.random.permutation(self.numOfCities)) 
                    for _ in range(self.numOfSwarm)]
        

        redundantResolution, distRedSol = utils.redundantResolution(args.BeginPoint)
        logging.debug('\nredundantResolution: {}'.format(redundantResolution))
        logging.debug('distRedSol: {}\n'.format(distRedSol))
        redundantResolution = list(map(lambda x:int(x), redundantResolution[:-1]))
        selfNum = int(self.numOfSwarm*args.InitPercent)
        sel = [redundantResolution for _ in range(selfNum)]
        randomHalf = [list(np.random.permutation(self.numOfCities)) for _ in range(self.numOfSwarm-selfNum)]
        return sel+randomHalf

        
    def evalObjFunc(self, x):
        return utils.evalTravDist(x)


    def updateVelocity(self):
        r1, r2 = np.random.rand(), np.random.rand()
        for idx, individual in enumerate(zip(self.positions,
                                             self.velocitys,
                                             self.localBestPos)):
            position, velocity, localBest = individual
            self.velocitys[idx] = velMult(self.w, velocity) \
                        + velMult(r1*self.c1, posSub(localBest,position)) \
                        + velMult(r2*self.c2, posSub(self.globalBestPos,position))
    
    
    def updatePosition(self):
        for idx, (position, velocity) in enumerate(zip(self.positions, 
                                                       self.velocitys)):
            self.positions[idx] = move(position, velocity)
    
    
    def isBetterThanLocal(self, position, localBest):
        if self.evalObjFunc(position)<self.evalObjFunc(localBest):
            return True
        return False
    
    
    def main(self,args):
        # while np.std(self.values)>=args.threshold \
        #       and self.iteration<args.iterations:
        while self.iteration<args.iterations:
            if self.iteration%5==0:
                logging.debug('iteration: {}'.format(self.iteration))
            
            # Find local best position
            for idx,(position, localBest) in enumerate(zip(self.positions,
                                                           self.localBestPos)):
                if self.isBetterThanLocal(position, localBest):
                    self.localBestPos[idx] = position
            
            # Find global best position
            self.globalBestPos = min(self.localBestPos, 
                                     key=lambda x:self.evalObjFunc(x))

            self.updateVelocity()
            
            self.updatePosition()
            
            # update values
            self.values = [self.evalObjFunc(position) 
                           for position in self.positions]
            
            self.iteration +=1
        
        logging.info('=== Parameters ===')
        logging.info(' Swarm Size: {}'.format(args.swarm))
        logging.info(' Iteration: {}'.format(args.iterations))
        logging.info(' RandomInit: {}'.format(args.RandomInit==1))
        logging.info(' ')
        logging.info('=== Results ===')
        logging.info(' bestValue: {}'.format(self.evalObjFunc(self.globalBestPos)))
        logging.info(' bestPath:\n   {}'.format(self.globalBestPos))
        logging.info(' ')
        logging.info('{}'.format(showStoreName(self.globalBestPos)))
  

if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="PSO")
    parser.add_argument("-s", "--swarm", type=int, 
                        help="Choose the number of swarm.", default=300)
    parser.add_argument("-c", "--cities", type=int, 
                        help="Choose the number of cities.", default=34)
    parser.add_argument("-i", "--iterations", type=int, 
                        help="How many iterations the algorithm should perform", default=300)
    parser.add_argument("-t", "--threshold", type=int, 
                        help="Converge Threshold of std of values", default=0.01)
    parser.add_argument("-r", "--RandomInit", type=int, 
                        help="Random Initialization", default=0)
    parser.add_argument("-b", "--BeginPoint", type=str, 
                        help="Choose a beginning point.", default='0')
    parser.add_argument("-p", "--InitPercent", type=float, 
                        help="Specify percent if not random init.", default=0.5)
    pos = ParticleSwarmOptimization(parser.parse_args())
    pos.main(parser.parse_args())