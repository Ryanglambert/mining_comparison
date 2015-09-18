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
                    #print "section len is :", len(hold_section)
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
        #print "still running"
        returned_ores = return_contiguous_ores(returned_ores, block_layout)
        if len(returned_ores.keys()) <= prev_returned_ores_len:
            break
        prev_returned_ores_len = len(returned_ores.keys())
    return returned_ores

def return_blocks(mining_path, block_layout, block_filter_list):
    assert type(block_filter_list) == list
    assert type(mining_path) == list
    assert type(block_layout) == dict
    """takes a path, block layout, and filter list
    Returns: all ores that are adjacent to the path, and in the filter list
    """
    path_blocks = {}
    filtered_block_layout = get_subset_of_type(block_layout, block_filter_list)
    mining_path_with_adjacency = get_adjacency(mining_path)
    for i in mining_path_with_adjacency:
        try:
            path_blocks[i] = filtered_block_layout[i]
        except IndexError:
            continue
        except KeyError:
            continue
    hold_path_blocks = path_blocks.copy()
    path_blocks.update(return_all_contiguous_ores(hold_path_blocks, filtered_block_layout))
    return path_blocks

def get_path_blocks_with_coordinates(world, path, ore_count_dict, x_start, x_end, z_start, z_end, y_start, y_end):
    """ Takes: world, path, ore filter, coordinates
        Returns: path_blocks
    """
    try:
        set_of_chunks = get_set_of_chunk_sections(
                x1=x_start,
                x2=x_end,
                z1=z_start,
                z2=z_end,
                y1=y_start,
                y2=y_end,
                world=world)
    except InconceivedChunk:
        pass
    path_with_offset = []
    for n_tuple in range(len(path)):
        path_with_offset.append(
                (path[n_tuple][0] + x_start*16, path[n_tuple][1] + z_start*16, path[n_tuple][2] + y_start*16)
                )

    return return_blocks(path_with_offset, set_of_chunks, ore_count_dict.keys())

"""
    this code needs it's own function

    num_blocks_mined = 0
    for ore in ore_count_dict.keys():
        ore_count_dict[ore] += len(return_blocks(path, set_of_chunks, [ore]))
    num_blocks_mined += sum(ore_count_dict.values()) + len(path)
    return num_blocks_mined, ore_count_dict
"""

def main():
### data
    ore_count = {
            'iron':0,
            'diamond':0,
            'redstone':0,
            'coal':0,
            'gold':0
            }

### path information
    path = []
    for x in xrange(2, 33, 4):
        for z in xrange(33):
            for y in range(5,8):
                path.append((x,z,y))

### simulate one set and tally ores
    world = load_world('/Users/ryanlambert/minecraft-server-new/world')


## visual confirmation of ores
    plot_chunk.plot_blocks(
       path_plot=path, 
       blocks_to_plot=get_path_blocks_with_coordinates(
           world,
           path,
           ore_count,
           x_start=1,
           x_end=3,
           z_start=0,
           z_end=2,
           y_start=0,
           y_end=2)
       )

if __name__ == "__main__":
    main()
