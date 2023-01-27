import bpy
import os
import numpy as np
import csv


# Directory containing the PLY files
file_dir = 'Z:/Collaboration_data/Lee_lab/cerebellum_mesh_lq_210422/'
csv_filename = 'file_list.csv'


test_sample = None # Number of sample cells to load. If None, loads them all.
#test_sample = 10


def save_filelist(visibility='allon'):

    file_list = sorted(os.listdir(file_dir))


    # Get the name from the ply list
    ply_list = [item for item in file_list if item.endswith('.ply')] # Get the high-resolution PLYs#

    if test_sample is not None:
        print('Creating csv for a subset of ', test_sample, ' cells ')
        ply_list = ply_list[:test_sample]

    else:
        print('Creating csv for all ',str(len(ply_list)) ,' cells ')

    file_arr = np.array(ply_list) # A list of the PLY filenames in the specified folder


    if visibility == 'rand':

        viewport_vis = np.random.randint(2, size=np.shape(file_arr)[0])
        render_vis = np.random.randint(2, size=np.shape(file_arr)[0])

    elif visibility == 'allon':
        viewport_vis = np.ones(shape=np.shape(file_arr), dtype='int32')
        render_vis = np.ones(shape=np.shape(file_arr), dtype='int32')

    elif visibility == 'alloff':
        viewport_vis = np.zeros(shape=np.shape(file_arr), dtype='int32')
        render_vis = np.zeros(shape=np.shape(file_arr), dtype='int32')

    # Create a spreadsheet-like data table with additional columns filled with random binary values
    sheet = np.vstack([file_arr,viewport_vis,render_vis])

    sheet_list = sheet.T.tolist() # Transpose the sheet to a python list of lists, so it can be saved as a csv with python-native imports.

    # Save the sheet as a csv spreadsheet.
    with open(os.path.join(file_dir,csv_filename), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sheet_list)

if __name__ == "__main__":

    save_filelist()
    #save_filelist(visibility='rand')
    #save_filelist(visibility='alloff')
    # save_filelist(visibility='allon')


    print('Finished creating filelist in csv: ', file_dir+csv_filename)
