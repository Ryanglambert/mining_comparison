import pdb
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import block_handler

"""
takes dict of blocks in format below and plots according to plot_dict into a 3d scatter plot
block_dict = {
    (x,z,y):'stone'
}
"""

plot_dict = {
        'diamond':('blue', 'h'),
        'gold':('yellow', 'h'),
        'iron':('white', 'h'),
        'coal':('white', 'h'),
        'redstone':('red', 'h'),
        #'stone':('white', '.'),
        #'dirt':('white', '.'),
        #'gravel':('white', '.'),
        #'bedrock':('white', '.'),
        }


def plot_blocks(block_array_to_plot):
    assert type(block_array_to_plot) == dict
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for key in plot_dict.keys():
        try:
            array_subset = block_handler.get_subset_of_type(block_array_to_plot, key)
            xs = [i[0] for i in array_subset.keys()]
            zs = [j[1] for j in array_subset.keys()]
            ys = [k[2] for k in array_subset.keys()]
            ax.scatter(xs, zs, ys, color=plot_dict[key][0], marker=plot_dict[key][1])
        except KeyError:
            continue
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Z Label')
    ax.set_zlabel('Y Label')
    
    plt.show()

def main():
    blocks = {}
    for y in range(0,32):
        for z in range(0,32):
            for x in range(0,32):
                blocks[(x, z, y)] = 'stone'
    """
    x = math.floor(i % x_length)
    y = (i // x_length) % y_length
    z = i // (x_length * y_length)
    """
    #pdb.set_trace()
    blocks[(5,5,5)] = 'diamond'
    blocks[(21,5,20)] = 'diamond'
    blocks[(16,5,16)] = 'diamond'
    blocks[(17,5,18)] = 'diamond'
    #print blocks[(5,5,5)]

    
    plot_blocks(blocks)

if __name__ == "__main__":
    main()
