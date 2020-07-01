#!/usr/bin/python3

'''
This file extracts the sampled Data to plot a scatter plot, e.g. f-T

What you have to do:
- check if all the data is collected which you need; otherwise extend it to your needs at the end of the 2nd for-loop

'''

import numpy as np
import pandas as pd
import os
#import matplotlib.pyplot as plt
from os.path import join
import os

# try:
#     from matplotlib2tikz import save as tikz_save
# except:
#     print('Install matplotlib2tikz: pip3 install matplotlib2tikz')

mypath = 'postProcessing/preview' #input('Where is the scatter data?, (e.g. preview) type in: ')

# f_BilgerMax Sandia
f_max = 1

storePath = 'scatter' #input('Where do you want to save the data?, (e.g. ../scatter) type in: ')
# alternatively you just provide the path hard coded

# get all the subdirectories file names (sampled time steps)
timeDict=os.listdir(mypath)

nSets = len(timeDict)
# noch automatisieren
nPoints = 22000
nEntries = nPoints*nSets

location_dict =['07.5','10','15','30','45']
nLocation = np.linspace(0,len(location_dict)-1,len(location_dict))

scatter_list = os.listdir(join(mypath,timeDict[0]))

fields_list = [f.split('_scatter_xD10.raw')[0] for f in scatter_list if f.endswith('_scatter_xD10.raw')]

# create scatter directory
if os.path.isdir('scatter') is False:
    os.mkdir('scatter')


# Four axes, returned as a 2-d array
#f, axarr = plt.subplots(4, 2)
isodd = lambda x: 1 if x %2 != 0 else 0

# loop over the different planes normal to x-axis
for n in range(0, len(nLocation)):
    print('Processing scatter data from position x/D='+location_dict[n])

    data_array = np.zeros((nEntries, len(fields_list)))

    counter_array = np.zeros(len(fields_list))
    # loop over the data sets
    for i in range(0,nSets):
        #print(timeDict[i])
        for id, field in enumerate(fields_list):
            this_path = join(mypath, timeDict[i], field + '_scatter_xD' + location_dict[n] + '.raw')
            print(this_path)
            #print(field)
            this_scatter = np.loadtxt(this_path)
            #print(join(mypath, timeDict[i], field + '_scatter_xD' + location_dict[n] + '.raw'))
            length = len(this_scatter)
            #print(this_scatter)
            data_array[int(counter_array[id]):int(counter_array[id] + length),id] = this_scatter[:, 3]
            # if field == 'f':
            #     print('f is: ', this_scatter[:, 3][:100])
            counter_array[id] += length
        # end loop

    #end loop

    # compose the output array
    # Output_np = np.array((arrayT, arrayf, arrayPV, arrayCH4, arrayCO2))

    Output_df = pd.DataFrame(data_array,columns=fields_list)
    #Output_df = Output_df.T
    #Output_df.columns = ['T', 'f_Bilger', 'PV', 'CH4', 'CO2']

    # skip all data where T is < 300.5
    print('Keep only the data points where T > 295 K')
    Output_df = Output_df[Output_df['T'] > 291].sample(30000)

    #Output_df['f'] = Output_df['f_Bilger'] / f_max

    output_name = storePath+'/scatter_xD' + location_dict[n] + '.txt'
    pd.DataFrame.to_csv(Output_df,output_name,index=False,sep='\t')

    # create scatter plot for all distances
    '''
    plt.figure(n+1)
    plt.scatter(arrayf,arrayT,marker='.',s=0.3)
    plt.xlabel('Mixture fraction f')
    plt.ylabel('Temperature')
    plt.xlim(0,0.3)
    plt.ylim(301,2400)
    plt.title('Scatter plot at: x/D='+str(int(location_dict[n])/10))
    '''

#     axarr[int(n/2), isodd(n)].scatter(Output_df['f_Bilger'],Output_df['T'],marker='.',s=0.3)
#     axarr[int(n/2), isodd(n)].set_title('Scatter plot at: x/D='+str(float(location_dict[n])/10))
#     axarr[int(n / 2), isodd(n)].set_xlim([0,0.3])
#     axarr[int(n / 2), isodd(n)].set_ylim([300,2350])
#     axarr[int(n / 2), isodd(n)].set_ylabel('T [K]')
#     axarr[int(n / 2), isodd(n)].set_xlabel('f')
#
#     # save tikz
#     # tikz_save('scatter'+location_dict[n]+'.tex')
#
# #end loop
# f.subplots_adjust(hspace=0.5)
# plt.show(block=False)







