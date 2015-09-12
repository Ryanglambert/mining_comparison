from os import path
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

#class MinePathLayout:
    #def __init__(self, mining_path_3d_array):
        #self.mining_path_3d_array = mining_path_3d_array
        #self.mining_adjacency_1d_array = []
        #self.1d_sparse_adjacency_path_array = []
        #pass
    
    #def get_3d_truth_array(self):
        #return self.3d_sparse_truth_array

    #def get_1d_truth_array(self):
        #return self.1d_sparse_truth_array
    
    #def set_adjacent_blocks(self):
        #for i in self.get_1d_truth_array():
            #try:
                #self.3d_sparse_truth_array[] = 1
                #self.3d_sparse_truth_array[] = 1
                #self.3d_sparse_truth_array[] = 1
                #self.3d_sparse_truth_array[] = 1
                #self.3d_sparse_truth_array[] = 1
                #self.3d_sparse_truth_array[] = 1
            #except IndexError:
                #pass
    #pass

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
    takes 1d array of block id's and returns list of lists containing 4 values each
    [block-id string, x, z, y]
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
        except KeyError:
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
                print "x is: ", x_index
                print "z is: ", z_index
                print "y is: ", y_index
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
                except IndexError, ValueError:
                    continue
                except InconceivedChunk:
                    continue
    return set_of_sections

def main():
### todo
### keep track of location in the world (nested loops to grab chunks)
### each "test" will be on a "set" of chunk sections of the same altitude
    ### block locations will need to be indexed by (y + section_value*16)
### after each test I'll index to a new location and test again

    world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    #array = world.get_nbt(0,0)['Level']['Sections'][0]['Blocks']
    #plot_chunk.plot_blocks(convert_1darray_to_3d_positions(array))
    set_of_chunks = get_set_of_chunk_sections(0,10,0,10,0,10,world)
    #print type(set_of_chunks)
    diamonds = 0
    gold = 0
    iron = 0
    for i in set_of_chunks.values():
        if i == 'diamond':
            diamonds += 1
        elif i == 'gold':
            gold += 1
        elif i == 'iron':
            iron += 1

    print "num diamonds is: ", diamonds
    print "num gold is: ", gold
    print "num diamonds is: ", iron
    plot_chunk.plot_blocks(set_of_chunks)
    

if __name__ == "__main__":
    main()
