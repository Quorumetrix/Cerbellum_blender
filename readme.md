# Cerebellum-Blender

A collection of Blender-Python scripts for loading cell reconstruction models from PLY files.

- Begin by using ply_list_to_csv.py to create a csv file.
This script can be run in the Scripting window of the Blender GUI, or any other Python console.

 - The script generated a csv file, where each row is one of the PLY files, and the columns store boolean values for the viewport and render visibility of each loaded object.

-  By default, the csv will be created such that the visibility of all objects is on, however this can be modified by manually changing the values in the csv.

- save_filelist() can have optional arguments:
    - visibility='allon' # default
    - visibility = 'alloff'
    - visibility = 'rand'

This will save the csv to the same directory where the PLY files are located.


# Loading the files into Blender

Begin by opening the cerebellum_template.blend file contained in this repo. This Blender file contains cameras, materials, and scene lighting. There is a Blender version-specific template file for Blender 3.4.1

- From the Scripting window of the Blender GUI, load the script: 'load_filelist_csv.py'.

- Several user-defined variables are present at the top of the script.

- currently the x,y,z scale are identical to the original blend I was sent, at the values are compatible with the camera movements in the file.

- The user may also choose which default camera movement to activate: 'orbit', 'static', 'angled', or 'pan'


Ensure that csv_filename is the same as in ply_list_to_csv.py, and that the directory listed in file_dir has already had a csv generated.
You may make changes to the csv file to select which files to show.
- The first column of the csv is the filename,
- The second column contains 0 or 1 for whether or not to show the object in the viewport.
- The third column contains 0 or 1 for whether or not to render the object.

### Run the script
This will load cell models into nested collections, under the parent collection 'Cells'.
Each type of cell is automatically extracted from the filename, which is the collection name. This works by splitting the PLY filename at the first underscore, '_', and using the prefix as the collection name.
Note: This leads to some many collections being made, but that can easily be toggled on or off in the outliner of the Blender GUI by unchecking the box next to the collection name.

The template file contains several materials, one for each of the major cell types. They are automatically applied to the relevant cell type, using the prefix extracted from the PLY filename,
Note: purkinje cells were labeled both as 'purkinje' and 'pc' labels , so both of those collections will have the Purkinje material applied to their meshes.
