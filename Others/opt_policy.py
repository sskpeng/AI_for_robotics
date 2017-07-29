# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[ 0, -1], # go left
         [ 0, 1 ], # go right
         [-1, 0 ], # go up
         [ 1, 0 ]] # go down

delta_name = ['<', '>', '^', 'v']

def optimum_policy(grid,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2

    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    policy[goal[0]][goal[1]] = '*'
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if value[x][y] > 0 and value[x][y] < 99:
                for a in range(len(delta)):
                    x3 = x + delta[a][0]
                    y3 = y + delta[a][1]
                    
                    if x3 >= 0 and x3 < len(grid) and y3 >= 0 and y3 < len(grid[0]) and grid[x3][y3] == 0:
                        v3 = value[x3][y3]

                        if v3 < value[x][y]:
                            change = True
                            policy[x][y] = delta_name[a]

    return policy
policy = (optimum_policy(grid,goal,cost))
for i in range(len(policy)):
    print (policy[i])