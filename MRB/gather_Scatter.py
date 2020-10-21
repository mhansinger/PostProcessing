#!/usr/bin/python3

'''
This is for the OxyFuel Flame

This file extracts the sampled Data to plot a scatter plot, e.g. f-T

What you have to do:
- check if all the data is collected which you need; otherwise extend it to your needs at the end of the 2nd for-loop

'''

import numpy as np
import pandas as pd
import os
#import matplotlib.pyplot as plt
from os.path import join


mypath = 'postProcessing/preview' #input('Where is the scatter data?, (e.g. preview) type in: ')
storePath = 'scatter' #input('Where do you want to save the data?, (e.g. ../scatter) type in: ')
# alternatively you just provide the path hard coded

# get all the subdirectories file names (sampled time steps)
timeDict=os.listdir(mypath)


# check if scatter directory is there
if not os.path.isdir('scatter'):
    os.mkdir('scatter')

nSets = len(timeDict)
# noch automatisieren
# nPoints = 22000
# nEntries = nPoints*nSets

# represents the different locations you defined in the sample dict file
#nLocation = [0, 1, 2, 3, 4, 5, 6]
location_dict = ['03', '06', '15', '22.5', '30', '60', '90']

location_dict =['01','03','05','10','15','20','30']
nLocation = np.linspace(0,len(location_dict)-1,len(location_dict))

scatter_list = os.listdir(join(mypath,timeDict[0]))

fields_list = [f.split('_scatter_xD03.raw')[0] for f in scatter_list if f.endswith('_scatter_xD03.raw')]

# # Four axes, returned as a 2-d array
# f, axarr = plt.subplots(4, 2)
# isodd = lambda x: 1 if x %2 != 0 else 0

# loop over the different planes normal to x-axis

for n in range(0, len(nLocation)):
    print('Processing scatter data from position x/D=' + location_dict[n])

    data_array = np.zeros((0, len(fields_list)+1))  # +1 is the column for the radius

    #counter_array = np.zeros(len(fields_list))
    # loop over the data sets

    for i in range(0, nSets):
        # print(timeDict[i])
        for id, field in enumerate(fields_list):
            this_path = join(mypath, timeDict[i], field + '_scatter_xD' + location_dict[n] + '.raw')
            print(this_path)
            #print(field)
            try:
                this_scatter = np.loadtxt(this_path)
            except:
                print('Not found: %s ' % this_path)
                break
            # print(join(mypath, timeDict[i], field + '_scatter_xD' + location_dict[n] + '.raw'))
            length = len(this_scatter)
            # print(this_scatter

            if id == 0:
                # compute radius only once and set it at the beginning of the array
                radius = np.sqrt(this_scatter[:, 1] ** 2 + this_scatter[:, 2] ** 2)
                this_data_array = np.array((radius))
                this_data_array = np.vstack((this_data_array,this_scatter[:, 3]))
            
            else:
                this_data_array = np.vstack((this_data_array,this_scatter[:, 3]))
            
        data_array = np.vstack((data_array,this_data_array.T))
        print('shape data_array: ',data_array.shape)

    # end loop

    # compose the output array
    # Output_np = np.array((arrayT, arrayf, arrayPV, arrayCH4, arrayCO2))

    Output_df = pd.DataFrame(data_array, columns=['r_in_m']+fields_list)

    # skip all data where T is < 300.5
    print('Keep only the data points where T > 294.5 K')
    Output_df = Output_df[Output_df['T'] > 294.5].sample(30000)

    # # remove all Zero vals
    # print('Removing all zero values')
    # Output_df= Output_df.replace(0,np.nan)
    # Output_df = Output_df.dropna()

    output_name = storePath + '/scatter_xD' + location_dict[n] + '.txt'
    pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')




