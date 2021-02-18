import copy
import argparse
import sys
import pickle
import logging
import utils
import numpy as np
from number_to_store_name import showStoreName
from os.path import dirname, join


def find_neighborhood(solution, dict_of_neighbours):
    """
    Pure implementation of generating the neighborhood (sorted by total distance of each solution from
    lowest to highest) of a solution with 1-1 exchange method, that means we exchange each node in a solution with each
    other node and generating a number of solution named neighborhood.

    :param solution: The solution in which we want to find the neighborhood.
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :return neighborhood_of_solution: A list that includes the solutions and the total distance of each solution
    (in form of list) that are produced with 1-1 exchange from the solution that the method took as an input


    Example:
    >>> find_neighborhood(['a','c','b','d','e','a']) (example c4取2=6, in our case: c33取2=528)
    [['a','e','b','d','c','a',90], [['a','c','d','b','e','a',90],['a','d','b','c','e','a',93],
    ['a','c','b','e','d','a',102], ['a','c','e','d','b','a',113], ['a','b','c','d','e','a',93]]

    """

    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                for i in dict_of_neighbours[k]:
                    if i[0] == next_node:
                        distance = distance + int(i[1])
            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)
    
    logging.debug(neighborhood_of_solution)
    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size):
    """
    Pure implementation of Tabu search algorithm for a Travelling Salesman Problem in Python.

    :param first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
    in a list.
    :param distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
    in first_solution.
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :param iters: The number of iterations that Tabu search will execute.
    :param size: The size of Tabu List.
    :return best_solution_ever: The solution with the lowest distance that occured during the execution of Tabu search.
    :return best_cost: The total distance that Travelling Salesman will travel, if he follows the path in best_solution
    ever.

    """
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while found is False:
            i = 0
            while i < len(best_solution):

                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list and [second_exchange_node,
                                                                                 first_exchange_node] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = neighborhood[index_of_best_solution]

        if len(tabu_list) >= size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_cost



def main(args=None):
    dict_of_neighbours = utils.loadDictDistanceMatrix()
    
    if args.RandomInit:
        first_solution = list(np.random.permutation(34))
        distance_of_first_solution = utils.evalTravDist(first_solution)
        first_solution.append(first_solution[0])
        first_solution = list(map(lambda x:str(x), first_solution))
    else:
        first_solution, distance_of_first_solution = utils.redundantResolution(args.BeginPoint)
    
    logging.debug('first_solution: {}'.format(first_solution))

    best_sol, best_cost = tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, args.Iterations,
                                      args.Size)
    
    logging.info('=== Parameters ===')
    logging.info(' Iteration: {}'.format(args.Iterations))
    logging.info(' Tabu List Size: {}'.format(args.Size))
    logging.info(' RandomInit: {}'.format(args.RandomInit==0))
    logging.info(' ')
    logging.info('=== Results ===')
    logging.info(' bestValue: {}'.format(best_cost))
    logging.info(' bestPath:\n   {}'.format(best_sol[:-1]))
    logging.info(' ')
    logging.info('{}'.format(showStoreName(best_sol[:-1])))


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Tabu Search")
    parser.add_argument(
        "-b", "--BeginPoint", type=str, help="Choose a beginning point.", default='0')
    parser.add_argument(
        "-i", "--Iterations", type=int, help="How many iterations the algorithm should perform", default=300)
    parser.add_argument(
        "-s", "--Size", type=int, help="Size of the tabu list", default=5)
    parser.add_argument(
        "-r", "--RandomInit", type=int, help="Random Initialization", default=0)
    # Pass the arguments to main method
    sys.exit(main(parser.parse_args()))