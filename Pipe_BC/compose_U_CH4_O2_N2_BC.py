#python3

'''
File to read in Vector and Scalar Fields from 1 simulation and store it in singe time steps.
In this case: Pipemixing.
'''

import os
from os.path import join

# path to the main file
main_path = '/home/hansinger/Precursor_LES/mixing_75mm/'

org_timesteps = join(main_path,'postProcessing/preview/')

# make a new directory where to store the timesteps
output_dir = 'FJ200-5GP-Lr75-80_FUEL'
os.mkdir(output_dir)

# get a list of all timesteps
time_list = os.listdir(org_timesteps)

# this header needs to be inserted in every U entry
header_U = '/*--*- c++ -*-----*/ FoamFile { version 2.0; format ascii; class vectorAverageField; object values; } (0 0 0)'
header_scalar = '/*--*- c++ -*-----*/ FoamFile { version 2.0; format ascii; class scalarAverageField; object values; } 0'

myScalars = ['CH4','O2','N2']

# loop over timesteps
for time in time_list:

    current_data_U = org_timesteps+time+'/planeIn/vectorField/'
    current_data_Scalar = org_timesteps+ time+'/planeIn/scalarField/'

    # create a new time directory at output
    current_out_path = join(main_path, output_dir, time)
    try:
        os.mkdir(current_out_path)
    except FileExistsError:
        pass

    #####################################
    # now copy the files and insert the header
    # start with U
    outfile1 = open(current_out_path + '/U', 'w')      # output file
    outfile1.write(header_U)
    outfile1.write('\n')
    with open(current_data_U+'U') as file:
        data = file.read()
        outfile1.write(data)
    # print(data)
    outfile1.close()

    #####################################
    for scalar in myScalars:
        outfile2 = open(current_out_path + '/' + scalar, 'w')  # output file
        outfile2.write(header_scalar)
        outfile2.write('\n')
        with open(current_data_Scalar + scalar) as file:
            data = file.read()
            outfile2.write(data)
        # print(data)
        outfile2.close()

    print('Done with time %s' % time)


