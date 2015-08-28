from os import path
import nbt 


### make an nbtfile
world = nbt.world.WorldFolder("world")

### get your chunk
world.get_nbt(1,1)['Level']['Sections'][0]['Blocks']

# TODO:
# function that maps the world.get_nbt(x,z)['Level']['Sections'][0]['Blocks'] String to locations in a 16 x 16 x 16 block


# layout mining pathway across length of N chunks where N is some symmetric layout




#script_dir = path.dirname("/Users/ryanlambert/minecraft-server-new/world/region/")
