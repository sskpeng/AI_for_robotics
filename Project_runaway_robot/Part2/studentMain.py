# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    ####----------------------
    if not OTHER:
        OTHER = []
    OTHER.append([measurement[0], measurement[1]])
    (pos_x, pos_y) = measurement
    
    if len(OTHER) == 1:
        est_h = 0
        est_d = 0
        est_t = 0
    else:
        moves = []
        for i in range(1, len(OTHER)):
            checked = False
            p1_x = OTHER[i][0]
            p1_y = OTHER[i][1]
            p2_x = OTHER[i - 1][0]
            p2_y = OTHER[i - 1][1]
            dist = distance_between((p1_x, p1_y), (p2_x, p2_y))
            heading = atan2((p1_y - p2_y), (p1_x - p2_x))
            if len(moves) > 2 and not checked:
                pre_heading = moves[-1][0][0]
                for d in [-1, 0, 1]:
                    diff = (int(pre_heading / (2 * pi)) + d) * (2 * pi)
                    if abs(heading + diff - pre_heading) < pi:
                        heading += diff
                        checked = True
            move = [[heading], [dist]]
            moves.append(move)
        
        (x, P) = kalman_filter(moves)
        est_h = x.value[0][0]
        est_t = x.value[1][0]
        est_d = x.value[2][0]
    est_x = pos_x + est_d * cos(est_h)
    est_y = pos_y + est_d * sin(est_h)

    xy_estimate = (est_x, est_y)

   
    ####----------------------
    #xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER

def kalman_filter2(measurements, P):

    # initial state (pos_x, pos_y, heading, turning, dist)
    x = matrix([[0],
                [0],
                [0.],
                [0.],
                [0.]])
    # external motion
    #u = matrix([[0.], [0.], [0.], [0.], [0.]]) 

    # P =  # initial uncertainty: 0 for positions x and y, 1000 for the two velocities
    P = matrix([[1000., 0, 0., 0., 0.],
                [0., 1000, 0., 0., 0.],
                [0., 0, 1000., 0., 0.],
                [0., 0, 0., 1000., 0.],
                [0., 0, 0., 0., 1000.]])
    # F =  # next state function: generalize the 2d version to 4d
    
    #F = matrix([[1., 0., 0.1, 0., 0.],
    #            [0., 1., 0., 0.1, 0.],
    #            [0., 0., 1., 0., 0.],
    #            [0., 0., 1., 0., 0.],
    #            [0., 0., 0., 1., 0.]])
    # H =  # measurement function: reflect the fact that we observe x and y but not the two velocities
    H = matrix([[1., 0., 0., 0., 0.],
                [0., 1., 0., 0., 0.]])
    # R =  # measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
    R = matrix([[0.1, 0.],
                [0., 0.1]])
    # I =  # 5d identity matrix
    I = matrix([[1., 0., 0., 0., 0.],
                [0., 1., 0., 0., 0.],
                [0., 0., 1., 0., 0.],
                [0., 0., 0., 1., 0.],
                [0., 0., 0., 0., 1.]])


    for n in range(len(measurements)):
        
        # measurement update
        temp = H * x
        Z = matrix([measurements[n]])
        y = Z.transpose() - (H * x)
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + K * y
        P = (I - K * H) * P

        # prediction
        if len(measurements) == 1:
            d = x.value[4][0]
            t = x.value[3][0]
            h = x.value[2][0]
        elif len(measurements) == 2:
            d = distance_between(measurements[1], measurements[0])
            x1 = measurements[1][0]
            y1 = measurements[1][1]
            x0 = measurements[1 - 1][0]
            y0 = measurements[1 - 1][1]
            h = atan2((y1 - y0), (x1 - x0))
            t = 0.             
        else:
            dists = []
            headings = []
            turnings = []
            for i in range(1, len(measurements)):
                dist = distance_between(measurements[i-1], measurements[i])
                x1 = measurements[i][0]
                y1 = measurements[i][1]
                x0 = measurements[i - 1][0]
                y0 = measurements[i - 1][1]
                heading = atan2((y1 - y0), (x1 - x0))
                dists.append(dist)
                headings.append(heading)
            for j in range(1, len(headings)):
                turning = headings[j] - headings[j - 1]
                turnings.append(turning)
            d = sum(dists) / len(dists)        
            h = x.value[2][0]
            #t = x.value[3][0]
            t = sum(turnings) / len(turnings)

        F = matrix([[1., 0., 0., 0., 0.],
                    [0., 1., 0., 0., 0.],
                    [0., 0., 1., 1., 0.],
                    [0., 0., 0., 1., 0.],
                    [0., 0., 0., 0., 1.]])
        
        u = matrix([[d * cos(h + t)], [d * sin(h + t)], [0.], [0.], [0.]]) 

        x = F * x + u
        P = F * P * F.transpose()
        
    return x,P


def kalman_filter(moves):
    sigma = 10
    u = matrix([[0.], [0.], [0.]])  # external motion
    x = matrix([[0.],
                [0.],
                [0.]]) # [heading, turning, dist]
    P = matrix([[1000., 0., 0.],
                [0., 1000., 0.],
                [0., 0., 1000.]])
        # measurement uncertainty
    R = matrix([[sigma, 0.],
                [0., sigma]])
        # next state function
    F = matrix([[1., 1., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])
        # measurement function
    H = matrix([[1., 0., 0.],
                [0., 0., 1.]])
        # identity matrix
    I = matrix([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])

    for n in range(len(moves)):
        
        # measurement update
        y = matrix(moves[n]) - (H * x)
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + K * y
        P = (I - K * H) * P

        # prediction
        x = F * x + u
        P = F * P * F.transpose()
        
    return x,P
# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading2(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 100:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 1000:
            print ("Sorry, it took you too many steps to localize the target.")
        print(ctr, error, position_guess, true_position)
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.

def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.1, 0.1, 0.1)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.1, 0.1, 0.1)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.1, 0.1, 0.1)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 50:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 10:
            print ("Sorry, it took you too many steps to localize the target.")
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    return localized

def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)
#test_target.set_noise(0.0, 0.0, 0.0)

#demo_grading(naive_next_pos, test_target)
demo_grading(estimate_next_pos, test_target)



