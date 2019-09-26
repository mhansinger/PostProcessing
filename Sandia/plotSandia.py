'''
This is to plot and compare different simulation and experimental results from the TNF data.
Both Radial Mean as Scatter

@author: mhansinger
'''

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from os.path import join

##############################
# HERE YOU HAVE to SPECIFY THE CASE DIRECTORIES


##############################
# single file names
# for scatter
planes = ['line_xD7.5_Sandia.txt','line_xD15_Sandia.txt','line_xD30_Sandia.txt','line_xD45_Sandia.txt',
          'line_xD60_Sandia.txt']

# for mean values
radial_names_end = ['radial_xD010.dat','radial_xD050.dat','radial_xD100.dat',
                    'radial_xD120.dat','radial_xD150.dat','radial_xD200.dat','radial_xD300.dat']

location_dict = ['7.5','15','30','45','60']

# Diameter
Diameter = 0.0072 # [m]

postProc='postProcessing/sampleDict'

##############################
# Experimental data is:
# scatter

#Exp_scatter = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species-5GP'
Exp_mean = '/home/max/Documents/10_Experimental_Data/Sandia_Flames/pmCDEFarchives' #'/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species_Mean_RMS-5GP/Radial_Favre'

# read in all the Experimental mean data
expfiles_D = os.listdir(join(Exp_mean,'pmD.stat'))
expfiles_E = os.listdir(join(Exp_mean,'pmE.stat'))
expfiles_F = os.listdir(join(Exp_mean,'pmF.stat'))

ExpData_D = {}
ExpData_E = {}
ExpData_F = {}
# read in the data
for file in expfiles_D:
    if file != "DCL.Yave" and file.endswith(".Yave"):
        print('Reading in data from: '+file)
        df = pd.read_csv(join(Exp_mean,'pmD.stat')+'/'+file, sep='\t',header=3)
        print(df.head())
        # generate file name
        name = file[0:-5]
        ExpData_D[name] = df

for file in expfiles_E:
    if file != "ECL.Yave" and file.endswith(".Yave"):
        print('Reading in data from: '+file)
        df = pd.read_csv(join(Exp_mean,'pmE.stat')+'/'+file, sep='\t',header=3)
        # generate file name
        name = file[0:-5]
        ExpData_E[name] = df

for file in expfiles_F:
    if file != "FCL.Yave" and file.endswith(".Yave") :
        print('Reading in data from: '+file)
        df = pd.read_csv(join(Exp_mean,'pmF.stat')+'/'+file, sep='\t',header=3)
        # generate file name
        name = file[0:-5]
        ExpData_F[name] = df


ExpNames_D = list(ExpData_D.keys())
# get the order of the files from the file ending
exp_order_D =[]
for id, f in enumerate(ExpNames_D):
    if f== 'D075':
        exp_order_D.append(7.5)
    else:
        exp_order_D.append(float(f[1:]))
        print(f[1:])

ExpNames_D = [x for _, x in sorted(zip(exp_order_D, ExpNames_D))]


ExpNames_E = list(ExpData_E.keys())
# get the order of the files from the file ending
exp_order_E =[]
for id, f in enumerate(ExpNames_E):
    if f== 'E075':
        exp_order_E.append(7.5)
    else:
        exp_order_E.append(float(f[1:]))
ExpNames_E = [x for _, x in sorted(zip(exp_order_E, ExpNames_E))]


ExpNames_F = list(ExpData_F.keys())
# get the order of the files from the file ending
exp_order_F=[]
for id, f in enumerate(ExpNames_F):
    if f== 'F075':
        exp_order_F.append(7.5)
    else:
        exp_order_F.append(float(f[1:]))
ExpNames_F = [x for _, x in sorted(zip(exp_order_F, ExpNames_F))]

print('\nsorted!')

# NOT FINISHED!

#####################################
# plots
#####################################

def plotRadial_reactive(species='F', case='D', factor=1000):
    plt.close('all')

    myPath = postProc
    LESdata = {}

    # get the files path

    if case == 'D':
        ExpData = ExpData_D
        ExpNames = ExpNames_D

    elif case == 'E':
        ExpData = ExpData_E
        ExpNames = ExpNames_E

    elif case == 'F':
        ExpData = ExpData_F
        ExpNames = ExpNames_F

    files = os.listdir(myPath)

    # read in the files
    for file in files:
        if file.endswith("Sandia.txt") and file != 'line_xD05_Sandia.txt':  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(myPath + '/' + file, sep='\t')
            # generate file name
            name = file[0:-11]
            print(name)
            LESdata[name] = df

    radialAv = list(LESdata.keys())
    # get the order of the files
    #print(radialAv)
    file_order = [float(re.search('line_xD(.*)',f).group(1)) for f in radialAv]

    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv = [x for _, x in sorted(zip(file_order, radialAv))]
    file_order = [float(re.search('line_xD(.*)',f).group(1)) for f in radialAv]
    print('\nsorted!')
    #print(radialAv)
    #print('file_order',file_order)

    if any(species == f for f in ['CH4','O2','H2O','CO2','CO','H2']):
        speciesEmean = 'Y'+species
        speciesErms = 'Y'+species+'rms'
        species = 'Y'+species
    elif species == 'F':
        speciesEmean = species
        speciesErms = species+'rms'
    elif species == 'F_Sandia':
        speciesEmean = 'F'
        speciesErms = 'Frms'
    elif species == 'T':
        speciesEmean = 'T(K)'
        speciesErms = 'Trms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv)):
        plt.figure(i+1)

        # assign the experimental data
        if case == 'D':
            thisExp = ExpData_D[ExpNames_D[i]]
            print(ExpNames_D[i])
        elif case == 'E':
            thisExp = ExpData_E[ExpNames_E[i+3]]
            print(ExpNames_E[i+3])
        elif case == 'F':
            thisExp = ExpData_F[ExpNames_F[i+3]]
            print(ExpNames_F[i+3])

        # print(radialAv)
        # print(thisExp)

        thisData = LESdata[radialAv[i]]

        #print(thisExp.head())

        thisExp['r'] = thisExp['r/d'] * Diameter
        thisData['r/d'] = thisData['r_in_m'] / Diameter

        # LES data
        plt.plot(thisData['r/d'], thisData[species],'r', lw=1.6)
        plt.plot(thisData['r/d'], thisData[species + 'rms'], 'r', lw=1.6)

        plt.plot(thisExp['r/d'], thisExp[speciesEmean], 'bo', lw=1)
        plt.plot(thisExp['r/d'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 5])
        plt.title(species+' at Plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius r/d')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'_Sanida_%s.png' % case
        plt.savefig(fig_name)
    plt.show(block=False)

