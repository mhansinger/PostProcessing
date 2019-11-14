'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger

last modified: Sept. 2019

OXYFUEL VERSION

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
    try:
        scalarTail = '_J_lamMean_J_sgsMean_J_H2Mean_J_H2_sgsMean_J_HMean_J_H_sgsMean_J_O2Mean_J_O2_sgsMean_J_H2OMean_J_H2O_sgsMean_J_CH4Mean_J_CH4_sgsMean_J_CO2Mean_J_CO2_sgsMean.xy'

    except:
        print('Something wrong!')

    print(scalarTail+'\n')

    # initialize arrays
    datapoints = 200
    noFiles = 40

    # represents the different locations you defined in the sample dict file
    nLocation = [0, 1, 2, 3, 4]
    location_dict = ['01', '03', '05', '10', '20']

    # get all time steps
    times = listdir(case_path+'/postProcessing/sampleDict_fluxes/')
    # remove the .txt files in the times list as they are also stored in the sampleDict folder
    times = [f for f in times if f[-3:] != 'txt']

    tailNames = scalarTail.split('Mean_')[:-1]
    tailNames[0] = tailNames[0][1:]
    # loop over the time steps for averaging

    for n in range(0, len(nLocation)):

        dataArray = np.zeros((datapoints, len(tailNames)))

        for time in times:
            for j in range(0, noFiles):

                dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict_fluxes/' + time + '/line_x'+str(nLocation[n]) + '-r' + str(j) + scalarTail)

                # print('Shape dataScalar: ', dataScalar.shape)

                # compute the radius only once at the beginning
                if j == 0 and time == times[0]:
                    arrayYPos = dataScalar[:, 1]    # m
                    arrayZPos = dataScalar[:, 2]    # m
                    arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)

                # IN CASE THE MEAN SCALAR FLUXES ARE PRESENT

                winkel = 2 * j / noFiles * 3.14

                for k in range(len(tailNames)):
                    # dataArray[:,k] += np.sqrt((np.sin(winkel) * dataScalar[:, k] + np.cos(winkel) * dataScalar[:, k])**2 +(np.cos(winkel) * dataScalar[:, k] + np.sin(winkel) * dataScalar[:, k])**2)
                    y_flux = (k+1)*3 + 1
                    z_flux = (k+1)*3 + 2
                    dataArray[:, k] += np.sqrt(dataScalar[:, y_flux]**2 + dataScalar[:, z_flux]**2)

            # loop 2 end

        # # set up to write the output file!
        # Output_np = np.array((arrayDist, arrayf, arrayT, arrayCH4, arrayH2O, arrayCO2, arrayO2, arrayCO, arrayH2, arrayU,
        #                       arrayV,arrayW,arrayfRMS, arrayTRMS, arrayCH4RMS, arrayH2ORMS, arrayCO2RMS, arrayO2RMS,
        #                       arrayCORMS, arrayH2RMS, arrayURMS,arrayVRMS, arrayWRMS,arrayJsgs_r,arrayJlam_r,arrayVol))

        # Divide by the number of files
        Output_T = dataArray/ (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = tailNames

        Output_df['r_in_m'] = arrayDist

        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = case_path+'/postProcessing/sampleDict_fluxes/' + 'line_xD' + location_dict[n] + '_fluxes_OxyFuel.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')


if __name__ == "__main__":
    radial_samples_reacting('.')