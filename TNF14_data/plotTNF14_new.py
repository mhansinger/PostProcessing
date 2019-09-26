'''
This is to plot and compare different simulation and experimental results from the TNF data.
Both Radial Mean as Scatter

@author: mhansinger

# last change: 3.1.19
'''

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import re


##############################
# HERE YOU HAVE to SPECIFY THE CASE DIRECTORIES

# specify the paths to the simulation data
# ubulk57
path_dict = {
'case_13_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-13_inert_LES_cold',

'case_05_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05',
'case_19_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-19_kEq_57_ESF',
'case_05_lowMa_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05_lam_lowMa',
'case_19_lowMa_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-19_kEqn_57_lam_lowMa',
'case_05_lowT_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05_lowT_lam',
'case_05_4Ord_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05_lam_lowMa_4Ord',
'case_27_lowMa_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-27_57_2.8Mio_WALE_lam',
'case_41_lam_1Mio_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-41_react_lamChem_WALE_1Mio',
'case_43_ESF_2.8Mio_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-43_ESF_WALE_2.8Mio',
'case_42_SuperMuc_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-42_react_ESF_WALE_1Mio',
    'case_42_Cluster_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-43_ESF_WALE_2.8Mio',
'case_44_lam_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-44_react_lam_WALE',
'case_27_lam_linear_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-27_lam_WALE_2.8Mio_linear',
    'case_43_ESF_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-43_ESF_WALE_2.8Mio',
'case_27_NOLOWMA_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-27_lam_WALE_2.8Mio_linear_NOLOWMA2',


#FPV
'case_FPV_reduced_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/ANN_cases/TNF_FPV_reduced',
'case_FPV_ANN_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/ANN_cases/Lr75-57_FPVANN_premix',

# inert cases
'case_12_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot',
'case_12_Pr0.2_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot_Pr0.2',

'case_12_2.8Mio_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot_2.8Mio',
'case_12_2.8Mio_2_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot_2.8Mio_2',
'case_12_1Mio_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12-inert_LES_hot_1Mio',
'case_12_1Mio_Pr0.2_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12-inert_LES_hot_1Mio_Pr0.2',
'case_12_550k_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_hot_550k_Pr0.2',


#qDNS
'case_DNS_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-16_inert_DNS',
# ubulk80
'case_20_path_inert':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-20_inert_LES_hot_80',
'case_21_path_inert':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-21_inert_LES_cold_80',
'case_20_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-20_kEq_80_ESF',
'case_22_lam_path':'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-22_Lr75-80_lam',
'case_12_4Ord_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot_4Order',
'case_17_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-17_inert_kEqn_hot',


#Numerik Vergleich
'case_111_linear_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Vergleich_Numerik/case-111_linear_2.8Mio',
'case_222_cubic_path':'/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Vergleich_Numerik/case-222_cubic_2.8Mio',

# dummy
'this_path':'./'

}

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

Exp_scatter = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/species-5GP-2015' #'/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species-5GP'
Exp_mean = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Species_Mean_RMS-5GP_2015/Radial_Reynolds'

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

def plotRadial_reactive(case,species='Z',velocity=57,laminar=True,factor=1000):
    plt.close('all')

    LESdata = {}

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    if velocity == 80:
        if laminar:
            mypath = os.path.join(case, postProc)
        else:
            mypath = os.path.join(case, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath = os.path.join(case, postProc)
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
        plt.plot(thisData['r_in_m']*factor, thisData[species+'_mean'],'r', lw=1.6)
        #thisData['r_in_m'].max()
        #try:
        #    if species == 'f_Bilger':
        plt.plot(thisData['r_in_m']*factor, thisData[species + '_rms'], 'r', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius [mm]')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'.png'
        plt.savefig(fig_name)

    plt.show(block=False)




########################################
#compare two cases
########################################
def plotRadial_reactive_compare(case1,case2, species='Z', velocity=57,laminar=True,factor=1000):
    plt.close('all')

    LESdata1 = {}
    LESdata2 = {}

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    if velocity == 80:
        if laminar:
            mypath1 = os.path.join(case1, postProc)
            mypath2 = os.path.join(case2, postProc)
        else:
            mypath1 = os.path.join(case1, postProc)
            mypath2 = os.path.join(case2, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath1 = os.path.join(case1, postProc)
        mypath2 = os.path.join(case2, postProc)
        ExpData = ExpData_57
        ExpNames = ExpNames_57

    files1 = os.listdir(mypath1)
    files2 = os.listdir(mypath2)

    # read in the files
    for file in files1:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath1 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata1[name] = df

    # read in the files
    for file in files2:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath2 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata2[name] = df

    radialAv1 = list(LESdata1.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv1 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv1)

    radialAv2 = list(LESdata2.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv2 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv2)

    if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
        speciesEmean = species
        speciesErms = species+'_rms'
        species = 'Y_'+species
    else:
        speciesEmean = species+'_mean'
        speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv1)):
        plt.figure(i+1)
        thisData1 = LESdata1[radialAv1[i]]
        thisData2 = LESdata2[radialAv2[i]]
        thisExp = ExpData[ExpNames[i]]

        # LES data case1
        plt.plot(thisData1['r_in_m']*factor, thisData1[species+'_mean'],'r', lw=1.6)
        plt.plot(thisData1['r_in_m']*factor, thisData1[species + '_rms'], 'r--', lw=1.6)

        # LES data case2
        plt.plot(thisData2['r_in_m'] * factor, thisData2[species + '_mean'], 'k', lw=1.6)
        plt.plot(thisData2['r_in_m'] * factor, thisData2[species + '_rms'], 'k--', lw=1.6)

        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius [mm]')
        #plt.legend(['Case1 mean','Case1 RMS','Case2 mean','Case2 RMS','Exp. mean','Exp RMS'])
        plt.legend([case1.split('_')[-2:], 'RMS', case2.split('_')[-2:], 'RMS', 'Exp. mean', 'Exp RMS'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'_compare.png'
        plt.savefig(fig_name)

    plt.show(block=False)

# compare inert cases

def plotRadial_inert_compare(case1,case2,species='Z',velocity=57,factor=1000):
    plt.close('all')

    LESdata1 = {}
    LESdata2 = {}

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    if velocity == 80:
        #if laminar:
        mypath1 = os.path.join(case1, postProc)
        mypath2 = os.path.join(case2, postProc)
        #else:
        #    mypath1 = os.path.join(case1, postProc)
        #    mypath2 = os.path.join(case2, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath1 = os.path.join(case1, postProc)
        mypath2 = os.path.join(case2, postProc)
        ExpData = ExpData_57
        ExpNames = ExpNames_57

    files1 = os.listdir(mypath1)
    files2 = os.listdir(mypath2)

    # read in the files
    for file in files1:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath1 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata1[name] = df

    # read in the files
    for file in files2:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath2 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata2[name] = df

    radialAv1 = list(LESdata1.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv1 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv1)

    radialAv2 = list(LESdata2.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv2 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv2)

    if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
        speciesEmean = species
        speciesErms = species+'_rms'
        species = 'Y_'+species
    elif any(species == f for f in ['J_sgs', 'J_lam', 'cellVolumes']):
        pass
    else:
        speciesEmean = species+'_mean'
        speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv1)):
        plt.figure(i+1)
        thisData1 = LESdata1[radialAv1[i]]
        thisData2 = LESdata2[radialAv2[i]]
        thisExp = ExpData[ExpNames[i]]

        # LES data case1
        plt.plot(thisData1['r_in_m']*factor, thisData1[species+'_mean'],'r', lw=1.6)
        plt.plot(thisData1['r_in_m']*factor, thisData1[species + '_rms'], 'r--', lw=1.6)

        # LES data case2
        plt.plot(thisData2['r_in_m'] * factor, thisData2[species + '_mean'], 'k', lw=1.6)
        plt.plot(thisData2['r_in_m'] * factor, thisData2[species + '_rms'], 'k--', lw=1.6)

        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        # plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        # plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        if species == 'cellVolumes':
            plt.ylabel('m^3')
            plt.ylim([-0.2e-10,5e-10])
        plt.xlabel('Radius [mm]')
        #plt.legend(['Case1 mean','Case1 RMS','Case2 mean','Case2 RMS'])
        plt.legend([case1.split('_')[-2:], 'RMS' ,case2.split('_')[-2:] , 'RMS'])
        #plt.legend(['1', '2', '3','4'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'_inert_compare.png'
        plt.savefig(fig_name)

    plt.show(block=False)


# plot inert case of current directory
def plotRadial_inert(species='Z', velocity=57,factor=1000):
    plt.close('all')

    LESdata1 = {}
    case1 = os.getcwd()

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    if velocity == 80:
        #if laminar:
        mypath1 = os.path.join(case1, postProc)
        #mypath2 = os.path.join(case2, postProc)
        #else:
        #    mypath1 = os.path.join(case1, postProc)
        #    mypath2 = os.path.join(case2, postProc)

        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath1 = os.path.join(case1, postProc)
        #mypath2 = os.path.join(case2, postProc)
        ExpData = ExpData_57
        ExpNames = ExpNames_57

    files1 = os.listdir(mypath1)
    #files2 = os.listdir(mypath2)

    # read in the files
    for file in files1:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath1 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata1[name] = df

    radialAv1 = list(LESdata1.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv1 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv1)

    if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
        speciesEmean = species
        speciesErms = species+'_rms'
        species = 'Y_'+species
    elif any(species == f for f in ['J_sgs', 'J_lam','J_r_sgs','J_r_lam']):
        pass
    else:
        speciesEmean = species+'_mean'
        speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv1)):
        plt.figure(i+1)
        thisData1 = LESdata1[radialAv1[i]]
        thisExp = ExpData[ExpNames[i]]

        # LES data case1
        plt.plot(thisData1['r_in_m']*factor, thisData1[species+'_mean'],'r', lw=1.6)
        #plt.plot(thisData1['r_in_m']*factor, thisData1[species + '_rms'], 'r--', lw=1.6)

        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        #plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        #plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius [mm]')
        #plt.legend(['Case1 mean','Case1 RMS','Case2 mean','Case2 RMS'])
        #plt.legend(['Case1 mean', 'Case2 mean'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'_inert.png'
        plt.savefig(fig_name)

    plt.show(block=False)

########################################
#compare two cases
########################################
def plotRadial_reactive_compareDNS(case1, species='Z', velocity=57,laminar=True,factor=1000):
    plt.close('all')

    LESdata1 = {}
    LESdata2 = {}

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    if velocity == 80:
        if laminar:
            mypath1 = os.path.join(case1, postProc)

        else:
            mypath1 = os.path.join(case1, postProc)


        ExpData = ExpData_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath1 = os.path.join(case1, postProc)

        ExpData = ExpData_57
        ExpNames = ExpNames_57

    files1 = os.listdir(mypath1)

    # read in the files
    for file in files1:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath1 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
           # print(name)
            LESdata1[name] = df

    radialAv1 = list(LESdata1.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv1 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv1)


    if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
        speciesEmean = species
        speciesErms = species+'_rms'
        species = 'Y_'+species
    else:
        speciesEmean = species+'_mean'
        speciesErms = species+'_rms'

    ########################################
    # DNS data read in
    DNS_data_mean = {}
    DNS_data_RMS = {}
    # compare with DNS data
    if species == 'T':
        DNS_path = '/home/max/Documents/02_Konferenzen/CombustionSymposium/Symposium_Paper/sources/Mean_Temperature/DNS_Temp'
        DNS_files = os.listdir(DNS_path)
        DNS_files = [f for f in DNS_files if f.endswith('txt')]
        # read in mean
        for f in DNS_files:
            if 'TMean' in f:
                df = pd.read_csv(os.path.join(DNS_path,f),delimiter=' ')
                name = f[11:]
                DNS_data_mean[name] = df
            elif 'TPrime2Mean' in f:
                df = pd.read_csv(os.path.join(DNS_path,f),delimiter=' ')
                name = f[11:]
                DNS_data_RMS[name] = df

        DNS_keys_mean = list(DNS_data_mean.keys())
        file_order_mean = [int(re.search('TMean_xD_(.*).txt',f).group(1)) for f in DNS_keys_mean]
        DNS_keys_mean = [x for _, x in sorted(zip(file_order_mean,DNS_keys_mean))]

        DNS_keys_RMS = list(DNS_data_RMS.keys())
        file_order_RMS = [int(re.search('TPrime2Mean_xD_(.*).txt', f).group(1)) for f in DNS_keys_RMS]
        DNS_keys_RMS = [x for _, x in sorted(zip(file_order_RMS, DNS_keys_RMS))]
        print('Done with data reading')

    elif species == 'Z':
        DNS_path = '/home/max/Documents/02_Konferenzen/CombustionSymposium/Symposium_Paper/sources/Mean_Z/DNS_Z'
        DNS_files = os.listdir(DNS_path)
        DNS_files = os.listdir(DNS_path)
        DNS_files = [f for f in DNS_files if f.endswith('txt')]
        # read in mean
        for f in DNS_files:
            if 'MaxMean' in f:
                df = pd.read_csv(os.path.join(DNS_path,f),delimiter=' ')
                name = f[11:]
                DNS_data_mean[name] = df
            elif 'MaxPrime2Mean' in f:
                df = pd.read_csv(os.path.join(DNS_path,f),delimiter=' ')
                name = f[11:]
                DNS_data_RMS[name] = df

        DNS_keys_mean = list(DNS_data_mean.keys())
        print(DNS_keys_mean)
        print('\n\n\n')
        file_order_mean = [int(re.search('BilgerMixFrac_MaxMean_xD_(.*).txt', f).group(1)) for f in DNS_keys_mean]
        DNS_keys_mean = [x for _, x in sorted(zip(file_order_mean, DNS_keys_mean))]

        DNS_keys_RMS = list(DNS_data_RMS.keys())
        file_order_RMS = [int(re.search('BilgerMixFrac_MaxPrime2Mean_xD_(.*).txt', f).group(1)) for f in DNS_keys_RMS]
        DNS_keys_RMS = [x for _, x in sorted(zip(file_order_RMS, DNS_keys_RMS))]
        print('Done with data reading')

    ########################################

    # radialAv = list(LESdata.keys())
    # loop over the different planes:
    for i in range(len(radialAv1)):
        plt.figure(i+1)
        thisData1 = LESdata1[radialAv1[i]]

        thisExp = ExpData[ExpNames[i]]

        # LES data case1
        plt.plot(thisData1['r_in_m']*factor, thisData1[species+'_mean'],'k', lw=1.8)
        plt.plot(thisData1['r_in_m']*factor, thisData1[species + '_rms'], 'k--', lw=1.8)

        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r [m]'], thisExp[speciesEmean], 'bo', lw=1)
        plt.plot(thisExp['r [m]'], thisExp[speciesErms], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(species+' at plane x/D = ' + location_dict[i])
        plt.ylabel(species)
        plt.xlabel('Radius [mm]')
        if species == 'T' or species == 'Z':
            thisDNS_mean = DNS_data_mean[DNS_keys_mean[i]]
            thisDNS_RMS = DNS_data_RMS[DNS_keys_RMS[i]]
            # LES data case1
            if species == 'T':
                print(thisDNS_mean.head())
                plt.plot(thisDNS_mean['rInmm'] , thisDNS_mean['TMean'], 'r-', lw=1.8)
            elif species == 'Z':
                #print(thisDNS_mean.head())
                plt.plot(thisDNS_mean['rInmm'] , thisDNS_mean['BilgerMixFrac_MaxMean'], 'r-', lw=1.8)
            #print(thisDNS_RMS.head())
            plt.plot(thisDNS_RMS['rInmm'] , thisDNS_RMS['RMS'], 'r--', lw=1.6)
            plt.legend(['LES mean', 'LES RMS', 'Exp mean', 'Exp RMS', 'DNS mean', 'DNS RMS'])

        else:
            plt.legend(['LES mean', 'LES RMS', 'Exp mean', 'Exp RMS'])
        plt.grid()
        fig_name = species+'_'+location_dict[i]+'_compareDNS.png'
        plt.savefig(fig_name)

    plt.show(block=False)


