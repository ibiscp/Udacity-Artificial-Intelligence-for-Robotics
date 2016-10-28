import os

__author__ = 'Ibis'

from operator import itemgetter

# -------------------
# Background Information
#
# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
#
# For example:
#
# warehouse = [[ 1, 2, 3],
#              [ 0, 0, 0],
#              [ 0, 0, 0]]
# dropzone = [2,0]
# todo = [2, 1]
#
# The robot starts at the dropzone.
# The dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to the dropzone.
#
# Robot can move diagonally, but the cost of a diagonal move is 1.5.
# The cost of moving one step horizontally or vertically is 1.
# So if the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, the robot has to move into the same cell as the box.
# When the robot picks up a box, that cell becomes passable (marked 0)
# The robot can pick up only one box at a time and once picked up
# it has to return the box to the dropzone by moving onto the dropzone cell.
# Once the robot has stepped on the dropzone, the box is taken away,
# and it is free to continue with its todo list.
# Tasks must be executed in the order that they are given in the todo list.
# You may assume that in all warehouse maps, all boxes are
# reachable from beginning (the robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works!)
# in a function named plan() that takes as input three parameters:
# warehouse, dropzone, and todo. See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order, which should
# match with our answer. You may include print statements to show
# the optimum path, but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
#
# Add your code at line 76.
#
# --------------------
# Parameter Info
#
# warehouse - a grid of values, where 0 means that the cell is passable,
# and a number 1 <= n <= 99 means that box n is located at that cell.
# dropzone - determines the robot's start location and the place to return boxes
# todo - list of tasks, containing box numbers that have to be picked up
#
# --------------------
# Testing
#
# You may use our test function below, solution_check(),
# to test your code for a variety of input parameters.

warehouse = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone = [2,0]
todo = [2, 1]
delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1], # go right
         [ 1, 1], # go left up
         [ 1,-1], # go left down
         [-1, 1], # go right up
         [-1,-1]] # go right down

# ------------------------------------------
# plan - Returns cost to take all boxes in the todo list to dropzone
#
# ----------------------------------------
# modify code below
# ----------------------------------------
def plan(warehouse, dropzone, todo):
    cost = [0 for x in range(len(todo))]

    actualPosition = warehouse

    for k in range(len(todo)):

        track = "todo"

        while track != "completed":

            # Determine what is the next goal, it could be or the place of the next box or the dropzone
            if track == "todo":
                goal = [[index, row.index(todo[k])] for index, row in enumerate(warehouse) if todo[k] in row][0]
                init = dropzone
            else:
                init = goal
                goal = dropzone
                track = "dropzone"

            # Creates blank number of steps matrix
            w, h = len(warehouse), len(warehouse[0])
            numberStepsMatrix = [[0 for x in range(h)] for y in range(w)]

            heuristic = heuristicMatrix([len(warehouse), len(warehouse[0])], goal)

            item = [sum(init), heuristic[init[0]][init[1]], init[0], init[1], 0]
            list = [item]
            tracked = []

            while track not in ("track", "completed"):
                # Sort list (smaller F up)
                list = sorted(list, key=itemgetter(1))

                actualPosition[item[2]][item[3]] = 0

                # Get item with smaller F
                item = list.pop(0)
                tracked.append(item)
                g = item[0]
                f = item[1]

                # actualPosition[item[2]][item[3]] = 'x'
                # print(10*'\n')
                # print('\n'.join([''.join(['{:4}'.format(str(a)) for a in row])
                #     for row in actualPosition]))
                # print('\n')
                # print('\n'.join([''.join(['{:4}'.format(str(a)) for a in row])
                #     for row in numberStepsMatrix]))

                if ([item[2],item[3]] == goal):
                    if track == "todo":
                        track = "track"
                    else:
                        track = "completed"

                # Places already tracked and not in places to track
                blacklist = [[x[2], x[3]] for x in tracked]

                # Create new items
                for i in range(0,len(delta)):
                    newItem = map(sum, zip([item[2],item[3]],delta[i]))
                    if (0 <= newItem[0] < len(warehouse)) and (0 <= newItem[1] < len(warehouse[0]))\
                        and (warehouse[newItem[0]][newItem[1]] in (0, todo[k]))\
                        and (newItem not in blacklist):
                            if i > 3:
                                effort = 1.5
                            else:
                                effort = 1
                            if (numberStepsMatrix[newItem[0]][newItem[1]] > numberStepsMatrix[item[2]][item[3]] + effort) or \
                                    (numberStepsMatrix[newItem[0]][newItem[1]] == 0):
                                numberStepsMatrix[newItem[0]][newItem[1]] = numberStepsMatrix[item[2]][item[3]] + effort
                                newG = g+effort
                                list.append([newG, newG+heuristic[newItem[0]][newItem[1]], newItem[0], newItem[1], effort])

            cost[k] += numberStepsMatrix[goal[0]][goal[1]]

    return sum(cost)

def heuristicMatrix(size, dropzone):

    # Size of the warehouse
    row = size[0]
    column = size[1]

    # Creates the heuristic matrix
    matrix = [[0.0 for x in range(column)] for y in range(row)]

    # Populate the heuristic matrix
    for i in range(row):
        for j in range(column):
            rowDiff = abs(i - dropzone[0])
            columnDiff = abs(j - dropzone[1])
            matrix[i][j] = abs(rowDiff - columnDiff) + min(rowDiff, columnDiff) * 1.5

    # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
    #       for row in matrix]))

    return matrix

################# TESTING ##################

# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[]. Uncomment the call
# to solution_check to test your code.
#
def solution_check(test, epsilon = 0.00001):
    answer_list = []

    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i+1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            #print "#############################################"
        else:
            print "\nTest case ", i+1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost
            answer_list.append(0)
    runtime =  time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False
#Testing environment
# Test Case 1
warehouse1 = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone1 = [2,0]
todo1 = [2, 1]
true_cost1 = 9
# Test Case 2
warehouse2 = [[   1, 2, 3, 4],
              [   0, 0, 0, 0],
              [   5, 6, 7, 0],
              [ 'x', 0, 0, 8]]
dropzone2 = [3,0]
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [[   1, 2,  3,  4, 5, 6,  7],
              [   0, 0,  0,  0, 0, 0,  0],
              [   8, 9, 10, 11, 0, 0,  0],
              [ 'x', 0,  0,  0, 0, 0, 12]]
dropzone3 = [3,0]
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[ 1, 17, 5, 18,  9, 19,  13],
              [ 2,  0, 6,  0, 10,  0,  14],
              [ 3,  0, 7,  0, 11,  0,  15],
              [ 4,  0, 8,  0, 12,  0,  16],
              [ 0,  0, 0,  0,  0,  0, 'x']]
dropzone4 = [4,6]
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
                 [dropzone1, dropzone2, dropzone3, dropzone4],
                 [todo1, todo2, todo3, todo4],
                 [true_cost1, true_cost2, true_cost3, true_cost4]]


solution_check(testing_suite) #UNCOMMENT THIS LINE TO TEST YOUR CODE

# plan(warehouse3,dropzone3,todo3)