'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger

last change: 8.1.2018
'''

#!/usr/bin/python
'''

This file extracts radial field values from OpenFoam data


'''

import numpy as np
import pandas as pd
from os import listdir
from os.path import isdir


def radial_samples_reacting(case_path):
    # this one has to be correct and is different for inert and reacting
    #scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean_TMean_TPrime2Mean_CH4Mean_CH4Prime2Mean_H2OMean_H2OPrime2Mean_' \
    #             'CO2Mean_CO2Prime2Mean_O2Mean_O2Prime2Mean_COMean_COPrime2Mean_H2Mean_H2Prime2Mean.xy'

    scalarTail = '_k_sgsMean.xy'


    # initialize arrays
    datapoints = 200
    noFiles = 40

    # Diameter
    d_Sandia = 0.0072

    # f_BilgerMax Sandia
    f_max = 1

    # represents the different locations you defined in the sample dict file
    nLocation = [0, 1, 2, 3, 4]
    location_dict = [ '07.5',  '15',  '30', '45', '60']

    # get all time steps
    times = listdir(case_path+'/postProcessing/sampleDict_k_sgs/')
    # remove the .txt files in the times list as they are also stored in the sampleDict folder
    times = [f for f in times if f[-3:] != 'txt']

    # loop over the time steps for averaging

    for n in range(0, len(nLocation)):
        arrayU = np.zeros((datapoints))
        arrayURMS = np.zeros((datapoints))
        arrayV = np.zeros((datapoints))
        arrayVRMS = np.zeros((datapoints))
        arrayW = np.zeros((datapoints))
        arrayWRMS = np.zeros((datapoints))
        arrayk_sgs = np.zeros((datapoints))

        for time in times:
            for j in range(0, noFiles):
                try:
                    dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict_k_sgs/' + time + '/line_x' +
                                            str(nLocation[n]) + '-r' + str(j) + scalarTail)
                except:
                    print('Check the file name and/or path of scalar fields! Something is wrong')
                    print(case_path + '/postProcessing/sampleDict_k_sgs/' + time + '/line_x' + str(nLocation[n]) + '-r' + str(j) + scalarTail)
                    print(' ')

                # there is the position of the T column in your data set;
                # check for consistency! they are summed up for different j
                arrayk_sgs += dataScalar[:, 3]

                dataURMS = np.loadtxt(case_path + '/postProcessing/sampleDict_k_sgs/' + time +
                                      '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')

                winkel = 2 * j / noFiles * 3.14

                arrayURMS += dataURMS[:, 3]
                arrayVRMS += np.sin(winkel) * dataURMS[:, 4] + np.cos(winkel) * dataURMS[:,5]#dataURMS[:, 4]
                arrayWRMS += np.cos(winkel) * dataURMS[:, 4] + np.sin(winkel) * dataURMS[:, 5] # dataURMS[:, 5]

                # compute the radius only once at the beginning
                if j == 0 and time == times[0]:
                    arrayYPos = dataScalar[:, 1]    # m
                    arrayZPos = dataScalar[:, 2]    # m
                    arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)

            # loop 2 end


        # set up to write the output file!
        Output_np = np.array((arrayDist, arrayk_sgs,arrayURMS,arrayVRMS,arrayWRMS))

        # Divide by the number of files and times and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['r_in_m','TKE_sgs','U_Prime','V_Prime','W_Prime'] #tailNames

        Output_df['r_in_m'] = arrayDist

        Output_df['r_in_mm'] = arrayDist * 1000

        Output_df['r_over_d'] = Output_df['r_in_m'].values / 0.0072

        Output_df['TKE_resolved'] = (Output_df.U_Prime.values +Output_df.V_Prime.values + Output_df.W_Prime.values)/ 2 # np.sqrt(Output_df.U_Prime.values ** 2 +Output_df.V_Prime.values** 2 + Output_df.W_Prime.values** 2)/2

        Output_df['TKE_ratio'] = Output_df.TKE_sgs.values / (Output_df.TKE_sgs.values + Output_df.TKE_resolved.values)


        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = case_path+'/postProcessing/sampleDict_k_sgs/' + 'line_xD' + location_dict[n] + '_k_sgs.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')


if __name__ == '__main__':
    radial_samples_reacting('.')
