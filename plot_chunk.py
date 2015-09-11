import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

"""
takes list of blocks in format below and plots according to plot_dict into a 3d scatter plot
#blocks = [
        #['type', x, z, y], 
        #]
#blocks = [
        #['stone', 0, 8, 2], 
        #['bedrock', 10, 3, 20], 
        #['diamond', 31, 39, 21],
        #['diamond', 3, 39, 21],
        #['diamond', 31, 9, 21],
        #]
"""

plot_dict = {
        'diamond':('blue', 'D'),
        'gold':('yellow', 'D'),
        'iron':('grey', 'D'),
        'coal':('black', 'D'),
        'redstone':('red', 'D'),
        'stone':('white', 's'),
        'dirt':('white', 's'),
        'gravel':('white', 's'),
        'bedrock':('white', 's'),
        }


def convert_block_id_to_scatter_color(block):
    block[0] = plot_dict[block[0]]
    return block

def convert_block_id_array_to_scatter_color_array(block_array):
    for block_index in xrange(len(block_array)):
        block_array[block_index] = convert_block_id_to_scatter_color(block_array[block_index])

def get_subset_of_type(unfiltered_block_array, block_type):
    return [i for i in unfiltered_block_array if i[0] == block_type]

def plot_blocks(block_array_to_plot):
    assert type(block_array_to_plot) == list
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for key in plot_dict.keys():
        array_subset = get_subset_of_type(block_array_to_plot,key)
        xs = [i[1] for i in array_subset]
        zs = [j[2] for j in array_subset]
        ys = [k[3] for k in array_subset]
        ax.scatter(xs, zs, ys, color=plot_dict[key][0], marker=plot_dict[key][1])
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Z Label')
    ax.set_zlabel('Y Label')
    
    plt.show()

def main():
    blocks = []
    for y in range(0,16):
        for z in range(0,16):
            for x in range(0,16):
                blocks.append(['stone', x, z, y]) 
    """
    x = math.floor(i % x_length)
    y = i // x_length
    z = i // (x_length * y_length)
    """
    bl = 253
    blocks[bl] = ['diamond',(bl % 16), (bl // 16) % 16, (bl // 256)]

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
