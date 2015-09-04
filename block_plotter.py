from os import path
import nbt 
import math

global x_chunk_section_size
global y_chunk_section_size
global z_chunk_section_size

x_chunk_section_size = 16
y_chunk_section_size = 16
z_chunk_section_size = 16


class mining_path:
    def __init__(self, 3d_sparse_truth_array):
        """one of these"""
        self.3d_sparse_truth_array = 3d_sparse_truth_array
        """ not sure which one I will use yet"""
        self.1d_sparse_truth_array = convert_3d_positions_to_1darray(3d_sparse_truth_array)
        pass
    
    def get_adjacent_blocks(self):
        for i in self.3d_sparse_truth_array:




def load_world(path_to_file):
    #script_dir = path.dirname("/Users/ryanlambert/minecraft-server-new/world/region/")
    #world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    return nbt.world.WorldFolder(path_to_file)
    pass

def load_section(world, x_chunk_coord, z_chunk_coord, y_chunk_coord):
    """
    load chunk section into memory
    """
    return world.get_nbt(x_chunk_coord, z_chunk_coord)['Sections'][y_chunk_coord]['Blocks']
    #world.get_nbt(1,1)['Level']['Sections'][0]['Blocks']
    pass

def convert_1darray_to_3d_positions(chunk_section_array):

    """
    x = math.floor(i % x_length)
    y = i // x_length
    z = i // (x_length * y_length)
    """
    pass

def convert_3d_positions_to_1darray(3d_array):
    """
    i = x + y*x_length + z*x_length*y_length
    return: 1D array with block ID's
    """

    pass


def visualize_chunk_section(chunk_section):
    convert_1darray_to_3d_positions
    """
    Mayavi to plot

    Takes a 4D array: 3 Coordinates and 1 State per block

    """
    pass


def main():
   pass 
    
    




if __name__ == "__main__":
    main()
