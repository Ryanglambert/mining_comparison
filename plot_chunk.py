import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

plot_dict = {
        'diamond':('blue', 'D'),
        'gold':('yellow', 'D'),
        'iron':('grey', 'D'),
        'redstone':('red', 'D'),
        'stone':('white', 's'),
        'gravel':('white', 's'),
        'bedrock':('black', 's'),
        }


def convert_block_id_to_scatter_color(block):
    block[0] = plot_dict[block[0]]
    return block

def convert_block_id_array_to_scatter_color_array(block_array):
    for block_index in xrange(len(block_array)):
        block_array[block_index] = convert_block_id_to_scatter_color(block_array[block_index])

def get_subset_of_type(unfiltered_block_array, block_type):
    return [i for i in unfiltered_block_array if i[0] == block_type]

def plot_blocks_of_type(block_array_to_plot):
    assert type(block_array_to_plot) == list
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for color, marker in [
            plot_dict['diamond'],
            ]:
        xs = [i[1] for i in block_array_to_plot]
        ys = [j[2] for j in block_array_to_plot]
        zs = [k[3] for k in block_array_to_plot]
        ax.scatter(xs, ys, zs, color=color, marker=marker)
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Z Label')
    ax.set_zlabel('Y Label')
    
    plt.show()

def main():
    blocks = [
            ['stone', 0, 8, 2], 
            ['bedrock', 10, 3, 20], 
            ['diamond', 31, 39, 21],
            ['diamond', 3, 39, 21],
            ['diamond', 31, 9, 21],
            ]
    subset = get_subset_of_type(blocks, 'diamond')
    print subset
    
    #plot_blocks_of_type(blocks)

if __name__ == "__main__":
    main()
