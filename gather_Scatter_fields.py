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
import matplotlib.pyplot as plt

try:
    from matplotlib2tikz import save as tikz_save
except:
    print('Install matplotlib2tikz: pip3 install matplotlib2tikz')

mypath = input('Where is the scatter data?, (e.g. preview) type in: ')

storePath = input('Where do you want to save the data?, (e.g. ../scatter) type in: ')
# alternatively you just provide the path hard coded

# get all the subdirectories file names (sampled time steps)
timeDict=os.listdir(mypath)
timeDict.sort()

#nSets = len(timeDict)
nSets = 1
# noch automatisieren
nPoints = 22200 #testen ob das geht
nEntries = nPoints*nSets

location_dict =['010','050','100','120','150','200','300']
nLocation = np.linspace(0,len(location_dict)-1,len(location_dict))

# Four axes, returned as a 2-d array
f, axarr = plt.subplots(4, 2)
isodd = lambda x: 1 if x %2 != 0 else 0

# loop over the different planes normal to x-axis
for n in range(0, len(nLocation)):
    print('Processing scatter data from position x/D = ' + location_dict[n])

    arrayT = np.zeros((nEntries,8))               # 1
    arrayPV = np.zeros((nEntries,1))                # 2
    arrayf = np.zeros((nEntries,1))                 # 3
    arrayCH4 = np.zeros((nEntries,8))             # 4
    arrayCO2 = np.zeros((nEntries,8))             # 5
    arrayH2O = np.zeros((nEntries,8))             # 6
    arrayO2 = np.zeros((nEntries,8))              # 7
    arrayCO = np.zeros((nEntries,8))              # 8
    arrayRadius = np.zeros((nEntries,1))          # 9
    # can be continued

    counterArray = np.zeros(8).astype(int)      # adjust number to number of arrays

    # loop over the data sets
    for i in range(0,nSets):

        print('\n Time step number: '+timeDict[i])

        try:
            fScatter = np.loadtxt(mypath+'/'+timeDict[i]+'/f_Bilger_scatter_xD'+location_dict[n]+'.raw')
            # 4th column is actual data, [:,0:2] is position data
            length = len(fScatter)
            arrayf[counterArray[0]:(counterArray[0] + length),0] = fScatter[:, 3]

            # compute the radial position of the sample
            y = fScatter[:,1]
            z = fScatter[:,2]
            arrayRadius[counterArray[0]:(counterArray[0] + length),0] = np.sqrt(y**2 + z**2)

            counterArray[0] += length
        except KeyboardInterrupt:
            break
        except:
            print('Check the file name and/or path of f scatter data! For: i= '+str(i)+' and n = '+str(n))

        try:
            PVScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/PV_scatter_xD' + location_dict[n] + '.raw')
            length = len(PVScatter)
            arrayPV[counterArray[1]:(counterArray[1] + length),0] = PVScatter[:, 3]
            counterArray[1] += length
        except KeyboardInterrupt:
            break
        except:
            print('Check the file name and/or path of PV scatter data!')

        ##################################
        # loop over all the single fields
        ##################################

        for f in range(0,8):
            #print('\n Field number: '+str(f+1))
            try:
                TScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/T_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(TScatter)
                arrayT[counterArray[2]:(counterArray[2] + length),f] = TScatter[:, 3]
                if f==0:
                    counterArray[2] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of T scatter data!')

            try:
                CH4Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CH4_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(CH4Scatter)
                arrayCH4[counterArray[3]:(counterArray[3] + length),f] = CH4Scatter[:, 3]
                if f == 0:
                    counterArray[3] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CH4 scatter data!')

            try:
                CO2Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CO2_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(CO2Scatter)
                arrayCO2[counterArray[4]:(counterArray[4] + length),f] = CO2Scatter[:, 3]
                if f == 0:
                    counterArray[4] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CO2 scatter data!')

            try:
                H2OScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/H2O_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(H2OScatter)
                arrayH2O[counterArray[5]:(counterArray[5] + length),f] = H2OScatter[:, 3]
                if f == 0:
                    counterArray[5] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of H2O scatter data!')

            try:
                COScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/CO_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(COScatter)
                arrayCO[counterArray[5]:(counterArray[5] + length),f] = COScatter[:, 3]
                if f == 0:
                    counterArray[5] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of CO scatter data!')

            try:
                O2Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/O2_'+str(f+1)+'_scatter_xD' + location_dict[n] + '.raw')
                length = len(O2Scatter)
                arrayO2[counterArray[6]:(counterArray[6] + length),f] = O2Scatter[:, 3]
                if f == 0:
                    counterArray[6] += length
            except KeyboardInterrupt:
                break
            except:
                print('Check the file name and/or path of O2 scatter data!')

    #end loop

    # compose the output array
    Output_np = np.concatenate((arrayRadius, arrayT,arrayf, arrayPV, arrayCH4, arrayCO2, arrayO2, arrayH2O, arrayCO),axis=1)

    Output_df = pd.DataFrame(Output_np)
   # Output_df = Output_df.T
    Output_df.columns = ['radius', 'f_Bilger', 'PV', 'T_1', 'T_2','T_3','T_4','T_5','T_6','T_7','T_8',
                         'CH4_1', 'CH4_2','CH4_3','CH4_4','CH4_5','CH4_6','CH4_7','CH4_8',
                         'CO2_1', 'CO2_2','CO2_3','CO2_4','CO2_5','CO2_6','CO2_7','CO2_8',
                          'O2_1', 'O2_2','O2_3','O2_4','O2_5','O2_6','O2_7','O2_8',
                          'H2O_1', 'H2O_2','H2O_3','H2O_4','H2O_5','H2O_6','H2O_7','H2O_8',
                         'CO_1', 'CO_2', 'CO_3', 'CO_4', 'CO_5', 'CO_6', 'CO_7', 'CO_8']

    # skip all data where T is < 300.5
    #print('Keep only the data points where T > 300.5 K')
    #Output_df = Output_df[Output_df['T'] > 300.5]

    output_name = storePath+'/scatter_xD' + location_dict[n] + '.txt'
    pd.DataFrame.to_csv(Output_df,output_name,index=False,sep='\t')


location = 6
for i in range(1,60,5):
    for f in range(1, 5):
        fScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/f_Bilger_scatter_xD' + location_dict[location] + '.raw')
        Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/T_' + str(f) + '_scatter_xD' + location_dict[location] + '.raw')
        plt.scatter(fScatter[:, 3], Scatter[:, 3], s=0.3, c='r')


for i in range(1,60,5):
    fScatter = np.loadtxt(mypath + '/' + timeDict[i] + '/f_Bilger_scatter_xD' + location_dict[location] + '.raw')
    Scatter = np.loadtxt(mypath + '/' + timeDict[i] + '/T_scatter_xD' + location_dict[location] + '.raw')
    plt.scatter(fScatter[:, 3], Scatter[:, 3], s=0.3, c='b')

plt.plot(flamelet['Z'],flamelet['temperature'],'k',lw=0.9)
plt.ylabel('T [K]')
plt.xlabel('f_Bilger')
plt.xlim([0, 0.3])
plt.title('x/D = '+location_dict[location])

plt.show()









