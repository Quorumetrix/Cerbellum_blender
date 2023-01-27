import bpy
import csv
import os

# User-defined variables

x_scale = -0.055221
y_scale = -0.055221
z_scale = -0.055221

file_dir = 'Z:/Collaboration_data/Lee_lab/cerebellum_mesh_lq_210422/'
csv_filename = 'file_list.csv'

# Camera motion: static, pan or orbit
cam_motion = 'pan'


def recursive_layer_collection(layer_coll, coll_name):
    '''
    A function to help add nested collections.
    Input:
        layer_collection: string
        common_filename: string

    Returns:
        layer_coll: Layer collection name that refers to the collection coll_name
    '''

    found = None
    if (layer_coll.name == coll_name):
        return layer_coll
    for layer in layer_coll.children:
        found = recursive_layer_collection(layer, coll_name)
        if found:
            return found


def load_cell_models():

    '''
    Loads the cell reconstructions from PLY files.
        - Creates nested collections for each file type contained in the folder
            (inferred from the naming convention)
        - Loads the csv file and extracts the visibility info from the
        spreadsheet columns.
            First column is filename
            Second column is viewport visibility
            Third second column is render visibility
        - Loads each PLY file into the corresponding collection
        - Apply material to objects based on common segment of filename.
            (Only applied to Purkinje, Mossy and Granule, others have default material)
    '''


    # Get the common parts of the filenames to create collections.
    file_list = sorted(os.listdir(file_dir))

    # Get the name from the ply list
    ply_list = [item for item in file_list if item.endswith('.ply')] # Get the high-resolution PLYs#

    # Create a list of all the prefixes, the common segment of the ply filenames
    prefix_list = []

    for file in ply_list:

        prefix_list.append(file.split('_')[0])

    prefix_list = list(set(prefix_list)) # Get a unique list of prefixes to create separate collections

    # Create the high-level collection 'Cells'
    shared_assets_collection_name = 'Cells'
    collection = bpy.data.collections.new(shared_assets_collection_name)
    bpy.context.scene.collection.children.link(collection)

    # Create a collection for each prefix (~ cell type)
    for prefix in prefix_list:

        # One collection to hold all the trees
        collection = bpy.data.collections.new(prefix)
        bpy.data.collections.get(shared_assets_collection_name).children.link(collection)

    with open(os.path.join(file_dir,csv_filename), newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in filereader:

            filename = row[0]

            viewport_vis = int(row[1])
            render_vis = int(row[2])

            common_filename = filename.split('_')[0] # Extract common filename before the '_'

            curr_collection = bpy.data.collections[common_filename]

            #Change the Active LayerCollection
            layer_collection = bpy.context.view_layer.layer_collection
            layer_coll = recursive_layer_collection(layer_collection, common_filename)
            bpy.context.view_layer.active_layer_collection = layer_coll

            # Load PLY
            bpy.ops.import_mesh.ply(filepath=os.path.join(file_dir,filename))

            # Use the spreadsheet columns to set the object viewport and render visibility.
            if(viewport_vis == 0):
                bpy.context.object.hide_set(True)

            if(render_vis == 0):
                bpy.context.object.hide_render = True

    #        bpy.context.object.rotation_euler[0] = 1.5708 # Rotates so that z is up.
            bpy.context.object.scale[0] = x_scale
            bpy.context.object.scale[1] = y_scale
            bpy.context.object.scale[2] = z_scale

            # Apply materials based on collection / common filename
            obj = bpy.context.active_object

            if(common_filename == 'mf'):
                mat = bpy.data.materials.get('Mossy')
                obj.data.materials.append(mat)

            elif(common_filename == 'grc'):
                mat = bpy.data.materials.get('Granule')
                obj.data.materials.append(mat)

            elif((common_filename == 'purkinje') or (common_filename == 'pc')):
                mat = bpy.data.materials.get('Purkinje')
                obj.data.materials.append(mat)


def select_camera(motion='pan'):

    '''
    Selects the active camera in the scene.
    Input:
        motion: string, 'pan' (default), 'static', or 'orbit'
    '''

    if motion == 'static':

        bpy.context.scene.camera = bpy.context.scene.objects.get('Camera.static')

    elif motion == 'pan':

        bpy.context.scene.camera = bpy.context.scene.objects.get('Camera.pan')

    elif motion == 'orbit':

        bpy.context.scene.camera = bpy.context.scene.objects.get('Camera.orbit')


'''
This is the main control flow for the script:
In Blender it is not necessary to be in a
if __name__ == "__main__":   block, though it could be.
'''

load_cell_models()

select_camera(motion=cam_motion)
