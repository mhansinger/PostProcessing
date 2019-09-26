#python3

'''
File to read in the input boundary conditions from two different precursor simulations.
In this case: annulus and pipe simulation. Ideally in both simulations you have written out the fields at the same, fixed 
time steps; makes life a lot easier. 
'''

import os
#from io import open

# path to annulus time steps
annulus_path = '/home/hansinger/Precursor_LES/annulus/postProcessing/preview/'

# path to pipe time steps
pipe_path = '/home/hansinger/Precursor_LES/pipe/postProcessing/preview/'

# output paths
out_path_pipe = '/home/hansinger/Precursor_LES/boundaryData/FUEL/'
out_path_annulus = '/home/hansinger/Precursor_LES/boundaryData/AIR/'

# this header needs to be inserted in every U entry
header = '/*-----*- c++ -*-----*/ FoamFile { version 2.0; format ascii; class vectorAverageField; object values; } (0 0 0)'

# loop over the time steps, first check, if time steps in pipe and annulus are the same, then you need only one loop
annulus_list = os.listdir(annulus_path)
pipe_list = os.listdir(pipe_path)

if annulus_list == pipe_list:
    # one loop is enough

    for time in annulus_list:
        #####################################
        # for annulus
        #####################################
        this_annu_out = out_path_annulus+time
        # create a new time directory at output
        try:
            os.mkdir(this_annu_out)
        except FileExistsError:
            pass
        # copy the U file
        #copy2(annulus_path+time+'/planeIn/vectorField/U',this_annu_out)

        # insert header in first line of U field
        outfile = open(this_annu_out+'/U', 'w')
        outfile.write(header)
        outfile.write('\n')
        with open(annulus_path+time+'/planeIn/vectorField/U') as file:
            data = file.read()
            outfile.write(data)
           # print(data)
        outfile.close()

        #####################################
        # for pipe
        #####################################

        this_pipe_out = out_path_pipe + time
        # create a new time directory at output
        try:
            os.mkdir(this_pipe_out)
        except FileExistsError:
            pass
        # copy the U file
        # copy2(annulus_path+time+'/planeIn/vectorField/U',this_annu_out)

        # insert header in first line of U field
        outfile2 = open(this_pipe_out + '/U', 'w')
        outfile2.write(header)
        outfile2.write('\n')
        with open(pipe_path + time + '/planeIn/vectorField/U', 'r', encoding='utf-8') as file:
            data = file.read()
            outfile2.write(data)

        outfile2.close()

        print('Done with time %s' % time)


else:
    print('You need two for loops')
    # not yet implemented





