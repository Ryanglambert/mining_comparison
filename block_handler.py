from os import path
import pdb
import nbt
import math
import plot_chunk

global x_chunk_section_size
global y_chunk_section_size
global z_chunk_section_size
global x_index_step
global y_index_step 
global z_index_step 

x_chunk_section_size = 16
y_chunk_section_size = 16
z_chunk_section_size = 16
x_index_step = 1
y_index_step = y_chunk_section_size
z_index_step = z_chunk_section_size * y_chunk_section_size

block_id_dict = {
        0:'air',
        1:'stone',
        2:'dirt',
        3:'dirt',
        4:'cobblestone',
        5:'planks',
        7:'bedrock',
        8:'water',
        9:'water',
        10:'lava',
        11:'lava',
        12:'sand',
        13:'gravel',
        14:'gold',
        15:'iron',
        16:'coal',
        49:'obsidian',
        56:'diamond',
        73:'redstone',
        74:'redstone',
        129:'emerald',
        }

class MinePathLayout:
    def __init__(self, mining_path_3d_array):
        """accepts list of tuples
        Returns: original list of tuples plus adjacent tuples
        """
        self.mining_path_3d_array = mining_path_3d_array
        self.mining_path_adjacency = []
        for coordinate_tuple in mining_path_3d_array:
            self.mining_path_adjacency.append((coordinate_tuple[0] + 1,coordinate_tuple[1], coordinate_tuple[2]))
            self.mining_path_adjacency.append((coordinate_tuple[0] - 1,coordinate_tuple[1], coordinate_tuple[2]))
            self.mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1] + 1, coordinate_tuple[2]))
            self.mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1] - 1, coordinate_tuple[2]))
            self.mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1], coordinate_tuple[2] + 1))
            self.mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1], coordinate_tuple[2] - 1))

class BlockLayout:
    def __init__(self, blocks):
        self.blocks = blocks
        
def load_world(path_to_file):
    return nbt.world.WorldFolder(path_to_file)

def get_subset_of_type(unfiltered_block_array, block_type):
    subset_dict = {}
    for key in unfiltered_block_array:
        if unfiltered_block_array[key] == block_type:
            subset_dict[key] = block_type
    return subset_dict

def convert_1darray_to_3d_positions(chunk_section_array, x_offset, z_offset, y_offset):
    """
    takes 1d array of block id's and 
    Returns: 
    {(x,z,y):'type'}
    """
    converted_array = {}
    for block_index in range(len(chunk_section_array)):
        try:
            converted_array[
                    (
                        (block_index % x_chunk_section_size) + x_offset * 16,
                        ((block_index // x_chunk_section_size) % z_chunk_section_size) + z_offset * 16,
                        (block_index // (x_chunk_section_size * z_chunk_section_size)) + y_offset * 16
                    )
                ] = block_id_dict[chunk_section_array[block_index]]
        except KeyError, IndexError:
            continue

    return converted_array

def get_set_of_chunk_sections(x1, x2, z1, z2, y1, y2, world):
    """ takes chunk coordinates (block_coordinate // 16)
    Returns concatenated dicitonary of block id's
    """
    set_of_sections = {}

    for x_index in xrange(x1, x2):
        for z_index in xrange(z1, z2):
            for y_index in xrange(y1, y2):
                #print "x is: ", x_index
                #print "z is: ", z_index
                #print "y is: ", y_index
                try:
                    hold_section = convert_1darray_to_3d_positions(
                            world.get_nbt(x_index, z_index)['Level']['Sections'][y_index]['Blocks'],
                            x_index,
                            z_index,
                            y_index
                            )
                    print "section len is :", len(hold_section)
                    for key in hold_section:
                        set_of_sections[key] = hold_section[key]
                except IndexError:
                    continue
                except ValueError:
                    continue
                except InconceivedChunk:
                    continue
    return set_of_sections

def return_blocks(mining_path, block_layout):
    assert type(mining_path) == list
    assert type(block_layout) == dict
    """takes a path and a set of blocks
    Returns: all ores that are adjacent to the path, perhaps also the size of the ore?
    """
    returned_blocks = {}
    for i in mining_path:
        try:
            returned_blocks[i] = block_layout[i]
        except IndexError:
            continue
        except KeyError:
            continue
    return returned_blocks

def main():
### todo
### keep track of location in the world (nested loops to grab chunks)
### each "test" will be on a "set" of chunk sections of the same altitude
    ### block locations will need to be indexed by (y + section_value*16)
### after each test I'll index to a new location and test again

    world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    set_of_chunks = get_set_of_chunk_sections(0,2,0,2,0,2,world)

    mine_path = MinePathLayout([(5, i, 5) for i in xrange(1,33)])
    #mine_path = MinePathLayout([
        #(5,1,5),
        #(5,2,5),
        #(5,3,5),
        #(5,4,5),
        #(5,5,5),
        #])

    adjacent_blocks = return_blocks(mine_path.mining_path_adjacency, set_of_chunks)
    plot_chunk.plot_blocks(adjacent_blocks)

if __name__ == "__main__":
    main()
