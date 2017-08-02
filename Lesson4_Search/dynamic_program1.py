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

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def compute_value(grid,goal,cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    res = [[99 for col in range(len(grid[row]))] for row in range(len(grid))]
    
    x = goal[1]
    y = goal[0]
    res[y][x] = 0
    # print 'res=',res
    g = 0
    finished = False
    front_end = []
    front_end.append([g, y, x])

    while len(front_end) <> 0:
        print 'front_end =', front_end
        for i in range(len(res)):
            print res[i]
        front_end.sort()
        front_end.reverse()
        next = front_end.pop()
        g = next[0]
        y = next[1]
        x = next[2]
        print 'this=', x, y

        for i in range(len(delta)):
            x2 = x + delta[i][1]
            y2 = y + delta[i][0]
            # print 'x2, y2=', x2, y2
            if x2 < len(grid[0]) and x2 > -1 and y2 < len(grid) and y2 > -1:
                if res[y2][x2] == 99 and grid[y2][x2] == 0:
                    g2 = g + 1
                    res[y2][x2] = g2
                    front_end.append([g2, y2, x2])

    value = res

    # make sure your function returns a grid of values as 
    # demonstrated in the previous video.
    return value 
res = compute_value(grid,goal,cost)
for i in range(len(res)):
    print res[i]