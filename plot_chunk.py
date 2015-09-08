import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

plot_dict = {
        'diamond':('b', 'o')
        }

def plot_blocks(chunk_blocks):
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #n = 100
    #for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        #xs = randrange(n, 23, 32)
        #ys = randrange(n, 0, 100)
        #zs = randrange(n, zl, zh)
        #xs = 
        #ys = 
        #zs = 
        #ax.scatter(xs, ys, zs, c=c, marker=m)
    
    #ax.set_xlabel('X Label')
    #ax.set_ylabel('Y Label')
    #ax.set_zlabel('Z Label')
    
    #plt.show()
    pass

def convert_block_id_to_scatter_color(block):
    block[0] = plot_dict[block[0]]
    print block
    return block


chunk_blocks = [
        ['diamond', 4, 3, 5], 
        ['diamond', 3, 3, 2], 
        ['diamond', 1, 3, 2], 
        ['diamond', 0, 8, 2], 
        ['diamond', 10, 3, 20], 
        ['diamond', 31, 39, 21]
        ]


block = ['diamond', 1, 3, 2]
convert_block_id_to_scatter_color(block)
