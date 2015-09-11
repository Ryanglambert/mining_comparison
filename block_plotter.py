from os import path
import nbt 
import math

global x_chunk_section_size
global y_chunk_section_size
global z_chunk_section_size
x_chunk_section_size = 16
y_chunk_section_size = 16
z_chunk_section_size = 16
global x_index_step
x_index_step = 1
global y_index_step 
y_index_step = y_chunk_section_size
global z_index_step 
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
        57:'diamond',
        73:'redstone',
        74:'redstone',
        129:'emerald',
        }

#class mining_path:
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
            
def load_world(path_to_file):
    #script_dir = path.dirname("/Users/ryanlambert/minecraft-server-new/world/region/")
    return nbt.world.WorldFolder(path_to_file)

def get_chunk_section(world,x_chunk_coordinate, z_chunk_coordinate):
    pass

def convert_data_values_to_titles(1dchunk_array):
    pass

def convert_1darray_to_3d_positions(chunk_section_array):
    """
    x = math.floor(i % x_length)
    y = i // x_length
    z = i // (x_length * y_length)
    """
    blocks[bl] = ['diamond',(bl % 16), (bl // 16) % 16, (bl // 256)]
    pass


def main():
    world = load_world('/Users/ryanlambert/minecraft-server-new/world')
    print world.get_nbt(0,0)['Level']['Sections'][0]['Blocks']
    

if __name__ == "__main__":
    main()
