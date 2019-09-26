import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
try:
    from matplotlib2tikz import save as tikz_save
except:
    print('Install matplotlib2tikz: pip3 install matplotlib2tikz')

'''
File to process/visualiz the stored scatter data and compare it with experimental data
@author: mhansinger
'''

location_dict =['010','050','100','120','150','200','300']

#############################################
# reads in the 8 stochastic fields
#############################################
mypath = input('Where did you save the scatter data?, type in: ')

files = os.listdir(mypath)

data = {}

# read in the files
for file in files:
     if file.endswith(".txt"):
         print('Reading in data from: '+file)
         df = pd.read_csv(mypath+'/'+file,sep='\t')
         # generate file name
         name = file[0:-4]
         data[name] = df

scatterPlanes = list(data.keys())
# get the order of the files
file_order = [int(f[-3:]) for f in scatterPlanes]
#sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
scatterPlanes = [x for _,x in sorted(zip(file_order,scatterPlanes))]


#############################################
# reads in the experimental data
#############################################
exppath = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/species-5GP-2015' #input('\nWhere is the experimental data?: ')
expfiles = os.listdir(exppath)

# /home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species_Mean_RMS-5GP/Mixture_fraction_Favre
# /home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species_Mean_RMS-5GP/Radial_Favre
# /home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Reacting_Species-5GP

ExpData = {}
# read in the data
for file in expfiles:
     if file.endswith(".csv"):
         print('Reading in data from: '+file)
         df = pd.read_csv(exppath+'/'+file, sep=',')
         # generate file name
         name = file[0:-4]
         ExpData[name] = df

ExpNames = list(ExpData.keys())
# get the order of the files from the file ending
exp_order = [int(f[-3:]) for f in ExpNames]
ExpNames = [x for _, x in sorted(zip(exp_order, ExpNames))]




#############################################
# plots
#############################################
def plotData(spec='T', sparse=1, colorby='radius'):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')
    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i + 1)
            thisData = data[scatterPlanes[i]]
            plt.scatter(thisData['f_Bilger'].iloc[::sparse], thisData[spec].iloc[::sparse], s=0.3, c=thisData[colorby].iloc[::sparse], cmap='jet_r')
            cbar = plt.colorbar()
            if colorby=='radius':
                plt.clim(0,max(thisData[colorby]/3))
            cbar.set_label(colorby)
            plt.xlabel('Mixture fraction f')
            plt.ylabel(spec)
            plt.xlim(0, 0.3)
            minSpec = min(thisData[spec]) * 0.999
            maxSpec = max(thisData[spec]) * 1.05
            plt.ylim(minSpec, maxSpec)
            plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
    except:
        print('Species not available')

    plt.show(block=False)


def plotCompare(spec='T'):
    # creates a scatter plot of the defined species over the mixture fraction
    if spec == 'T':
        specE = 'Tray'
    else:
        specE = spec

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i+1)
            thisData = data[scatterPlanes[i]]
            thisExp = ExpData[ExpNames[i]]
            f, (ax1, ax2) = plt.subplots(1, 2, share=True, figsize=(10,6))
            #ax1.grid()
            ax1.scatter(thisData['f_Bilger'], thisData[spec], s=0.3, c=thisData['radius'], cmap='jet_r')
            ax1.set_xlabel('f Bilger')
            ax1.set_ylabel(spec)

            ax1.set_title('Simulation')

            #ax2.grid()
            ax2.scatter(thisExp['Fblgr'], thisExp[specE], marker='.', s=0.2, color='k')
            ax2.set_title('Experiment')
            ax2.set_xlabel('f Bilger')

            if spec=='T':
                ax1.set_xlim(0, 0.3)
                ax2.set_xlim(0, 0.3)
            minSpec = min(thisData[spec]) * 0.999
            maxSpec = max(thisData[spec]) * 1.1
            ax1.set_ylim(minSpec, maxSpec)
            ax2.set_ylim(minSpec, maxSpec)

            f.suptitle('Plane: '+ location_dict[i])

    except:
        print('Species not available')

    plt.show(block=False)


def plotDataPlane(spec='T',plane=3):
    # creates a scatter plot of the defined species over the mixture fraction
    i=plane
    # loop over the different planes:
    try:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)
        ax.set_xticks([0, 0.1, 0.2, 0.3])
        ax.set_yticks([500, 1000, 1500, 2000, 2500])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(alpha=0.3, color='k')
        thisData = data[scatterPlanes[i]]
        plt.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2, color='k')
        # plt.xlabel('Mixture fraction f')
        # plt.ylabel(spec)
        plt.xlim(0, 0.3)
        minSpec = min(thisData[spec]) * 0.999
        maxSpec = max(thisData[spec]) * 1.05
        plt.ylim(300, 2500)
        # plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
        # ax.axis('off')

        plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + '.png', bbox_inches='tight', pad_inches=0)

    except:
        print('Species not available')

    plt.show(block=False)


def plotCompare_8(spec='T'):
    # creates a scatter plot of the defined species over the mixture fraction
    if spec == 'T':
        specE = 'Tray'
    else:
        specE = spec

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i+1)
            thisData = data[scatterPlanes[i]]
            thisData_8 = data_8[scatterPlanes_8[i]]
            thisExp = ExpData[ExpNames[i]]
            f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(10,6))
            #ax1.grid()
            ax1.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2)
            ax1.set_xlabel('f Bilger')
            ax1.set_ylabel(spec)

            ax1.set_title('Simulation: laminar')

            #ax2.grid()
            ax2.scatter(thisData_8['f_Bilger'], thisData_8[spec], marker='.', s=0.2)
            ax2.set_xlabel('f Bilger')
            ax2.set_ylabel(spec)

            ax2.set_title('Simulation: 8 fields')

            #ax3.grid()
            ax3.scatter(thisExp['Fblgr'], thisExp[specE], marker='.', s=0.2, color='k')
            ax3.set_title('Experiment')
            ax3.set_xlabel('f Bilger')

            if spec=='T':
                ax1.set_xlim(0, 0.3)
                ax2.set_xlim(0, 0.3)
                ax3.set_xlim(0, 0.3)
            minSpec = min(thisData[spec]) * 0.999
            maxSpec = max(thisData[spec]) * 1.1
            ax1.set_ylim(minSpec, maxSpec)
            ax2.set_ylim(minSpec, maxSpec)
            ax3.set_ylim(minSpec, maxSpec)

            f.suptitle('Plane: '+ location_dict[i])

    except:
        print('Species not available')

    plt.show(block=False)

#
# if scalar == 'O2':
#     sddd
