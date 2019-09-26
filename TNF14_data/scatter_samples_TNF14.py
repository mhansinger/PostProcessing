#!/usr/bin/python3

'''
This file extracts the sampled Data to plot a scatter plot, e.g. f-T

What you have to do:
- check if all the data is collected which you need; otherwise extend it to your needs at the end of the 2nd for-loop

@author: mhansinger

'''

import numpy as np
import pandas as pd
import os

try:
    from matplotlib2tikz import save as tikz_save
except:
    print('Install matplotlib2tikz: pip3 install matplotlib2tikz')


def scatter_samples(case_path,nr_samples=50000):
    # get all the subdirectories file names (sampled time steps)

    print('\nProcessing scatter data from case: %s \n' % case_path)

    mypath = case_path+'/postProcessing/preview/'

    timeDict = os.listdir(mypath)
    timeDict = [t for t in timeDict if t[-4]!='.']


    nSets = len(timeDict)
    # noch automatisieren
    nPoints = 22000  # testen ob das geht
    nEntries = nPoints * nSets

    location_dict = ['010', '050', '100', '120', '150', '200', '300']
    nLocation = np.linspace(0, len(location_dict) - 1, len(location_dict))

    # # Four axes, returned as a 2-d array
    # f, axarr = plt.subplots(4, 2)
    # isodd = lambda x: 1 if x % 2 != 0 else 0

    # loop over the different planes normal to x-axis
    for n in range(0, len(nLocation)):
        print('Processing scatter data from position x/D = ' + location_dict[n])

        arrayT = np.zeros((nEntries))  # 1
        arrayPV = np.zeros((nEntries))  # 2
        arrayf = np.zeros((nEntries))  # 3
        arrayCH4 = np.zeros((nEntries))  # 4
        arrayCO2 = np.zeros((nEntries))  # 5
        arrayH2O = np.zeros((nEntries))  # 6
        arrayO2 = np.zeros((nEntries))  # 7
        arrayCO = np.zeros((nEntries))  # 8
        arrayH2 = np.zeros((nEntries))  # 9
        arrayRadius = np.zeros((nEntries))  # 10
        # can be continued

        counterArray = np.zeros(9).astype(int)  # adjust number to number of arrays

        # loop over the data sets
        for i in range(0, nSets):

            try:
                fScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/f_Bilger_scatter_xD' + location_dict[n] + '.raw')
                # 4th column is actual data, [:,0:2] is position data
                length = len(fScatter)
                arrayf[counterArray[0]:(counterArray[0] + length)] = fScatter[:, 3]

                # compute the radial position of the sample
                y = fScatter[:, 1]
                z = fScatter[:, 2]
                arrayRadius[counterArray[0]:(counterArray[0] + length)] = np.sqrt(y ** 2 + z ** 2)

                counterArray[0] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of f scatter data! For: i= ' + str(i) + ' and n = ' + str(n))

            try:
                TScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/T_scatter_xD' + location_dict[n] + '.raw')
                length = len(TScatter)
                arrayT[counterArray[1]:(counterArray[1] + length)] = TScatter[:, 3]
                counterArray[1] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of T scatter data!')

            # try:
            #     PVScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/PV_scatter_xD' + location_dict[n] + '.raw')
            #     length = len(PVScatter)
            #     arrayPV[counterArray[2]:(counterArray[2] + length)] = PVScatter[:, 3]
            #     counterArray[2] += length
            # except KeyboardInterrupt:
            #     break
            # except:
            #     print('Check the file name and/or path of PV scatter data!')

            try:
                CH4Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CH4_scatter_xD' + location_dict[n] + '.raw')
                length = len(CH4Scatter)
                arrayCH4[counterArray[3]:(counterArray[3] + length)] = CH4Scatter[:, 3]
                counterArray[3] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CH4 scatter data!')

            try:
                CO2Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CO2_scatter_xD' + location_dict[n] + '.raw')
                length = len(CO2Scatter)
                arrayCO2[counterArray[4]:(counterArray[4] + length)] = CO2Scatter[:, 3]
                counterArray[4] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CO2 scatter data!')

            try:
                H2OScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/H2O_scatter_xD' + location_dict[n] + '.raw')
                length = len(H2OScatter)
                arrayH2O[counterArray[5]:(counterArray[5] + length)] = H2OScatter[:, 3]
                counterArray[5] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of H2O scatter data!')

            try:
                COScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CO_scatter_xD' + location_dict[n] + '.raw')
                length = len(COScatter)
                arrayCO[counterArray[6]:(counterArray[6] + length)] = COScatter[:, 3]
                counterArray[6] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CO scatter data!')

            try:
                O2Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/O2_scatter_xD' + location_dict[n] + '.raw')
                length = len(O2Scatter)
                arrayO2[counterArray[7]:(counterArray[7] + length)] = O2Scatter[:, 3]
                counterArray[7] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of O2 scatter data!')

            try:
                H2Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/H2_scatter_xD' + location_dict[n] + '.raw')
                length = len(H2Scatter)
                arrayH2[counterArray[8]:(counterArray[8] + length)] = H2Scatter[:, 3]
                counterArray[8] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of H2 scatter data!')

        # end loop

        # compose the output array
        Output_np = np.array((arrayRadius,  arrayf, arrayT, arrayCH4, arrayH2O, arrayCO2, arrayO2, arrayCO, arrayH2))

        Output_df = pd.DataFrame(Output_np)
        Output_df = Output_df.T
        Output_df.columns = ['r[m]', 'Z', 'T', 'Y_CH4', 'Y_H2O', 'Y_CO2', 'Y_O2', 'Y_CO', 'Y_H2']

        # skip all data where T is < 300.5
        print('Keep only the data points where T > 300.01 K')
        Output_df = Output_df[Output_df['T'] > 300.01]
        Output_df = Output_df.sample(nr_samples)

        store_path = case_path+'/postProcessing/scatter/'

        # create directory if it doesn't exist
        if os.path.isdir(store_path) is False:
            os.mkdir(store_path)
        output_name = store_path + '/scatter_xD' + location_dict[n] + '_TNF14.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')








