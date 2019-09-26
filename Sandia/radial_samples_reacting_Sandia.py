'''
This is to postprocess the data again in the desired format as required for the TNF14 workshop

@author: mhansinger

last change: 8.1.2018
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
    #scalarTail = '_f_BilgerMean_f_BilgerPrime2Mean_TMean_TPrime2Mean_CH4Mean_CH4Prime2Mean_H2OMean_H2OPrime2Mean_' \
    #             'CO2Mean_CO2Prime2Mean_O2Mean_O2Prime2Mean_COMean_COPrime2Mean_H2Mean_H2Prime2Mean.xy'

    scalarTail = '_fMean_fPrime2Mean_TMean_TPrime2Mean_CH4Mean_CH4Prime2Mean_H2OMean_H2OPrime2Mean_CO2Mean_CO2Prime2Mean_O2Mean_O2Prime2Mean_COMean_COPrime2Mean_H2Mean_H2Prime2Mean.xy'


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
    times = listdir(case_path+'/postProcessing/sampleDict/')
    # remove the .txt files in the times list as they are also stored in the sampleDict folder
    times = [f for f in times if f[-3:] != 'txt']

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

        # arrayf_Sandia = np.zeros((datapoints))
        # arrayf_SandiaRMS = np.zeros((datapoints))

        arrayU = np.zeros((datapoints))
        arrayURMS = np.zeros((datapoints))
        arrayV = np.zeros((datapoints))
        arrayVRMS = np.zeros((datapoints))
        arrayW = np.zeros((datapoints))
        arrayWRMS = np.zeros((datapoints))

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
                    print(' ')

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

                try:
                    dataU = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
                                       str(nLocation[n]) + '-r' + str(j) + '_UMean.xy')
                except:
                    print('Check the file name of U! Something is wrong')

                winkel = 2 * j / noFiles * 3.14

                arrayU += dataU[:, 3]
                arrayV += np.sin(winkel) * dataU[:, 4] + np.cos(winkel) * dataU[:, 5]
                arrayW += np.cos(winkel) * dataU[:, 4] + np.sin(winkel) * dataU[:, 5]

                # RMS
                try:
                    dataURMS = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time +
                                          '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')
                except:
                    print('Check the file name of U! Something is wrong')

                winkel = 2 * j / noFiles * 3.14

                arrayURMS += np.sqrt(dataURMS[:, 3])
                arrayVRMS += np.sqrt(np.sin(winkel) * dataURMS[:, 4] + np.cos(winkel) * dataURMS[:,5])
                arrayWRMS += np.sqrt(np.cos(winkel) * dataURMS[:, 4] + np.sin(winkel) * dataURMS[:, 5])

            # loop 2 end

        # convert f_Bilger values
        arrayf = arrayf / f_max
        arrayfRMS = arrayfRMS/(f_max)

        # set up to write the output file!
        Output_np = np.array((arrayDist, arrayf, arrayT, arrayCH4, arrayH2O, arrayCO2, arrayO2, arrayCO, arrayH2, arrayU,
                              arrayV, arrayW, arrayfRMS,  arrayTRMS, arrayCH4RMS, arrayH2ORMS, arrayCO2RMS, arrayO2RMS,
                              arrayCORMS, arrayH2RMS, arrayURMS,arrayVRMS, arrayWRMS))

        # Divide by the number of files and times and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['r_in_m', 'F', 'T','YCH4','YH2O','YCO2','YO2','YCO',
                 'YH2','U_axial','U_radial','U_teta','Frms','Trms','YCH4rms','YH2Orms',
                 'YCO2rms','YO2rms','YCOrms','YH2rms','U_axialrms','U_radialrms','U_tetarms']

        Output_df['r_in_m'] = arrayDist
        Output_df['r_over_d'] = arrayDist/d_Sandia


        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = case_path+'/postProcessing/sampleDict/' + 'line_xD' + location_dict[n] + '_Sandia.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')


if __name__ == '__main__':
    radial_samples_reacting('.')
