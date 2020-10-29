'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger

last modified: April 2020

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
        scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean_TMean_TPrime2Mean_CH4Mean_CH4Prime2Mean_H2OMean_H2OPrime2Mean_CO2Mean_CO2Prime2Mean_O2Mean_O2Prime2Mean_COMean_COPrime2Mean_H2Mean_H2Prime2Mean.xy'

    except:

        scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean_TMean_TPrime2Mean_CH4Mean_' \
                 'CH4Prime2Mean_H2OMean_H2OPrime2Mean_CO2Mean_CO2Prime2Mean_O2Mean_O2Prime2Mean_COMean_COPrime2Mean_H2Mean_H2Prime2Mean.xy'

        print('NO DIFFUSIVE FLUXES ARE PRESENT!')

    print(scalarTail+'\n')

    # initialize arrays
    datapoints = 200
    noFiles = 40

    # represents the different locations you defined in the sample dict file
    nLocation = [0, 1, 2, 3, 4,5,6]
    location_dict = ['003', '006', '015', '0225', '03','06', '09']

    # get all time steps
    times = listdir(case_path+'/postProcessing/sampleDict/')
    # remove the .txt files in the times list as they are also stored in the sampleDict folder
    times = [f for f in times if f[-3:] != 'txt']
    times = [f for f in times if f.startswith('0.')]

    # loop over the time steps for averaging

    for n in range(0, len(nLocation)):
        arrayT = np.zeros((datapoints))
        arrayTRMS = np.zeros((datapoints))

        arrayCH4 = np.zeros((datapoints))
        arrayCH4RMS = np.zeros((datapoints))

        arrayCO = np.zeros((datapoints))
        arrayCORMS = np.zeros((datapoints))

        arrayCO2 = np.zeros((datapoints))
        arrayCO2RMS = np.zeros((datapoints))

        arrayH2O = np.zeros((datapoints))
        arrayH2ORMS = np.zeros((datapoints))

        arrayH2 = np.zeros((datapoints))
        arrayH2RMS = np.zeros((datapoints))

        arrayO2 = np.zeros((datapoints))
        arrayO2RMS = np.zeros((datapoints))

        arrayf = np.zeros((datapoints))
        arrayfRMS = np.zeros((datapoints))

        arrayU = np.zeros((datapoints))
        arrayURMS = np.zeros((datapoints))
        arrayV = np.zeros((datapoints))
        arrayVRMS = np.zeros((datapoints))
        arrayW = np.zeros((datapoints))
        arrayWRMS = np.zeros((datapoints))

        arrayJ_r_sgs = np.zeros((datapoints))
        arrayJ_r_lam = np.zeros((datapoints))
        arrayJsgs_r = np.zeros((datapoints))
        arrayJlam_r = np.zeros((datapoints))
        arrayVol = np.zeros((datapoints))

        # Koordinate Position
        #arrayYPos = np.zeros((datapoints))
        #arrayZPos = np.zeros((datapoints))
        #arrayDist = np.zeros((datapoints))

        for time in times:
            for j in range(0, noFiles):
                try:
                    dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                            str(nLocation[n]) + '-r' + str(j) + scalarTail)
                except:
                    print('Check the file name and/or path of scalar fields! Something is wrong')
                    print(case_path + '/postProcessing/sampleDict/' + time + '/line_x' + str(nLocation[n]) + '-r' + str(j) + scalarTail)

                # there is the position of the T column in your data set;
                # check for consistency! they are summed up for different j
                arrayf += dataScalar[:, 3]
                arrayfRMS += np.sqrt(dataScalar[:, 4])
                arrayT += dataScalar[:, 5]
                arrayTRMS += np.sqrt(dataScalar[:, 6])
                arrayCH4 += dataScalar[:, 7]
                arrayCH4RMS += np.sqrt(dataScalar[:, 8])
                arrayH2O += dataScalar[:, 9]
                arrayH2ORMS += np.sqrt(dataScalar[:, 10])
                arrayCO2 += dataScalar[:, 11]
                arrayCO2RMS += np.sqrt(dataScalar[:, 12])
                arrayO2 += dataScalar[:, 13]
                arrayO2RMS += np.sqrt(dataScalar[:, 14])
                arrayCO += dataScalar[:, 15]
                arrayCORMS += np.sqrt(dataScalar[:, 16])
                arrayH2 += dataScalar[:, 17]
                arrayH2RMS += np.sqrt(dataScalar[:, 18])

                # compute the radius only once at the beginning
                if j == 0 and time == times[0]:
                    arrayYPos = dataScalar[:, 1]    # m
                    arrayZPos = dataScalar[:, 2]    # m
                    arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)

                #READ IN U ONLY IF PRESENT
                try:
                    dataU = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                       str(nLocation[n]) + '-r' + str(j) + '_UMean.xy')

                    winkel = 2 * j / noFiles * 3.14

                    arrayU += dataU[:, 3]
                    arrayV += np.sin(winkel) * dataU[:, 4] + np.cos(winkel) * dataU[:, 5]
                    arrayW += np.cos(winkel) * dataU[:, 4] + np.sin(winkel) * dataU[:, 5]

                except:
                    print('Check the file name of U! Something is wrong')

                # RMS
                try:
                    try:
                        dataURMS = np.loadtxt(case_path + '/postProcessing/sampleDict/' + time +
                                              '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')
                    except:
                        dataURMS = np.loadtxt(case_path + '/postProcessing/sampleDict/' + time +
                                              '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean_J_sgsPrime2Mean_J_lamPrime2Mean.xy')
                except:
                    print('Check the file name of U! Something is wrong')

                winkel = 2 * j / noFiles * 3.14

                arrayURMS += np.sqrt(dataURMS[:, 3])
                arrayVRMS += (np.sqrt(dataURMS[:, 6]) + np.sqrt(dataURMS[:, 8]))*0.5 #np.sqrt(np.sin(winkel) * dataURMS[:, 6] + np.cos(winkel) * dataURMS[:,8])
                arrayWRMS +=  np.sqrt(np.cos(winkel) * dataURMS[:, 6] + np.sin(winkel) * dataURMS[:, 8])
                print(dataURMS[0,3:9])


                # IN CASE THE MEAN SCALAR FLUXES ARE PRESENT
                try:
                    dataJ = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                       str(nLocation[n]) + '-r' + str(j) + '_UMean_J_sgsMean_J_lamMean.xy')

                    winkel = 2 * j / noFiles * 3.14

                    # get the U data again, just in case dataU was not read in
                    arrayU += dataJ[:, 3]
                    arrayV += np.sin(winkel) * dataJ[:, 4] + np.cos(winkel) * dataJ[:, 5]
                    arrayW += np.cos(winkel) * dataJ[:, 4] + np.sin(winkel) * dataJ[:, 5]

                    #arrayJ_sgs += dataJ[:,6]
                    arrayJsgs_r += np.sqrt((np.sin(winkel) * dataJ[:, 7] + np.cos(winkel) * dataJ[:, 8])**2 +
                                           (np.cos(winkel) * dataJ[:, 7] + np.sin(winkel) * dataJ[:, 8])**2)

                    arrayJlam_r += np.sqrt((np.sin(winkel) * dataJ[:, 10] + np.cos(winkel) * dataJ[:, 11])**2 +
                                           (np.cos(winkel) * dataJ[:, 10] + np.sin(winkel) * dataJ[:, 11])**2)
                except:
                    print('NO J_SGS_MEAN AVAILABLE!')

                ## READ IN THE CELL VOLUME IF PRESENT
                # try:
                #     dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                #                             str(nLocation[n]) + '-r' + str(j) + '_cellVolumes.xy')
                #
                #     # there is the position of the T column in your data set; check for consistency! they are summed up for different j
                #     arrayVol += dataScalar[:, 3]
                #
                # except:
                #     print('NO CELL VOLUME INFORMATION!')

            # loop 2 end

        # set up to write the output file!
        Output_np = np.array((arrayDist, arrayf, arrayT, arrayCH4, arrayH2O, arrayCO2, arrayO2, arrayCO, arrayH2, arrayU,
                              arrayV,arrayW,arrayfRMS, arrayTRMS, arrayCH4RMS, arrayH2ORMS, arrayCO2RMS, arrayO2RMS,
                              arrayCORMS, arrayH2RMS, arrayURMS,arrayVRMS, arrayWRMS,arrayJsgs_r,arrayJlam_r))

        # Divide by the number of files and times and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['r_in_m', 'av_Z', 'av_T','av_CH4','av_H2O','av_CO2','av_O2','av_CO',
                 'av_H2','U_axial_mean','av_U_radial','av_U_teta','std_Z','std_T','std_CH4','std_H2O',
                 'std_CO2','std_O2','std_CO','std_H2','std_U_axial','std_U_radial','std_U_teta',
                 'av_J_sgs','av_J_lam']

        Output_df['r_in_m'] = arrayDist

        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        if location_dict[n] == '0225':
            output_name = case_path + '/postProcessing/sampleDict/' + 'line_x' + '022_5' + '_MRB.txt'
        elif len(location_dict[n]) ==2:
            output_name = case_path + '/postProcessing/sampleDict/' + 'line_x' + location_dict[n] + '0_MRB.txt'
        else:
            output_name = case_path+'/postProcessing/sampleDict/' + 'line_x' + location_dict[n] + '_MRB.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')


if __name__ == "__main__":
    radial_samples_reacting('.')