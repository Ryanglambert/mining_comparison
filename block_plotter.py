from os import path
import nbt 
import math


def load_world(path_to_file):
    return nbt.world.WorldFolder(path_to_file)

def convert_array_to_3d_positions(chunk_section_array):

    """
    x = (index-1) mod (Level Width)
    y = floor( (index-1) / (Level Width) )
    """
    x_width = 2
    z_width = 2
    block_dictionary = {}
    for i in range(len(chunk_section_array)):
        x_position = int((i) % x_width)
        z_position = int(math.floor(i / z_width))
        block_dictionary[(x_position,z_position)] = chunk_section_array[i]
    return block_dictionary


def visualize_chunk_section(chunk_section):
    pass



def main():
    #world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    
    #world.get_nbt(1,1)['Level']['Sections'][0]['Blocks']
    
    # TODO:
    # function that maps the world.get_nbt(x,z)['Level']['Sections'][0]['Blocks'] String to locations in a 16 x 16 x 16 block
    
    array = [1,2,3,4]
    convert_array_to_3d_positions(array)

    # layout mining pathway across length of N chunks where N is some symmetric layout

    #script_dir = path.dirname("/Users/ryanlambert/minecraft-server-new/world/region/")


if __name__ == "__main__":
    main()
