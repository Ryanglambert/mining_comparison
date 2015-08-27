from os import path
import nbt 


### make an nbtfile
nbtfile = nbt.region.RegionFile("r.-1.-1.mca")
### get your chunk
chunk = nbtfile.get_nbt(1,1)

### do things to your hcunk


print chunk['Level']['Sections'][0]['Blocks']
script_dir = path.dirname("/Users/ryanlambert/minecraft-server-new/world/region/")

mca_file = "r.-1.-1.mca"

