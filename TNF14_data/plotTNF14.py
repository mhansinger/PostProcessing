'''
This is to plot and compare different simulation and experimental results from the TNF data.
Both Radial Mean as Scatter

@author: mhansinger
'''

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


##############################
# HERE YOU HAVE to SPECIFY THE CASE DIRECTORIES

# specify the paths to the simulation data
# ubulk57
case_13_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-13_inert_LES_cold'
case_12_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot'
case_05_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05'
case_19_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-19_kEq_57_ESF'

#DNS
case_11_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-11_inert_DNS'

# ubulk80
case_20_path_inert='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-20_inert_LES_hot_80'
case_21_path_inert='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-21_inert_LES_cold_80'
case_20_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-20_kEq_80_ESF'

case_22_lam_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-22_Lr75-80_lam'

##############################
# single file names
# for scatter
planes = ['line_xD010_TNF14.txt','line_xD050_TNF14.txt','line_xD100_TNF14.txt','line_xD120_TNF14.txt',
          'line_xD150_TNF14.txt','line_xD200_TNF14.txt','line_xD300_TNF14.txt']

# for mean values
radial_names_end = ['radial_xD010.dat','radial_xD050.dat','radial_xD100.dat',
                    'radial_xD120.dat','radial_xD150.dat','radial_xD200.dat','radial_xD300.dat']

location_dict = ['010','050','100','120','150','200','300']

postProc='postProcessing/sampleDict'

##############################
# Experimental data is:
# scatter

Exp_scatter = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species-5GP'
Exp_mean = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species_Mean_RMS-5GP/Radial_Favre'

# read in all the Experimental mean data
expfiles = os.listdir(Exp_mean)

ExpData_57 = {}
ExpData_80 = {}
# read in the data
for file in expfiles:
    if file.endswith(".csv") and 'Lr75-57' in file:
        print('Reading in data from: '+file)
        df = pd.read_csv(Exp_mean+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpData_57[name] = df
    if file.endswith(".csv") and 'Lr75-80' in file:
        print('Reading in data from: '+file)
        df = pd.read_csv(Exp_mean+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpData_80[name] = df


ExpNames_57 = list(ExpData_57.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames_57]
ExpNames_57 = [x for _, x in sorted(zip(exp_order, ExpNames_57))]

ExpNames_80 = list(ExpData_80.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames_80]
ExpNames_80 = [x for _, x in sorted(zip(exp_order, ExpNames_80))]

print('\nsorted!')

# reads in the velocity data
Exp_Velocity = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Pilot_Only_Velocity-5GP'

velocity_files = os.listdir(Exp_Velocity)

ExpVel_57 = {}
ExpVel_80 = {}
# read in the data
for file in velocity_files:
    if file.endswith(".csv") and 'Lr75-57' in file:
        print('Reading in Velocity data from: '+file)
        df = pd.read_csv(Exp_Velocity+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpData_57[name] = df
    if file.endswith(".csv") and 'Lr75-80' in file:
        print('Reading in Velocity data from: '+file)
        df = pd.read_csv(Exp_Velocity+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpData_80[name] = df


# NOT FINISHED!

#####################################
# plots
#####################################

def plotRadial_reactive(species='Z', case=80,laminar=True,factor=1000):
    plt.close('all')

    LESdata = {}

    try:
        case=int(case)
    except:
        print('')

    # get the files path

    if case == 80:
        if laminar:
            mypath = os.path.join(case_22_lam_path, postProc)
        else:
            mypath = os.path.join(case_20_path, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif case == 57:
        mypath = os.path.join(case_19_path, postProc)
        ExpData = ExpData_57
        ExpNames = ExpNames_57

    files = os.listdir(mypath)

    # read in the files
    for file in files:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata[name] = df

    radialAv = list(LESdata.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv = [x for _, x in sorted(zip(file_order, radialAv))]
    print('\nsorted!')
    print(radialAv)

    if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
        speciesEmean = species
        speciesErms = species+'_rms'
        species = 'Y_'+species
    else:
        speciesEmean = species+'_mean'
        speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv)):
        plt.figure(i+1)
        thisData = LESdata[radialAv[i]]
        thisExp = ExpData[ExpNames[i]]

        # LES data
        plt.plot(thisData['r[m]']*factor, thisData[species+'_mean'],'r', lw=1.6)
        #thisData['r[m]'].max()
        #try:
        #    if species == 'f_Bilger':
        plt.plot(thisData['r[m]']*factor, thisData[species + '_rms'], 'r', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at Plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius [mm]')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'.png'
        plt.savefig(fig_name)


    plt.show(block=False)

# function to plot the velocity data
def plot_velocity(case=57,factor=1000):
    plt.close('all')

    LESdata = {}

    try:
        case=int(case)
    except:
        print('')

    # get the files path

    if case == 80:
        if laminar:
            mypath = os.path.join(case_22_lam_path, postProc)
        else:
            mypath = os.path.join(case_20_path, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif case == 57:
        mypath = os.path.join(case_19_path, postProc)
        ExpData = ExpData_80
        ExpNames = ExpNames_80

    files = os.listdir(mypath)
