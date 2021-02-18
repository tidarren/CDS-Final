import pickle
from os.path import dirname, join


def loadDistanceMatrix():
    currentDir = dirname(__file__)
    dataPath = join(currentDir,'./distance_matrix.pickle')

    with open(dataPath, 'rb') as f:
        distanceMatrix = pickle.load(f)
    
    return distanceMatrix


def evalTravDist(path):
    """
    Evaluate traveling distances.
    
    Parameters:
    -----------
        :path: (list of int): traveling path without the start city at the end of path
        
    Return:
    -------
        :fitnessValue: (int): traveling distances
    """
    distanceMatrix = loadDistanceMatrix()
    fitnessValue = 0
    for i,source in enumerate(path):
        if i==len(path)-1:
            target = path[0]
        else:
            target = path[i+1]

        fitnessValue += distanceMatrix[source][target]

    return fitnessValue



def redundantResolution(start_node):
    """
    Pure implementation of generating the first solution for the Tabu search to start, with the redundant resolution
    strategy. That means that we start from the starting node (e.g. node 'a'), then we go to the city nearest (lowest
    distance) to this node (let's assume is node 'c'), then we go to the nearest city of the node 'c', etc
    till we have visited all cities and return to the starting node.

    :param path: The path to the .txt file that includes the graph (e.g.tabudata2.txt)

    :return first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
    in a list.
    :return distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
    in first_solution.

    """
    dict_of_neighbours = loadDictDistanceMatrix()
    end_node = start_node

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0

    while visiting not in first_solution:
        minim = 10000
        for k in dict_of_neighbours[visiting]:
            if int(k[1]) < int(minim) and k[0] not in first_solution:
                minim = k[1]
                best_node = k[0]

        first_solution.append(visiting)
        distance_of_first_solution += int(minim)
        visiting = best_node

    first_solution.append(end_node)

    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = distance_of_first_solution + int(
        dict_of_neighbours[first_solution[-2]][position][1]) - 10000
    
    return first_solution, distance_of_first_solution


def loadDictDistanceMatrix():
    """
    Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    """
    distanceMatrix = loadDistanceMatrix()
    dict_Distance_Matrix = {}
    for i, targets in enumerate(distanceMatrix):
        dict_Distance_Matrix[str(i)] = []
        for j, target in enumerate(targets):
            if j==i:
                continue
            dict_Distance_Matrix[str(i)].append([str(j), int(target)])
    return dict_Distance_Matrix