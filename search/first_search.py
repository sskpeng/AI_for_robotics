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

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------
    step = 0
    grid_size_x = len(grid[0])
    grid_size_y = len(grid)
    path = []
    closed_list = []
    open_list = []
    # path.append([step, init[0], init[1]])
    open_list.append([step, init[0], init[1]])

    while True:
        step = path[0][0]
        x = path[0][1]
        y = path[0][2]
        for i in range(len(delta):
            if x > 0: # <
                if (grid[x-1,y] ==0) and not [x - 1, y] in closed_list:
                    open_list.append([step+1, x - 1, y])

            if x < grid_size_x-1: # >
                if (grid[x-1,y] ==0) and not [x + 1, y] in closed_list:
                    open_list.append([step+1, x + 1, y])

            if y < grid_size_y-1: # v
                if (grid[x-1,y] ==0) and not [x, y+1] in closed_list:
                    open_list.append([step+1, x, y+1])

            if y > 0: # ^
                if (grid[x-1,y] ==0) and not [x, y-1] in closed_list:
                    open_list.append([step+1, x, y-1])

            closed_list.append([x,y)
            open_list.remove([step, x, y])

            if len(open_list) == 0:
                # fail
                finished = True
            elif expression:
                pass


        step += 1

    return path
