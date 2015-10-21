from os import path
import pdb
import pandas as pd
import nbt
import math
import copy

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

def return_contiguous_ores(ores, block_layout, ignore_ores):
    assert type(ores) == dict
    assert type(ignore_ores) == dict
    assert type(block_layout) == dict
    ores_to_return = ores
    for ore in ores.keys():
        if ore not in ignore_ores.keys():
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
    ores_already_counted = {}
    while True:
        #print "still running"
        returned_ores = return_contiguous_ores(returned_ores, block_layout, ores_already_counted)
        ores_already_counted.update(returned_ores)
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
    hold_path_blocks = copy.deepcopy(path_blocks)
    path_blocks.update(return_all_contiguous_ores(hold_path_blocks, filtered_block_layout))
    return path_blocks

def generate_absolute_path(path, chunkx1, chunkx2, chunkz1, chunkz2, chunky1, chunky2):
    absolute_path = []
    for chunk_x in range(chunkx1 * 16, chunkx2 * 16, 48):
        for chunk_z in range(chunkz1 * 16, chunkz2 * 16, 48):
            for chunk_y in range(chunky1 * 16, chunky2 * 16, 48):
                for position in path:
                    absolute_path.append((position[0] + chunk_x, position[1] + chunk_z, position[2] + chunk_y))
    return absolute_path

def mine_blocks_with_path(world, path, ore_count_dict, x_start, x_end, z_start, z_end, y_start, y_end):
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
    except:
        pass
    return return_blocks(path, set_of_chunks, ore_count_dict.keys())

def simulation(x1, x2, z1, z2, y1, y2, relative_path, ore_count, world):
### ore filter
    blocks_found = {}
    total_ores = copy.deepcopy(ore_count)


### Generate patterned absolute path
    absolute_path = generate_absolute_path(relative_path, x1, x2, z1, z2, y1, y2)

### Mine!
    blocks = mine_blocks_with_path(
            world,
            absolute_path,
            ore_count,
            x_start=x1,
            x_end=x2,
            z_start=z1,
            z_end=z2,
            y_start=y1,
            y_end=y2)
### Tally up ores and blocks mined!
    for blocktype in blocks.values():
        ore_count[blocktype] += 1

    ## Plot!
    plot_chunk.plot_blocks(
        path_plot=None, 
        blocks_to_plot=blocks
        )
    return blocks, absolute_path

def main():

    world = load_world('/Users/ryanlambert/minecraft-server/world')

### path information
    relative_path = []
    for y_pattern in xrange(0, 3, 3):
        for x in xrange(6, 42, 12):
            for z in xrange(2, 48):
                for y in range(5 + y_pattern,7 + y_pattern):
                    relative_path.append((x,z,y))
            for z in xrange(3, 48, 4):
                for x_2 in xrange(x, x + 6):
                    for y in range(6 + y_pattern,7 + y_pattern):
                        relative_path.append((x_2,z,y))
                for x_3 in xrange(x - 5, x):
                    for y in range(6 + y_pattern,7 + y_pattern):
                        relative_path.append((x_3,z,y))
    ore_count = {
            'iron':0,
            'diamond':0,
            'redstone':0,
            #'coal':0,
            #'stone':0,
            'gold':0
            }

    simulation(x1=0, x2=3, z1=0, z2=3, y1=0, y2=1, relative_path=relative_path, ore_count=ore_count, world=world)
    #simulation(x1=0, x2=3, z1=0, z2=3, y1=0, y2=1)


if __name__ == "__main__":
    main()
