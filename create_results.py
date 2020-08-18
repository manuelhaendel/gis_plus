# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:23:25 2020

@author: Manuel
"""


import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from functions import (focal_statistics, get_values,
                       get_angle, get_newdata, rectangfun)
from classes import Rectangle, Circle, Wedge



def make_image(data, outputname, size=(4, 6), dpi=80, cmap = 'RdYlBu', add_values = True,
               show_window = False, window = "None", window_type = "circle",
               center = (7, 5), radius = 3, start = 0, end = 90, corner = (3,8,6,9)):
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    fig.add_axes(ax)
    
    ax.set_xticks(np.arange(-.5, 10, 1))
    ax.set_yticks(np.arange(-.5, 15, 1))
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    ax.tick_params(axis='both', which='both',length=0)

    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
    
    if show_window:
        ax.imshow(window, aspect='equal', cmap = cmap)
        if window_type == "circle":
            x, y = draw_circle(center, radius)
        elif window_type == "wedge":
            x, y = draw_wedge(center, radius, start, end)
        elif window_type == "rectangle":
            x = [corner[0]-.5, corner[1]+.5, corner[1]+.5,
                 corner[0]-.5, corner[0]-.5]
            y = [corner[2]-.5, corner[2]-.5, corner[3]+.5,
                 corner[3]+.5, corner[2]-.5]
            
        ax.plot(x, y, '-', linewidth=2.5, color='k')
    else:
        ax.imshow(data, aspect='equal', cmap = cmap)
    
    if add_values:
        # add cell values as text in each cell
        for col in range(np.size(data, 1)):
            for row in range(np.size(data, 0)):
                str = int(data[row, col])
                ax.text(col-0.25, row+0.2, str)
    
    
    
    ax.grid(which = "major", color = "k", linestyle='-', linewidth=2)
    
    #plt.show()
    plt.savefig(outputname, dpi=dpi)


def draw_circle(center, radius):

    x = np.linspace(-radius, radius, 100)
    y = np.sqrt(radius**2 - x**2)
    x = center[1] + x
    x = np.concatenate((x, x[::-1]), 0)
    y_up = center[0] + y
    y_lo = center[0] - y
    y = np.concatenate((y_up, y_lo), 0)
    return(x, y)

center = (7,5)
radius = 3


def draw_wedge(center, radius, start, end):

    x, y = draw_circle(center, radius)
    angle = np.zeros(x.shape)
    for i in range(x.size):
        angle[i] = get_angle(center[0], center[1], y[i], x[i])
    
    angle = np.round(angle, 2)
    
    # When the positive x-axis is included in the wedge, the end
    # angle is smaller than the start angle. In this case all the
    # angles between 0° and the end angle must be increased by 360°
    # so the condition for selecting the window works as intended.
    if start > end:
                    
        condition = (angle >= 0) & (angle <= end)
        angle = np.where(condition, angle + 360, angle)
        end = end + 360
        
    # The positive x-axis has an angle of 0°. It must be set
    # to 360°, when the end angle is exactly 360°, so the condition
    # for selecting the window works as intended.
    if end == 360:
        angle = np.where(angle == 0, 360, angle)
        
    # selecting cells that fall into the window.
    window = np.where((angle >= start) & (angle <= end))
    
    x = x[window]
    x = np.append(center[1], x)
    x = np.append(x, center[1])
    y = y[window]
    y = np.append(center[0], y)
    y = np.append(y, center[0])
    
    return(x, y)

np.random.seed(100)
file = np.random.randint(0,99, 150).reshape(15, 10)

# save plot of input array
make_image(file, 'figures/focal_stat_in.png')

# colormap for figures that show window
cmap = mcolors.LinearSegmentedColormap.from_list("", [(1,1,1), (0,0.5,0)])


# save outputs for circle neighborhood
out = focal_statistics(file, Circle(3), "max")
make_image(out, 'figures/circle_3_out_max.png')

out = focal_statistics(file, Circle(3), "mean")
make_image(out, 'figures/circle_3_out_mean.png')

out = focal_statistics(file, Circle(3), "std")
make_image(out, 'figures/circle_3_out_std.png')


window = get_values(file, Circle(3), 7, 5, show_window = 1)
make_image(file, 'figures/circle_3_out_window.png', show_window = True,
           window_type = "circle", window = window, cmap = cmap)
make_image(file, 'figures/circle_3_out_window_no_values.png', add_values = False,
           show_window = True, window_type = "circle", window = window, cmap = cmap)



# save outputs for wedge neighborhood
out = focal_statistics(file, Wedge(3, 0, 135), "max")
make_image(out, "figures/wedge_3_0_135_out_max.png")

out = focal_statistics(file, Wedge(3, 0, 135), "mean")
make_image(out, "figures/wedge_3_0_135_out_mean.png")

out = focal_statistics(file, Wedge(3, 0, 135), "std")
make_image(out, "figures/wedge_3_0_135_out_std.png")


window = get_values(file, Wedge(3, 0, 135), 7, 5, show_window = 1)[0]
make_image(file, 'figures/wedge_3_0_135_out_window.png', show_window = True,
           window_type = "wedge", window = window, cmap = cmap, start = 0, end = 135)
make_image(file, 'figures/wedge_3_0_135_out_window.png', show_window = True, add_values = False,
           window_type = "wedge", window = window, cmap = cmap, start = 0, end = 135)




# save outputs for rectangle neighborhood
out = focal_statistics(file, Rectangle(6, 4), "max")
make_image(out, "figures/rectangle_5_3_out_max.png")

out = focal_statistics(file, Rectangle(6, 4), "mean")
make_image(out, "figures/rectangle_5_3_out_mean.png")

out = focal_statistics(file, Rectangle(6, 4), "std")
make_image(out, "figures/rectangle_5_3_out_std.png")
    

window = np.zeros(file.shape)
window[6:10, 3:9] = 0.5
window[7, 5] = 1
make_image(file, 'figures/rectangle_5_3_out_window.png', show_window = True,
           window_type = "rectangle", window = window, cmap = cmap, corner = (3,8,6,9))
make_image(file, 'figures/rectangle_5_3_out_window.png', show_window = True, add_values = False,
           window_type = "rectangle", window = window, cmap = cmap, corner = (3,8,6,9))











