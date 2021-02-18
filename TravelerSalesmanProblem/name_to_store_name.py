import ast
import sys
import pickle
import logging
import argparse
from os.path import dirname, join


BEST_PATH = [25, 5, 7, 27, 17, 1, 2, 30, 33, 29, 10, 16, 32, 20, 3, 0, 4, 13, 24, 9, 8, 12, 31, 28, 23, 11, 15, 14, 21, 22, 6, 18, 26, 19]
    
def loadStoreName():
    currentDir = dirname(__file__)
    dataPath = join(currentDir,'./distance_matrix_name.pickle')

    with open(dataPath, 'rb') as f:
        storeNames = pickle.load(f)
    
    # leave only store name
    # 7-ELEVEN 林坊門市 > 林坊
    storeNames = list(map(lambda x:x.split()[1].replace('門市',''), storeNames))

    return storeNames


def number2Stores(bestPath, storeNames):
    # pathList = ast.literal_eval(args.path)
    pathList = list(map(lambda x:int(x), bestPath))
    return [storeNames[num] for num in pathList]


def showPath(bestPath):
    bestPath = list(bestPath)
    start = bestPath[0]
    bestPath = ' -> '.join(bestPath)
    bestPath += ' -> {}'.format(start)
    return bestPath


def showStoreName(bestPath):
    storeNames = loadStoreName()

    bestPath = number2Stores(bestPath, storeNames)
    print('{}'.format(showPath(bestPath)))
    

# if __name__ == "__main__":
#     logging.basicConfig(format='%(message)s', level=logging.INFO)
#     # parser = argparse.ArgumentParser(description="Tabu Search")
#     # parser.add_argument(
#     #     "-p", "--BestPath", type=str, help="Input bestpath to derive the corresponding store names.")
    
#     sys.exit(showStoreName(bestPath=[]))