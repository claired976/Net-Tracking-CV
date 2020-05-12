# Adapted from https://math.stackexchange.com/questions/1993953/closest-points-between-two-lines
from numpy import array, cross
from numpy.linalg import solve, norm
import time

# write to this text file
file3 = open("ballLocation.txt", "w")

# camera positions
A0 = array([0, 175, 0])
B0 = array([145, 0, 0])

firstLoop = True

# continuously read in points from the .txt files
while(True):
    # read in data and split by lines
    feed1_data = open('feed1.txt','r').read()
    feed2_data = open('feed2.txt','r').read()
    lines1 = feed1_data.split('\n')
    lines2 = feed2_data.split('\n')
        
    # read in x, y, z values
    cx1, cy1, cz1 = lines1[len(lines1)-1].split(',')
    cx2, cy2, cz2 = lines2[len(lines2)-1].split(',')

    # convert values from pixels to cm
    x1 = float(int(cx1) - 300)*7.62/45
    y1 = float(cy1)
    z1 = float(-int(cz1) + 168)*7.62/45

    x2 = float(cx1)
    y2 = float(int(cy2) - 300)*7.62/52
    z2 = float(-int(cz2) + 168)*7.62/52

    # define the two lines
    A1 = array([x1, y1, z1])
    B1 = array([x2, y2, z2])

    # compute unit vectors
    UA = (A1 - A0) / norm(A1 - A0)
    UB = (B1 - B0) / norm(B1 - B0)

    # unit vector for C, perpendicular to both
    UC = cross(UB, UA); UC /= norm(UC)

    # solve equations
    RHS = B0 - A0
    LHS = array([UA, -UB, UC]).T
    solution = solve(LHS, RHS)

    # find points of intersection on two lines
    q1 = A0 + solution[0]*UA
    q2 = B0 + solution[1]*UB

    # find closest point, in middle of intersection points
    x = (q1[0] + q2[0])/2
    y = (q1[1] + q2[1])/2
    z = (q1[2] + q2[2])/2

    # no newline if this is the first line
    if (firstLoop):
        pt = str(x) + ',' + str(y) + ',' + str(z)
        firstLoop = False
    else:
        pt = '\n' + str(x) + ',' + str(y) + ',' + str(z)

    # write data to text file
    file3.write(pt)
    file3.flush()

    # sleep 0.033 seconds; waiting for new data point if running in real time
    time.sleep(0.033)
