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

time = input('Which time step you choose for sampling (usually latest):  ')

scalarTail = '_fMean_TMean.xy'

#speciesTail = '_N2Mean_N2Prime2Mean_O2Mean_O2Prime2Mean_CH4Mean_CH4Prime2Mean_H2OMean_H2OPrime2Mean_CO2Mean_CO2Prime2Mean_H2Mean_H2Prime2Mean_COMean_COPrime2Mean.xy'

# initialize arrays
datapoints = 200
noFiles = 40

#represents the different locations you defined in the sample dict file
nLocation = [0,1,2,3,4,5,6]
location_dict =['010','050','100','120','150','200','300']

for n in range(0, len(nLocation)):
    arrayT = np.zeros((datapoints))

    arrayf = np.zeros((datapoints))




    # to be continued for further species... and RMS!
    # important here you have to check if the data Name is correct!
    # this is for the species field values!
    # here it is looping over the different radial positions

    for j in range(0, noFiles):
        try:
            dataScalar = np.loadtxt('postProcessing/sampleDict/'+time+'/line_x' + str(nLocation[n])+'-r'+str(j)+scalarTail)
        except:
            print('Check the file name and/or path of scalar fields! Something is wrong')

        # there is the position of the T column in your data set;
        # check for consistency! they are summed up for different j
        arrayf += dataScalar[:, 3]

        arrayT += dataScalar[:, 4]


        if j == 0:
            arrayYPos = dataScalar[:,1]* 1000       # m to mm
            arrayZPos = dataScalar[:,2]* 1000       # m to mm
            arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)
            print(arrayYPos)

        # try:
        #     dataU = np.loadtxt('postProcessing/sampleDict/'+time+'/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UMean.xy')
        # except:
        #     print('Check the file name of U! Something is wrong')

        winkel = 2 * j / noFiles * 3.14

        # arrayU += dataU[:,3]
        # arrayV += np.sin(winkel) * dataU[:,4] + np.cos(winkel) * dataU[:,5]
        # arrayW += np.cos(winkel) * dataU[:,4] + np.sin(winkel) * dataU[:,5]

        # # RMS
        # try:
        #     dataURMS = np.loadtxt('postProcessing/sampleDict/'+time+'/line_x' + str(nLocation[n]) + '-r' + str(j) + '_UPrime2Mean.xy')
        # except:
        #     print('Check the file name of U! Something is wrong')

        # winkel = 2 * j / noFiles * 3.14
        #
        # arrayURMS += dataURMS[:,3]
        # arrayVRMS += np.sin(winkel) * dataURMS[:,4] + np.cos(winkel) * dataURMS[:,5]
        # arrayWRMS += np.cos(winkel) * dataURMS[:,4] + np.sin(winkel) * dataURMS[:,5]

        # # Species
        # try:
        #     dataSpecies = np.loadtxt('sampleDict/'+time+'/line_x'+str(nLocation[n])+'-r'+str(j)+'_Species')
        # except:
        #     print('Check the file name of your species data! Something is wrong')
        #
        #
        # arrayO2 += dataSpecies[:,5]
        # arrayCH4 += dataSpecies[:,7]
        # arrayH2O += dataSpecies[:,9]
        # arrayCO2 += dataSpecies[:,11]
        # arrayH2 += dataSpecies[:,13]

        # loop 2 end

    # set up to write the output file!
    Output_np = np.array((arrayDist, arrayf, arrayT))

    # Divide by the number of files and transpose
    Output_T = Output_np.T
    Output_T = Output_T/noFiles
    # set up dataframe to write as CSV
    Output_df = pd.DataFrame(Output_T)

    # Name correctly the output columns
    Output_df.columns = ['x_Pos', 'f', 'T']
    Output_df['x_Pos'] = arrayDist

    #write one output file for each position
    output_name = 'postProcessing/sampleDict/'+'line_xD' + location_dict[n] + '.txt'
    pd.DataFrame.to_csv(Output_df,output_name,index=False,sep='\t')

    # plot the radial temperature profiles
    plt.figure(n+1)
    plt.plot(Output_df['x_Pos'],Output_df['T'])
    plt.ylabel('Temperature')
    plt.xlabel('radial Position')
    plt.title('Mean temperature plot at: x/D=' + str(int(location_dict[n]) / 10))
    plt.ylim([250,2300])

    # loop end
plt.show(block=False)
#plt.close()





