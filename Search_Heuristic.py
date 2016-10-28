__author__ = 'Ibis'

# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

from operator import itemgetter

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]
heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost,heuristic):

    # Creates blank number of steps matrix
    w, h = len(grid), len(grid[0])
    numberStepsMatrix = [[-1 for x in range(h)] for y in range(w)]
    step = 0

    # Creates blank directions matrix
    directonsMatrix = [[' ' for x in range(h)] for y in range(w)]
    action = [[0 for x in range(h)] for y in range(w)]

    list = [[sum(init), heuristic[init[0]][init[1]], init[0], init[1]]]
    tracked = []

    while list:
        # Sort list (smaller F up)
        list = sorted(list, key=itemgetter(1))

        # Get item with smaller F
        item = list.pop(0)
        tracked.append(item)
        g = item[0]
        f = item[1]

        # Populate number of steps matrix with step
        numberStepsMatrix[item[2]][item[3]] = step
        step += 1

        # Check if the goal is achieved
        if [item[2],item[3]] == goal:
            break

        # Places already tracked and not in places to track
        blacklist = [[x[2], x[3]] for x in list + tracked]

        # Create new items
        for i in range(0,len(delta)):
            newItem = map(sum, zip([item[2],item[3]],delta[i]))
            if (0 <= newItem[0] < len(grid)) and (0 <= newItem[1] < len(grid[0]))\
                and (grid[newItem[0]][newItem[1]] != 1)\
                and (newItem not in blacklist):
                    newG = g+cost
                    list.append([newG, newG+heuristic[newItem[0]][newItem[1]], newItem[0], newItem[1]])
                    action[newItem[0]][newItem[1]] = i

    # Populate directions matrix
    if goal == [item[2],item[3]]:
        x = goal[0]
        y = goal[1]
        directonsMatrix[x][y] = '*'
        while x != init[0] or y != init[1]:
            x2 = x - delta[action[x][y]][0]
            y2 = y - delta[action[x][y]][1]
            directonsMatrix[x2][y2] = delta_name[action[x][y]]
            x = x2
            y = y2
    else:
        return 'fail'

    # Exercise 1 - Return goal position with cost
    # if goal != [item[1],item[2]]:
    #     return 'fail'
    # else:
    #     return [item]
    # Exercise 2 - Return matrix with number of steps
    return numberStepsMatrix
    # Exercise 3 - Return matrix with directions
    # return directonsMatrix

answer = search(grid, init, goal, cost, heuristic)
if isinstance(answer, list):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
          for row in answer]))
else:
    print answer