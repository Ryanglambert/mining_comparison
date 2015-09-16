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
        21:'lapis',
        49:'obsidian',
        56:'diamond',
        73:'redstone',
        74:'redstone',
        129:'emerald',
        }

def load_world(path_to_file):
    return nbt.world.WorldFolder(path_to_file)

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

def get_adjacency(mining_path_3d_array):
    """accepts list of tuples
    Returns: original list of tuples plus adjacent tuples
    """
    mining_path_adjacency = []
    for coordinate_tuple in mining_path_3d_array:
        mining_path_adjacency.append((coordinate_tuple[0] + 1,coordinate_tuple[1], coordinate_tuple[2]))
        mining_path_adjacency.append((coordinate_tuple[0] - 1,coordinate_tuple[1], coordinate_tuple[2]))
        mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1] + 1, coordinate_tuple[2]))
        mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1] - 1, coordinate_tuple[2]))
        mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1], coordinate_tuple[2] + 1)) 
        mining_path_adjacency.append((coordinate_tuple[0] ,coordinate_tuple[1], coordinate_tuple[2] - 1))
    return mining_path_adjacency

def return_contiguous_ores(ores, block_layout):
    assert type(ores) == dict
    assert type(block_layout) == dict
    ores_to_return = ores
    for ore in ores.keys():
        try:
            if block_layout[ore] == block_layout[ore[0],ore[1] + 1,ore[2]] and (ore[0], ore[1] + 1, ore[2]) not in ores_to_return.keys():
                ores_to_return[ore[0],ore[1] + 1, ore[2]] = block_layout[ore[0],ore[1] + 1, ore[2]]
            if block_layout[ore] == block_layout[ore[0],ore[1] - 1 ,ore[2]] and (ore[0], ore[1] - 1, ore[2]) not in ores_to_return.keys():
                ores_to_return[ore[0],ore[1] - 1, ore[2]] = block_layout[ore[0],ore[1] - 1, ore[2]]
            if block_layout[ore] == block_layout[ore[0] + 1,ore[1] ,ore[2]] and (ore[0] + 1, ore[1], ore[2]) not in ores_to_return.keys():
                ores_to_return[ore[0] + 1,ore[1], ore[2]] = block_layout[ore[0] + 1,ore[1], ore[2]]
            if block_layout[ore] == block_layout[ore[0] - 1,ore[1] ,ore[2]] and (ore[0] - 1, ore[1], ore[2]) not in ores_to_return.keys():
                ores_to_return[ore[0] - 1,ore[1], ore[2]] = block_layout[ore[0] - 1,ore[1], ore[2]]
            if block_layout[ore] == block_layout[ore[0],ore[1],ore[2] + 1] and (ore[0], ore[1], ore[2] + 1) not in ores_to_return.keys():
                ores_to_return[ore[0],ore[1], ore[2] + 1] = block_layout[ore[0],ore[1], ore[2] + 1]
            if block_layout[ore] == block_layout[ore[0],ore[1],ore[2] - 1] and (ore[0], ore[1], ore[2] -1) not in ores_to_return.keys():
                ores_to_return[ore[0],ore[1], ore[2] - 1] = block_layout[ore[0],ore[1], ore[2] - 1]
        except KeyError:
            continue
    return ores_to_return

def get_subset_of_type(unfiltered_block_array, block_types):
    subset_dict = {}
    for key in unfiltered_block_array.keys():
        for block_type in block_types:
            if unfiltered_block_array[key] == block_type:
                subset_dict[key] = block_type
    return subset_dict

def return_all_contiguous_ores(returned_ores, block_layout):
    prev_returned_ores_len = len(returned_ores.keys())
    while True:
        print "still running"
        returned_ores = return_contiguous_ores(returned_ores, block_layout)
        if len(returned_ores.keys()) <= prev_returned_ores_len:
            break
        prev_returned_ores_len = len(returned_ores.keys())
    return returned_ores

def return_blocks(mining_path, block_layout, block_filter_list):
    assert type(mining_path) == list
    assert type(block_layout) == dict
    """takes a path and a set of blocks
    Returns: all ores that are adjacent to the path, perhaps also the size of the ore?
    """
    path_blocks = {}
    filtered_block_layout = get_subset_of_type(block_layout, block_filter_list)
    for i in mining_path:
        try:
            path_blocks[i] = filtered_block_layout[i]
        except IndexError:
            continue
        except KeyError:
            continue
    hold_path_blocks = path_blocks.copy()
    path_blocks.update(return_all_contiguous_ores(hold_path_blocks, filtered_block_layout))
    return path_blocks

def simulate_mine_path(path, ores_of_interest, set_of_chunks):
    assert type(path) == list
    assert type(ores_of_interest) == list
    assert type(set_of_chunks) == dict
    discovered_ores = {}
    pass
    
def main():
### todo
### keep track of location in the world (nested loops to grab chunks)
### each "test" will be on a "set" of chunk sections of the same altitude
    ### block locations will need to be indexed by (y + section_value*16)
### after each test I'll index to a new location and test again

    x_start = 32
    x_finish = 64
    z_start = 0
    z_finish = 32
    y_start = 0
    y_finish = 32
    world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    set_of_chunks = get_set_of_chunk_sections(2,4,0,2,0,2,world)

    path = []
    for x in xrange(2+(16*2), 33+(16*2), 4):
        for z in xrange(33):
            for y in range(5,8):
                path.append((x,z,y))

    ore_count = {
            'iron':0,
            'diamond':0,
            'redstone':0,
            'coal':0,
            'gold':0
            }
    for ore in ore_count.keys():
        ore_count[ore] += len(return_blocks(get_adjacency(path), set_of_chunks, [ore]))

    print ore_count

### visual confirmation of ores
    #iron = return_blocks(get_adjacency(path), set_of_chunks, ['iron'])
    #diamond = return_blocks(get_adjacency(path), set_of_chunks, ['diamonds'])
    #gold = return_blocks(get_adjacency(path), set_of_chunks, ['gold'])
    #redstone = return_blocks(get_adjacency(path), set_of_chunks, ['redstone'])
    #coal = return_blocks(get_adjacency(path), set_of_chunks, ['coal'])
    #discovered_ores = {}
    #discovered_ores.update(iron)
    #discovered_ores.update(diamond)
    #discovered_ores.update(gold)
    #discovered_ores.update(redstone)
    #discovered_ores.update(coal)

### visual confirmation of path
    #plot_chunk.plot_blocks(blocks_to_plot=discovered_ores, path_plot=path, xstart=32, xlim=64, zstart=0, zlim=32, ystart=0, ylim=32)
    plot_chunk.plot_blocks(path_plot=path, xstart=32, xlim=64, zstart=0, zlim=32, ystart=0, ylim=32)

if __name__ == "__main__":
    main()
