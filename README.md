# mining_comparison

### Overview 
The primary driver for this project is that it is **fun**.  It is also a project that covers a lot of different skillsets that I'd like to grow as a data analyst: Data Wrangling with Pandas, Inferential Stats, General Python, and communicating those results in notebook format.  

This project is broken into a 'back end' and a 'front end'.

The Front End - Minepath Evaluation with Cross-Validation.ipynb contains most of the code/data pertinent to configuring variables and data analysis.  

The Back End contains most of the code required to extract block id, coordinates, based on mining pathway array input.  It's not necessary to dig into the back end for any of the analysis.  Thus why it is simply imported into the notebook as a tool.  

### Back End
This is mostly represented by the "block_handler.py" module.  

This module takes a minecraft world folder, a given path array, a list of ore types to return then returns contiguous ores (entire veins) that were discovered for the given path iterated throughout a set of bounds given by the user.  

"plot_chunk.py" is briefly used to provide a 3d scatter plot to give a rudimentary confirmation that ores were in fact returned.  This is not used for explicit confirmation for large data sets, rather a brief "that looks ok" confirmation.  

Explicit confirmation of block_handler accuracy  was confirmed with much smaller datasets early in the writing of this module.  (eventually for the sake of completeness I'll come back to this and give a more rigorous demonstration that is presentable). 

### Front End
The 'front end' is everything found in the ipython notebook.  The majority of the analysis is done here with Pandas.  Given paths, ore_filters, and worlds are also defined from within the ipython notebook.  

1. Mining Efficiencies
1. Mining Pathway Definitions
    1. Mining Pathway Optimization
1. Confidence Intervals
1. Other Descriptive statistics



### More Notes
for reading the NBT Tags
http://minecraft.gamepedia.com/Chunk_format

using NBT
https://github.com/twoolie/NBT/blob/master/nbt/region.py

coordniates of regions:
    http://minecraft.gamepedia.com/Region_file_format
        regionX = (int)floor(chunkX / 32.0);
        regionZ = (int)floor(chunkZ / 32.0);
    

