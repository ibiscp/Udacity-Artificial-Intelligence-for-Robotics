__author__ = 'Ibis'

# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

clear = "\n" * 100

delta_name = ['^', '<', 'v', '>']

# def compute_value(grid,goal,cost):
def optimum_policy(grid,goal,cost):

    # Creates blank number of steps matrix
    w, h = len(grid), len(grid[0])
    numberStepsMatrix = [[99 for x in range(h)] for y in range(w)]

    # Creates blank directions matrix
    directonsMatrix = [[' ' for x in range(h)] for y in range(w)]

    # Inicial position
    xGoal = goal[0]
    yGoal = goal[1]

    # Inicialize steps and directions matrix
    numberStepsMatrix[xGoal][yGoal] = 0
    directonsMatrix[xGoal][yGoal] = '*'

    # List with places already navigated
    blacklist = []

    # List of places to navigate
    list = [[xGoal,yGoal]]

    while list:

        # Get item from list
        item = list.pop(0)
        blacklist.append(item)

        # Create new items
        for i in range(0,len(delta)):
            next = map(sum, zip(item,delta[i]))
            if (0 <= next[0] < len(grid)) and (0 <= next[1] < len(grid[0]))\
                and (grid[next[0]][next[1]] != 1) and (next not in blacklist) and (next not in list):
                    numberStepsMatrix[next[0]][next[1]] = numberStepsMatrix[item[0]][item[1]] + cost
                    directonsMatrix[next[0]][next[1]] = delta_name[(i+2)%4]
                    list.append(next)
                    # print clear
                    # print('\n'.join([''.join(['{:4}'.format(value) for value in row])
                    #    for row in directonsMatrix]))


    # First exercise - Return all the numbers of steps to achieve goal
    #return numberStepsMatrix

    # Second exercise - Return all the directions matrix
    return directonsMatrix

# First exercise
# matrix = compute_value(grid,goal,cost)

# Second exercise
matrix = optimum_policy(grid,goal,cost)

# Print the result
print('\n'.join([''.join(['{:4}'.format(value) for value in row])
   for row in matrix]))