'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger

last modified: 12.2.19

'''

#!/usr/bin/python

'''
This file extracts radial field values from OpenFoam data

What you have to do is:
- check if scalarTail and speciesTail in line 18&19 corresponds to your sampled output fiĺes in sampleDict/TIME
- datapoints and noFiles ind line 22 & 23 is correct, therefore you have to check the length of your files!
- check if Output_np and Output_df in line 120 and 129 comprise all the arrays you need or if something is missing!

'''

import numpy as np
import pandas as pd
from os import listdir
from os.path import isdir


def radial_samples_reacting(case_path):
    # this one has to be correct and is different for inert and reacting
    scalarTail = '_dQMean_dQPrime2Mean_cellVolumes.xy'

    # initialize arrays
    datapoints = 200
    noFiles = 40

    # represents the different locations you defined in the sample dict file
    nLocation = [0, 1, 2, 3, 4, 5, 6]
    location_dict = ['010', '050', '100', '120', '150', '200', '300']

    # get all time steps
    times = listdir(case_path+'/postProcessing/sampleDict/')
    # remove the .txt files in the times list as they are also stored in the sampleDict folder
    times = [f for f in times if f[-3:] != 'txt']

    # loop over the time steps for averaging

    for n in range(0, len(nLocation)):
        arraydQ = np.zeros((datapoints))
        arraydQRMS = np.zeros((datapoints))
        arrayVols = np.zeros((datapoints))

        arrayDist = np.zeros((datapoints))

        for time in times:
            for j in range(0, noFiles):
                try:
                    dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict_dQ/' + time + '/line_x' +
                                            str(nLocation[n]) + '-r' + str(j) + scalarTail)
                except:
                    print('Check the file name and/or path of scalar fields! Something is wrong')
                    print(case_path + '/postProcessing/sampleDict_dQ/' + time + '/line_x' + str(nLocation[n]) + '-r' + str(j) + scalarTail)

                # there is the position of the T column in your data set;
                # check for consistency! they are summed up for different j
                arraydQ += dataScalar[:, 3]
                arraydQRMS += np.sqrt(dataScalar[:, 4])
                arrayVols += (dataScalar[:, 5])

                # compute the radius only once at the beginning
                if j == 0 and time == times[0]:
                    arrayYPos = dataScalar[:, 1]    # m
                    arrayZPos = dataScalar[:, 2]    # m
                    arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)

            # loop 2 end

        # set up to write the output file!
        Output_np = np.array((arrayDist, arraydQ, arraydQ/arrayVols ,arraydQRMS))

        # Divide by the number of files and times and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['r_in_m', 'dQ_mean', 'heatRelease','dQ_rms']

        Output_df['r_in_m'] = arrayDist

        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = case_path+'/postProcessing/sampleDict_dQ/' + 'line_xD' + location_dict[n] + '_dQ_TNF14.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')

    print('OK')


if __name__ == "__main__":
    radial_samples_reacting('.')
