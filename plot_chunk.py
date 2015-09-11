import pdb
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

"""
takes dict of blocks in format below and plots according to plot_dict into a 3d scatter plot
block_dict = {
    (x,z,y):'stone'
}
"""

plot_dict = {
        'diamond':('blue', 'D'),
        'gold':('yellow', 'D'),
        'iron':('white', 'D'),
        'coal':('white', 'D'),
        'redstone':('red', 'D'),
        'stone':('white', 's'),
        'dirt':('white', 's'),
        'gravel':('white', 's'),
        'bedrock':('white', 's'),
        }


def get_subset_of_type(unfiltered_block_array, block_type):
    subset_dict = {}
    for key in unfiltered_block_array:
        if unfiltered_block_array[key] == block_type:
            subset_dict[key] = block_type
    return subset_dict


def plot_blocks(block_array_to_plot):
    assert type(block_array_to_plot) == dict
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for key in plot_dict.keys():
        try:
            array_subset = get_subset_of_type(block_array_to_plot, key)
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
    for y in range(0,16):
        for z in range(0,16):
            for x in range(0,16):
                blocks[(x, z, y)] = 'stone'
    """
    x = math.floor(i % x_length)
    y = (i // x_length) % y_length
    z = i // (x_length * y_length)
    """
    #pdb.set_trace()
    blocks[(5,5,5)] = 'diamond'
    #print blocks[(5,5,5)]

    #blocks = [
            #['stone', 0, 8, 2], 
            #['bedrock', 10, 3, 20], 
            #['diamond', 31, 39, 21],
            #['diamond', 3, 39, 21],
            #['diamond', 31, 9, 21],
            #]
    
    plot_blocks(blocks)

if __name__ == "__main__":
    main()
