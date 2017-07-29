# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn
#---------------------------------
grid = [[0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [4, 5, 0]
goal = [4, 3]
cost = [1, 1, 1]
#---------------------------------
# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid,init,goal,cost):
    val = [[99 for col in range(len(grid[row]))] for row in range(len(grid))]
    ori = [[-1 for col in range(len(grid[row]))] for row in range(len(grid))]
    res = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    res[goal[0]][goal[1]] = '*'

    y = init[0]
    x = init[1]
    o = init[2]
    g = 0
    val[y][x] = g
    ori[y][x] = o
    front_end = []
    front_end.append([g, y, x, o])
    finished = False
    found = False

    while finished == False and found == False:
        print 'front_end =', front_end
        for i in range(len(val)):
            print val[i]
        for i in range(len(val)):
            print ori[i]
        front_end.sort()
        front_end.reverse()
        next = front_end.pop()
        g = next[0]
        y = next[1]
        x = next[2]
        o = next[3]
        print 'this=', x, y
        if g == 0:
            res[y][x] = '#'
        else:
            x3 = x - forward[o][1]
            y3 = y - forward[o][0]
            o3 = ori[y3][x3]
            for i in range(len(action)):
                if o == (o3+action[i]) % 4:
                    res[y3][x3] = action_name[i]
            #act3 = (o3-o) % 4
            #res[y3][x3] = action_name[action.index(-act3)]

        for i in range(len(action)):
            o2 = (o + action[i]) % 4
            x2 = x + forward[o2][1]
            y2 = y + forward[o2][0]
            g2 = g + cost[i]

            if x2 < len(grid[0]) and x2 > -1 and y2 < len(grid) and y2 > -1:
                
                #if grid[y2][x2] <> 1:
                if ori[y2][x2] <> o2 and grid[y2][x2] == 0:
                #if grid[y2][x2] <> 1:
                    #g2 = g + 1
                    val[y2][x2] = g2
                    ori[y2][x2] = o2
                    front_end.append([g2, y2, x2, o2])
                    if x2 == goal[1] and y2 == goal[0]:
                        res[y][x] = action_name[i]
                        found = True
        if len(front_end) == 0 and g >= 99:
            finished = True
    
   
    
    policy2D = res

    return policy2D
res = optimum_policy2D(grid,init,goal,cost)
for i in range(len(res)):
    print res[i]