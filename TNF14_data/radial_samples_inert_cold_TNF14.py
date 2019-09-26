'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger
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


def radial_samples_inert(case_path='.'):
    # this one has to be correct and is different for inert and reacting

    #scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean_O2Mean_O2Prime2Mean_CH4Mean_CH4Prime2Mean_CO2Mean_CO2Prime2Mean_TMean_TPrime2Mean.xy'
    scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean.xy'

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

        arrayf = np.zeros((datapoints))
        arrayfRMS = np.zeros((datapoints))

        arrayU = np.zeros((datapoints))
        arrayURMS = np.zeros((datapoints))
        arrayV = np.zeros((datapoints))
        arrayVRMS = np.zeros((datapoints))
        arrayW = np.zeros((datapoints))
        arrayWRMS = np.zeros((datapoints))

        arrayJ_sgs = np.zeros((datapoints))
        arrayJ_lam = np.zeros((datapoints))
        arrayJsgsRMS_r = np.zeros((datapoints))
        arrayJlamRMS_r = np.zeros((datapoints))
        arrayVol = np.zeros((datapoints))
        arrayCell = np.zeros((datapoints))
        arrayJsgs_r = np.zeros((datapoints))
        arrayJlam_r = np.zeros((datapoints))
        # Koordinate Position
        #arrayYPos = np.zeros((datapoints))
        #arrayZPos = np.zeros((datapoints))
        #arrayDist = np.zeros((datapoints))

        for time in times:
            for j in range(0, noFiles):
                try:
                    # try:

                    this_path = case_path+'/postProcessing/sampleDict/' + time + '/line_x'+str(nLocation[n]) + '-r' + str(j) + scalarTail
                    print(this_path)
                    dataScalar = np.loadtxt(this_path)
                    # except OSError:
                    #     dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                    #                         str(nLocation[n]) + '-r' + str(j) + scalarTail2)

                    # there is the position of the T column in your data set; check for consistency! they are summed up for different j
                    arrayf += dataScalar[:, 3]
                    arrayfRMS += np.sqrt(dataScalar[:, 4])

                except:
                    print('Check the file name and/or path of scalar fields! Something is wrong')
                    print(this_path)

                # compute the radius only once at the beginning
                if j == 0 and time == times[0]:
                    arrayYPos = dataScalar[:, 1]
                    arrayZPos = dataScalar[:, 2]
                    arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)

                # #READ IN U ONLY IF PRESENT
                # try:
                #     dataU = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                #                        str(nLocation[n]) + '-r' + str(j) + '_UMean.xy')
                #
                #     winkel = 2 * j / noFiles * 3.14
                #
                #     arrayU += dataU[:, 3]
                #     arrayV += np.sin(winkel) * dataU[:, 4] + np.cos(winkel) * dataU[:, 5]
                #     arrayW += np.cos(winkel) * dataU[:, 4] + np.sin(winkel) * dataU[:, 5]
                #
                # except:
                #     print('Check the file name of U! Something is wrong') # or only with scalar fluxes


                # RMS
                try:
                    dataURMS = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time +
                                          '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean_J_sgsPrime2Mean_J_lamPrime2Mean.xy')

                    winkel = 2 * j / noFiles * 3.14

                    arrayURMS += np.sqrt(dataURMS[:, 3])
                    arrayVRMS += np.sqrt(np.sin(winkel) * dataURMS[:, 4] + np.cos(winkel) * dataURMS[:, 5])
                    arrayWRMS += np.sqrt(np.cos(winkel) * dataURMS[:, 4] + np.sin(winkel) * dataURMS[:, 5])

                    arrayJsgsRMS_r += np.sqrt((np.sin(winkel) * dataURMS[:, 10] + np.cos(winkel) * dataURMS[:, 11])**2 +
                                           (np.cos(winkel) * dataURMS[:, 10] + np.sin(winkel) * dataURMS[:, 11])**2)

                    arrayJlamRMS_r += np.sqrt((np.sin(winkel) * dataURMS[:, 16] + np.cos(winkel) * dataURMS[:, 17])**2 +
                                           (np.cos(winkel) * dataURMS[:, 16] + np.sin(winkel) * dataURMS[:, 17])**2)

                except:
                    print('Check the file name of U! Something is wrong')


                # #READ IN URMS ONLY IF PRESENT
                # try:
                #     dataURMS = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                #                        str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')
                #
                #     winkel = 2 * j / noFiles * 3.14
                #
                #     arrayURMS += dataU[:, 3]
                #     arrayVRMS += np.sin(winkel) * dataU[:, 4] + np.cos(winkel) * dataU[:, 5]
                #     arrayWRMS += np.cos(winkel) * dataU[:, 4] + np.sin(winkel) * dataU[:, 5]
                #
                # except:
                #     print('Check the file name of U! Something is wrong') # or only with scalar fluxes


                # IN CASE THE MEAN SCALAR FLUXES ARE PRESENT
                try:


                    dataJ = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                       str(nLocation[n]) + '-r' + str(j) + '_UMean_J_sgsMean_J_lamMean.xy')

                    print('U and Scalar Fluxes are processed.')

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

                # READ IN THE CELL VOLUME IF PRESENT
                try:
                    dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                            str(nLocation[n]) + '-r' + str(j) + '_cellVolumes.xy')

                    # there is the position of the T column in your data set; check for consistency! they are summed up for different j
                    arrayVol += dataScalar[:, 3]
                    arrayCell += np.cbrt(dataScalar[:, 3])

                except:
                    print('NO CELL VOLUME INFORMATION!')

            # loop 2 end

        # set up to write the output file!
        Output_np = np.array((arrayDist, arrayf, arrayU, arrayV, arrayW, arrayfRMS, arrayURMS, arrayVRMS, arrayWRMS,
                              arrayJsgs_r, arrayJlam_r, arrayJsgsRMS_r, arrayJlamRMS_r))

        # Divide by the number of files and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['r_in_m', 'Z_mean', 'U_axial_mean', 'U_radial_mean', 'U_teta_mean',
                             'Z_rms','U_axial_rms', 'U_radial_rms', 'U_teta_rms',
                             'J_sgs_mean','J_lam_mean','J_sgsRMS_mean','J_lamRMS_mean']

        Output_df['r_in_m'] = arrayDist

        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = case_path+'/postProcessing/sampleDict/' + 'line_xD' + location_dict[n] + '_TNF14.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')

    print('Sampled case: %s \n' % case_path)

# run it
if __name__ == "__main__":
    radial_samples_inert('.')