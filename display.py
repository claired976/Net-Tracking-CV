# import matplotlib and animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# new 3D figure
fig = plt.figure()
ax1 = plt.axes(projection='3d')

j = 0

def animate(i):
    data = open('ballLocation.txt','r').read() # read in locations
    lines = data.split('\n') # split by newlines

    # if this is before the last line, split the next line by commas
    if (i < (len(lines))): 
        x, y, z = lines[i].split(',')
    
    # if this is the last line or later, continue to use the last line.
    else:
        x, y, z = lines[(len(lines) - 1)].split(',')
        print(i)

    # clear plot and label axes
    ax1.clear()
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # scale for graph
    ax1.set_xlim(-15,15)
    ax1.set_ylim(-30,30)
    ax1.set_zlim(-10,10)

    # plot object point, and its projection on three planes
    ax1.plot([float(x)], [float(y)], [float(z)], 'ro', markersize = 10)
    ax1.plot([-15], [float(y)], [float(z)], 'go')
    ax1.plot([float(x)], [30], [float(z)], 'bo')
    ax1.plot([float(x)], [float(y)], [-10], 'yo')
    
    # plot lines from main object to projections
    ax1.plot([float(x), -15], [float(y), float(y)], [float(z), float(z)], 'g', linewidth=1)
    ax1.plot([float(x), float(x)], [float(y), 30], [float(z), float(z)], 'b', linewidth=1)
    ax1.plot([float(x), float(x)], [float(y), float(y)], [float(z), -10], 'y', linewidth=1)

# animate with a new frame each 20 ms
ani = animation.FuncAnimation(fig, animate, interval=20) 
plt.show()