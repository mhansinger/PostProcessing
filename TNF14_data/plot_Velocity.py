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

location_dict = ['010','050','100','200','300']

postProc='postProcessing/sampleDict'


##############################
# Experimental data is:
# scatter
##############################

# reads in the velocity data
Exp_Velocity = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Reacting_Velocity-5GP'

Exp_Velocity_inert = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/Non-reacting_Velocity-5GP'

velocity_files = os.listdir(Exp_Velocity)

velocity_inert_files = os.listdir(Exp_Velocity_inert)

ExpVel_57 = {}
ExpVel_inert_57 = {}
ExpVel_80 = {}
# read in the data
for file in velocity_files:
    if file.endswith("0.csv") and 'Lr75-57' in file:
        print('Reading in Velocity data from: '+file)
        df = pd.read_csv(Exp_Velocity+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpVel_57[name] = df
    if file.endswith("0.csv") and 'Lr75-80' in file:
        print('Reading in Velocity data from: '+file)
        df = pd.read_csv(Exp_Velocity+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpVel_80[name] = df


for file in velocity_inert_files:
    if file.endswith("0.csv") and 'Lr75-57' in file:
        print('Reading in inert Velocity data from: '+file)
        df = pd.read_csv(Exp_Velocity+'/'+file, sep=',')
        # generate file name
        name = file[0:-4]
        ExpVel_inert_57[name] = df



ExpNames_57 = list(ExpVel_57.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames_57]
ExpNames_57 = [x for _, x in sorted(zip(exp_order, ExpNames_57))]

#inert cases
ExpNames_inert_57 = list(ExpVel_inert_57.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames_inert_57]
ExpNames_inert_57 = [x for _, x in sorted(zip(exp_order, ExpNames_inert_57))]

ExpNames_80 = list(ExpVel_80.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames_80]
ExpNames_80 = [x for _, x in sorted(zip(exp_order, ExpNames_80))]

print('\nsorted!')

#####################################
# plots
#####################################

def plotVelocity(case=path_dict['case_05_lowMa_path'],velocity=57,laminar=True,factor=1000):
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

        ExpData = ExpVel_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath = os.path.join(case, postProc)
        ExpData = ExpVel_57
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
            if name[-3:] != '120':
                if name[-3:] != '150':
                    #print(name[-3:])
                    LESdata[name] = df

    print(LESdata.keys())

    radialAv = list(LESdata.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv = [x for _, x in sorted(zip(file_order, radialAv))]
    print('\nsorted!')
    print(radialAv)
    #
    # if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
    #     speciesEmean = species
    #     speciesErms = species+'_rms'
    #     species = 'Y_'+species
    # else:
    #     speciesEmean = species+'_mean'
    #     speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:

    print(ExpNames)

    j = 0

    for i in range(len(LESdata)):#,len(radialAv)):
        plt.figure(i+1)
        thisData = LESdata[radialAv[i]]
        thisExp = ExpData[ExpNames[i+1]]

        print(ExpNames[i+1])
        print(radialAv[i])

        # LES data
        plt.plot(thisData['r[m]']*factor, thisData['U_axial_mean'],'r', lw=1.6)
        #thisData['r[m]'].max()
        #try:
        #    if species == 'f_Bilger':
        plt.plot(thisData['r[m]']*factor, thisData['U_axial_rms'], 'r', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r(mm)'], thisExp['U(m/s)'], 'bo', lw=1)
        plt.plot(thisExp['r(mm)'], thisExp['Urms(m/s)'], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title('U at Plane x/D = ' + location_dict[i])
        plt.ylabel('U [m/s]')
        plt.xlabel('Radius [mm]')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name ='U_'+location_dict[i]+'.png'
        plt.savefig(fig_name)


    plt.show(block=False)


#####################################
# plots compare


def plotVelocity_compare(case1=path_dict['case_05_path'],case2=path_dict['case_05_lowMa_path'],velocity=57,laminar=True,factor=1000):
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

        ExpData = ExpVel_80
        ExpNames = ExpNames_80

    elif velocity == 57:
        mypath1 = os.path.join(case1, postProc)
        mypath2 = os.path.join(case2, postProc)
        ExpData = ExpVel_57
        ExpNames = ExpNames_57

    files1 = os.listdir(mypath1)
    files2 = os.listdir(mypath2)

    # read in the files case1
    count=0
    for i, file in enumerate(files1):
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            df = pd.read_csv(mypath1 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
            # print(name)
            if name[-3:] != '120':
                if name[-3:] != '150':
                    #print(name[-3:])
                    print('Reading in data from: ' + file)
                    LESdata1[name] = df
                    count+=1

    print(LESdata1.keys())

    # read in the files case1
    count=0
    for i,file in enumerate(files2):
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            df = pd.read_csv(mypath2 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
            # print(name)
            if name[-3:] != '120':
                if name[-3:] != '150':
                    print('Reading in data from: ' + file)
                    #print(name[-3:])
                    LESdata2[name] = df
                    count=+1

    print(LESdata2.keys())

    radialAv1 = list(LESdata1.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv1]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv1 = [x for _, x in sorted(zip(file_order, radialAv1))]
    print('\nsorted!')
    print(radialAv1)

    radialAv2 = list(LESdata2.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv2]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv2 = [x for _, x in sorted(zip(file_order, radialAv2))]
    print('\nsorted!')
    print(radialAv2)

    #
    # if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
    #     speciesEmean = species
    #     speciesErms = species+'_rms'
    #     species = 'Y_'+species
    # else:
    #     speciesEmean = species+'_mean'
    #     speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:

    print(ExpNames)

    j = 0

    for i in range(len(LESdata1)):#,len(radialAv)):
        plt.figure(i)
        thisData1 = LESdata1[radialAv1[i]]
        thisData2 = LESdata2[radialAv2[i]]
        thisExp = ExpData[ExpNames[i]]

        print(ExpNames[i])
        print(radialAv1[i])

        # LES data case1
        plt.plot(thisData1['r[m]']*factor, thisData1['U_axial_mean'],'r', lw=1.6)
        plt.plot(thisData1['r[m]']*factor, thisData1['U_axial_rms'], 'r', lw=1.6)

        # LES data case2
        plt.plot(thisData2['r[m]']*factor, thisData2['U_axial_mean'],'k', lw=1.6)
        plt.plot(thisData2['r[m]']*factor, thisData2['U_axial_rms'], 'k', lw=1.6)


        plt.plot(thisExp['r(mm)'], thisExp['U(m/s)'], 'bo', lw=1)
        plt.plot(thisExp['r(mm)'], thisExp['Urms(m/s)'], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title('U at Plane x/D = ' + location_dict[i])
        plt.ylabel('U [m/s]')
        plt.xlabel('Radius [mm]')
        plt.legend(['Case1 mean', 'Case1 RMS', 'Case2 mean', 'Case2 RMS', 'Exp. mean', 'Exp RMS'])
        plt.grid()
        fig_name ='U_'+location_dict[i]+'_compare.png'
        plt.savefig(fig_name)


    plt.show(block=False)



def plotVelocity_inert(case=path_dict['case_05_lowMa_path'],laminar=True,factor=1000):
    plt.close('all')

    LESdata = {}

    try:
        velocity=int(velocity)
    except:
        print('')

    # get the files path

    mypath = os.path.join(case, postProc)
    ExpData = ExpVel_inert_57
    ExpNames = ExpNames_inert_57

    files = os.listdir(mypath)

    # read in the files
    for file in files:
        if file.endswith("TNF14.txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath + '/' + file, sep='\t')
            # generate file name
            name = file[0:-10]
            # print(name)
            if name[-3:] != '120':
                if name[-3:] != '150':
                    #print(name[-3:])
                    LESdata[name] = df

    print(LESdata.keys())

    radialAv = list(LESdata.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv = [x for _, x in sorted(zip(file_order, radialAv))]
    print('\nsorted!')
    print(radialAv)
    #
    # if any(species == f for f in ['CH4','O2','H2O','CO2','CO']):
    #     speciesEmean = species
    #     speciesErms = species+'_rms'
    #     species = 'Y_'+species
    # else:
    #     speciesEmean = species+'_mean'
    #     speciesErms = species+'_rms'

    # radialAv = list(LESdata.keys())
    # loop over the different planes:

    print(ExpNames)

    j = 0

    for i in range(len(LESdata)):#,len(radialAv)):
        plt.figure(i+1)
        thisData = LESdata[radialAv[i]]
        thisExp = ExpData[ExpNames[i+1]]

        print(ExpNames[i+1])
        print(radialAv[i])

        # LES data
        plt.plot(thisData['r[m]']*factor, thisData['U_axial_mean'],'r', lw=1.6)
        #thisData['r[m]'].max()
        #try:
        #    if species == 'f_Bilger':
        plt.plot(thisData['r[m]']*factor, thisData['U_axial_rms'], 'r', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['r(mm)'], thisExp['U(m/s)'], 'bo', lw=1)
        plt.plot(thisExp['r(mm)'], thisExp['Urms(m/s)'], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title('U at Plane x/D = ' + location_dict[i])
        plt.ylabel('U [m/s]')
        plt.xlabel('Radius [mm]')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name ='U_'+location_dict[i]+'.png'
        plt.savefig(fig_name)


    plt.show(block=False)