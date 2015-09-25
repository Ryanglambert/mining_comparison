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
        'diamond':('#2ECDB1', 's'),
        'gold':('#DEDE00', 's'),
        'iron':('#969696', 's'),
        'coal':('#2D2D2D', 's'),
        'redstone':('#FF0102', 's'),
        #'lava':('green', '.'),
        #'water':('green', '.'),
        #'obsidian':('green', '.'),
        #'stone':('green', '.'),
        #'dirt':('green', '.'),
        #'gravel':('green', '.'),
        #'bedrock':('green', '.'),
        }

def get_subset_of_type(unfiltered_block_array, block_type):
    subset_dict = {}
    for key in unfiltered_block_array:
        if unfiltered_block_array[key] == block_type:
            subset_dict[key] = block_type
    return subset_dict

#def plot_blocks(blocks_to_plot, path_plot, xstart, xlim, zstart, zlim, ystart, ylim):
def plot_blocks(blocks_to_plot, path_plot):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if blocks_to_plot != None:
        for key in plot_dict.keys():
            try:
                array_subset = get_subset_of_type(blocks_to_plot, key)
                xs = [i[0] for i in array_subset.keys()]
                zs = [j[1] for j in array_subset.keys()]
                ys = [k[2] for k in array_subset.keys()]
                ax.scatter(xs, zs, ys, color=plot_dict[key][0], marker=plot_dict[key][1], label=key)
                ax.set_zlim3d([0, 16])
                #ax.set_xlim3d([xstart - 5,xlim + 5])
                #ax.set_ylim3d([zstart - 5,zlim + 5]) ### <<< intentional
                ax.set_xlabel('X Label')
                ax.set_ylabel('Z Label')
                ax.set_zlabel('Y Label')
                ax.legend()
            except KeyError:
                continue

    if path_plot != None:
        try:
            xs = [i[0] for i in path_plot]
            zs = [j[1] for j in path_plot]
            ys = [k[2] for k in path_plot]
            ax.scatter(xs, zs, ys, color='green', marker='|')
            ax.set_zlim3d([0, 33])
            #ax.set_xlim3d([xstart - 5,xlim + 5])
            #ax.set_ylim3d([zstart - 5,zlim + 5]) ### <<< intentional
            ax.set_xlabel('X Label')
            ax.set_ylabel('Z Label')
            ax.set_zlabel('Y Label')
        except KeyError:
            pass

    
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
