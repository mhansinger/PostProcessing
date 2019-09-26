import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

'''
To plot the radial averaged mean quantities

@author: mhansinger 
'''

location_dict =['010','050','100','120','150','200','300']

# read in and sort the simulation data
mypath = 'postProcessing/sampleDict/'#input('Where is the extracted radial data? : ')

files = os.listdir(mypath)

LESdata = {}

# read in the files
for file in files:
     if file.endswith(".txt"):         # to exclude the TNF Data with different headers
         print('Reading in data from: '+file)
         df = pd.read_csv(mypath+'/'+file,sep='\t')
         # generate file name
         name = file[0:-4]
         LESdata[name] = df

radialAv = list(LESdata.keys())
# get the order of the files
file_order = [int(f[-9:-6]) for f in radialAv]
#sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
radialAv = [x for _,x in sorted(zip(file_order, radialAv))]
print('\nsorted!')

# read in and sort the experimental data
expPath = '/home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species_Mean_RMS-5GP/Radial_Favre'
#input('\nWhere is the experimental data?\nProbably it is: /home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species_Mean_RMS-5GP/Radial_Favre')

# /home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species_Mean_RMS-5GP/Radial_Favre

# reads in the velocity case
vel = input('Velocity case? : ')
#FJ200-5GP-Lr75-57-xD010_Radial_Reynolds

expfiles = os.listdir(expPath)

ExpData = {}
# read in the data
for file in expfiles:
     if file.endswith(".csv") and file[15:17]==vel:
         print('Reading in data from: '+file)
         df = pd.read_csv(expPath+'/'+file, sep=',')
         # generate file name
         name = file[0:-4]
         ExpData[name] = df

ExpNames = list(ExpData.keys())
# get the order of the files from the file ending
exp_order = [int(str(''.join(list(filter(str.isdigit, f))))[-3:]) for f in ExpNames]
ExpNames = [x for _, x in sorted(zip(exp_order, ExpNames))]
print('\nsorted!')

#####################################
#moredata = input('Read in other data? (True/False) ')

#if moredata:
try:
    new_path = input('Which path? ')
    new_data_path = new_path+'/'+mypath

    files2 = os.listdir(new_data_path)

    LESdata2 = {}

    # read in the files
    for file in files2:
        if file.endswith(".txt"):  # to exclude the TNF Data with different headers
            print('Reading in data from: ' + file)
            df = pd.read_csv(new_data_path + '/' + file, sep='\t')
            # generate file name
            name = file[0:-4]
            LESdata2[name] = df

    radialAv2 = list(LESdata2.keys())
    # get the order of the files
    file_order = [int(f[-3:]) for f in radialAv2]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    radialAv2 = [x for _, x in sorted(zip(file_order, radialAv2))]
    print('\nsorted!')
except:
    pass


#####################################
# plots
#####################################

def plotRadial(field='T', factor=1000):
    plt.close('all')
    # creates a scatter plot of the defined species over the mixture fraction
    if field == 'T':
        fieldE = 'Tray'
    elif field=='Z':
        #field='f_Bilger'
        fieldE='Fblgr'
    else:
        fieldE = field

    # loop over the different planes:
    #try:
    for i in range(len(radialAv)):
        plt.figure(i+1)
        thisData = LESdata[radialAv[i]]
        thisExp = ExpData[ExpNames[i]]

        # LES data
        plt.plot(thisData['r[m]']*factor, thisData[field+'_mean'],'r', lw=1.6)
        #try:
        #    if field == 'f_Bilger':
        plt.plot(thisData['r[m]']*factor, thisData[field + '_rms'], 'r', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['xmm mean'], thisExp[fieldE + ' mean'], 'bo', lw=1)
        plt.plot(thisExp['xmm mean'], thisExp[fieldE + ' RMS'], 'bo', lw=1)
        plt.xlim([0, 18])
        plt.title(field+' at Plane x/D = ' + location_dict[i])
        plt.ylabel(field)
        plt.xlabel('Radius [mm]')
        plt.legend(['LES mean','LES RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name = field+'_'+location_dict[i]+'.png'
        plt.savefig(fig_name)


    #except:
     #   print('Species not available')

    plt.show(block=False)


def plot2cases(field='T'):
    plt.close('all')
    # creates a scatter plot of the defined species over the mixture fraction
    if field == 'T':
        fieldE = 'Tray'
    elif field=='f':
        #field='f_Bilger'
        fieldE='Fblgr'
    else:
        fieldE = field


    # loop over the different planes:
    #try:
    for i in range(len(radialAv)):
        plt.figure(i+1)
        thisData = LESdata[radialAv[i]]
        thisExp = ExpData[ExpNames[i]]
        thisData2 = LESdata2[radialAv2[i]]

        # LES data
        plt.plot(thisData['x_Pos'], thisData[field],'r', lw=1.6)
        plt.plot(thisData2['x_Pos'], thisData2[field], 'b', lw=1.6)
        #try:
        #    if field == 'f_Bilger':
        plt.plot(thisData['x_Pos'], thisData[field + 'RMS'], 'r', lw=1.6)
        plt.plot(thisData2['x_Pos'], thisData2[field + 'RMS'], 'b', lw=1.6)
        #except:
        #    print('No RMS data given from LES')
        # Experimental data
        plt.plot(thisExp['xmm mean'], thisExp[fieldE + ' mean'], 'ko', lw=1)
        plt.plot(thisExp['xmm mean'], thisExp[fieldE + ' RMS'], 'ko', lw=1)
        plt.xlim([0, 16])
        plt.title(field+' at Plane x/D = ' + location_dict[i])
        plt.ylabel(field)
        plt.xlabel('Radius [mm]')
        plt.legend(['LES k','LES WALE','LES k RMS','LES WALE RMS','Exp. mean','Exp RMS'])
        plt.grid()
        fig_name = field+'_'+location_dict[i]+'_2compare.png'
        plt.savefig(fig_name)


    plt.show(block=False)
