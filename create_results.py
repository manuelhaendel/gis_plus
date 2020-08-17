# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:23:25 2020

@author: Manuel
"""


import png
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


out = get_values(file, Circle(3), 7, 5, show_window = 1)

data = out
size = (5,5)
dpi = 80
cmap = 'RdYlBu'
cmap = mcolors.LinearSegmentedColormap.from_list("", [(1,1,1), (0,0.5,0)])

def make_image(data, outputname, size=(1, 1), dpi=80, cmap = 'hot'):
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    #ax.set_axis_off()
    
    fig.add_axes(ax)
    #plt.set_cmap(cmap)
    for col in range(np.size(data, 1)):
            for row in range(np.size(data, 0)):
                str = int(file[row, col])
                ax.text(col-0.25, row+0.2, str)
    
        
    ax.set_xticks(np.arange(-.5, 10, 1))
    ax.set_yticks(np.arange(-.5, 15, 1))
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    ax.tick_params(axis='both', which='both',length=0)

    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    ax.imshow(data, aspect='equal', cmap = cmap)
    ax.grid(which = "major", color = "k", linestyle='-', linewidth=2)
    
    # draw cricle
    center = (7, 5)
    radius = 3
    x = np.linspace(-radius, radius, 100)
    y = np.sqrt(radius**2 - x**2)
    x = center[1] + x
    x = np.concatenate((x, x[::-1]), 0)
    y_up = center[0] + y
    y_lo = center[0] - y
    y = np.concatenate((y_up, y_lo), 0)
    
    ax.plot(x, y, '-', linewidth=2.5, color='k')
    
    plt.show()
    plt.savefig(outputname, dpi=dpi)


make_image(out, 'figures/out.png', size=(4,6), cmap = 'RdYlBu')


img = plt.imread("figures/out.png")

fig, ax = plt.subplots()
# create x,y coordinates of circle


'''
fig = plt.figure()
fig.set_size_inches(size)
plt.plot(x,y)
'''

ax.imshow(img, extent=[0, 10, 0, 15])




