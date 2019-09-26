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
import matplotlib.pyplot as plt
import os

scalarTail='_f_BilgerMean_f_BilgerPrime2Mean.xy'

# initialize arrays
datapoints = 200
noFiles = 40

#represents the different locations you defined in the sample dict file
nLocation = [0,1]
location_dict =['-1','0']

root = os.getcwd()

pipes = os.listdir(root)
pipes = [f for f in pipes if os.path.isdir(root) and f[:4] == 'pipe']


for p in pipes:
    # get the latest time step from every simulation
    thisPath = os.path.join(root,p,'postProcessing','sampleDict')
    times = os.listdir(thisPath)
    # remove all entries which are not time steps!
    times = [t for t in times if os.path.isdir(thisPath+'/'+t)]
    times.sort()
    latestTime = times[-1]
    print(times)

    print('Processing: ',p)
    print('')

    for n in range(0, len(nLocation)):
        arrayT = np.zeros((datapoints))
        arrayTRMS = np.zeros((datapoints))
        arrayf = np.zeros((datapoints))
        arrayfRMS = np.zeros((datapoints))

        arrayU = np.zeros((datapoints))
        arrayURMS = np.zeros((datapoints))
        arrayV = np.zeros((datapoints))
        arrayVRMS = np.zeros((datapoints))
        arrayW = np.zeros((datapoints))
        arrayWRMS = np.zeros((datapoints))

        # Koordinate Position
        arrayYPos = np.zeros((datapoints))
        arrayZPos = np.zeros((datapoints))
        arrayDist = np.zeros((datapoints))

        # to be continued for further species... and RMS!
        # important here you have to check if the data Name is correct!
        # this is for the species field values!
        # here it is looping over the different radial positions

        for j in range(0, noFiles):
            try:
                dataScalar = np.loadtxt(thisPath+'/' + latestTime + '/line_x' + str(nLocation[n]) + '-r' + str(j) + scalarTail)
            except:
                print('Check the file name and/or path of scalar fields! Something is wrong in:', thisPath)
                break

            arrayf[:len(dataScalar)] += dataScalar[:,3]   # there is the position of the
                                        # f_Bilger column in your data set; check for consistency! they are summed up for different j
            arrayfRMS[:len(dataScalar)] += np.sqrt(dataScalar[:, 4])

            if j == 0:
                arrayYPos[:len(dataScalar)] = dataScalar[:, 1]
                arrayZPos[:len(dataScalar)] = dataScalar[:, 2]
                arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos) * 1000

            try:
                dataU = np.loadtxt(thisPath+'/' + latestTime + '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UMean.xy')
            except:
                print('Check the file name of U! Something is wrong')

            winkel = 2 * j / noFiles * 3.14

            arrayU[:len(dataU)] += dataU[:, 3]
            arrayV[:len(dataU)] += np.sin(winkel) * dataU[:, 4] + np.cos(winkel) * dataU[:, 5]
            arrayW[:len(dataU)] += np.cos(winkel) * dataU[:, 4] + np.sin(winkel) * dataU[:, 5]

            # RMS
            try:
                dataURMS = np.loadtxt(thisPath+'/' + latestTime + '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')
            except:
                print('Check the file name of U! Something is wrong')

            winkel = 2 * j / noFiles * 3.14

            arrayURMS[:len(dataURMS)] += dataURMS[:, 3]
            arrayVRMS[:len(dataURMS)] += np.sin(winkel) * dataURMS[:, 4] + np.cos(winkel) * dataURMS[:, 5]
            arrayWRMS[:len(dataURMS)] += np.cos(winkel) * dataURMS[:, 4] + np.sin(winkel) * dataURMS[:, 5]

            # # Species
            # try:
            #     dataSpecies = np.loadtxt(thisPath+'/' + latestTime + '/line_x' + str(nLocation[n]) + '-r' + str(j) + '_Species')
            # except:
            #     print('Check the file name of your species data! Something is wrong')
            #
            # arrayN2 += dataSpecies[:, 3]
            # arrayO2 += dataSpecies[:, 5]
            # arrayCH4 += dataSpecies[:, 7]
            # arrayH2O += dataSpecies[:, 9]
            # arrayCO2 += dataSpecies[:, 11]
            # arrayH2 += dataSpecies[:, 13]

            # loop 2 end

        # set up to write the output file!
        Output_np = np.array((arrayDist, arrayf,  arrayU, arrayV, arrayW, arrayfRMS,  arrayURMS, arrayVRMS, arrayWRMS))

        # Divide by the number of files and transpose
        Output_T = Output_np.T
        Output_T = Output_T / noFiles
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['x_Pos', 'f',  'U', 'V', 'W', 'fRMS', 'URMS', 'VRMS', 'WRMS']

        # write one output file for each position

        output_name = os.path.join(thisPath,'line_xD'+ location_dict[n]+'.txt')
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')

        # plot the data
        if n==0:
            plt.figure(1)
            plt.plot(Output_df[Output_df['f']>0.01]['x_Pos'], Output_df[Output_df['f']>0.01]['f'])
            #plt.plot(Output_df[Output_df['f']>0.01]['x_Pos'], Output_df[Output_df['f']>0.01]['fRMS'], '--')
            # plt.legend(['f_mean_' + str(p), 'f_RMS_' + str(p)])

            plt.figure(2)
            plt.plot(Output_df[Output_df['U']>40]['x_Pos'], Output_df[Output_df['U']>40]['U'])
            #plt.plot(Output_df[Output_df['U']>40]['x_Pos'], Output_df[Output_df['U']>40]['URMS'], '--')
            #plt.legend(['f_mean_' + str(p), 'f_RMS_' + str(p)])


# loop end
plt.figure(1)
plt.title('Compare inflows: f_Bilger mean')
plt.xlabel('r in [mm]')
plt.ylabel('f')
plt.figure(2)
plt.xlabel('r in [mm]')
plt.ylabel('U in [m/s]')
plt.title('Compare inflows: U mean')
plt.show(block=False)
#plt.close()





