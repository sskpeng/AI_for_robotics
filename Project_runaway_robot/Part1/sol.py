def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    ####----------------------
    if not OTHER:
        OTHER = []
    OTHER.append(measurement)
    if len(OTHER) == 1:
        x = OTHER[0][0]
        y = OTHER[0][1]
        xy_estimate = (x, y)
    elif len(OTHER) == 2:
        x1 = OTHER[0][0]
        y1 = OTHER[0][1]
        x2 = OTHER[1][0]
        y2 = OTHER[1][1]
        dx = x2 - x1
        dy = y2 - y1
        xy_estimate = (x2 + dx, y2 + dy)
    else:
        headings = []
        dists = []
        for i in range(1, len(OTHER)):
            p1 = (OTHER[i][0], OTHER[i][1])
            p2 = (OTHER[i-1][0], OTHER[i-1][1])
            dist = distance_between(p1, p2)
            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]
            heading = atan2(dy, dx)
            dists.append(dist)
            headings.append(heading)
        turnings = []
        for i in range(1, len(headings)):
            turnings.append(headings[i] - headings[i-1])

        est_dist = sum(dists) / len(dists)
        est_turning = sum(turnings) / len(turnings)
        est_heading = angle_trunc(headings[-1] + est_turning)
        x = OTHER[-1][0]
        y = OTHER[-1][1]
        est_x = x + est_dist * cos(est_heading)
        est_y = y + est_dist * sin(est_heading)
        xy_estimate = (est_x, est_y)

        

    ####----------------------
    return xy_estimate, OTHER 