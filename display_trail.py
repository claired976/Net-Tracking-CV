# import matplotlib and animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

# new 3D figure
fig = plt.figure()
ax1 = plt.axes(projection='3d')

j = 0


def animate(i):
    data = open('ballLocation.txt','r').read() # read in locations
    lines = data.split('\n') # split by newlines

    # clear plot
    ax1.clear()

    # plot previous points with decreasing color saturation
    for j in range(i):
        x1, y1, z1 = lines[j].split(',')
        r = 1.0/(i+1)
        ax1.plot([float(x1)], [float(y1)], [float(z1)], 'o', color=mcolors.hsv_to_rgb([0,1 - r*(i - j),1]))

    # if this is before the last line, plot the current point
    if (i < (len(lines))):
        x, y, z = lines[i].split(',')
    
    # if this is the last line or afterwards, plot the last point
    else:
        x, y, z = lines[(len(lines) - 1)].split(',')
        print(i)

    # label and scale axes
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_xlim(-15,15)
    ax1.set_ylim(-30,30)
    ax1.set_zlim(-10,10)

    # plot current point
    ax1.plot([float(x)], [float(y)], [float(z)], 'o', color=mcolors.hsv_to_rgb([0,1,1]))

# animate with a new frame each 20 ms
ani = animation.FuncAnimation(fig, animate, interval=20) 
plt.show()