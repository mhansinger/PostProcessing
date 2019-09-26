import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from os.path import join


try:
    from matplotlib2tikz import save as tikz_save
except:
    print('Install matplotlib2tikz: pip3 install matplotlib2tikz')

'''
File to process/visualiz the stored scatter data and compare it with experimental data
@author: mhansinger
'''

location_dict =['07.5','15','30','45']

mypath = 'scatter' #input('Where did you save the scatter data?, type in: ')

files = os.listdir(mypath)

data = {}

# read in the files and ignore xD10 as we dont have ExpData for it
for file in files:
     if file.endswith(".txt") and not file.endswith('xD10.txt'):
         print('Reading in data from: '+file)
         df = pd.read_csv(mypath+'/'+file,sep='\t')
         # generate file name
         name = file[0:-4]
         data[name] = df

scatterPlanes = list(data.keys())

# get the order of the files
file_order = [float(f.split('xD')[1]) for f in scatterPlanes]
#sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
scatterPlanes = [x for _,x in sorted(zip(file_order,scatterPlanes))]


#############################################
# reads in the experimental scatter data for D, E, F Sandia Flames
#############################################
# exppath = input('\nWhere is the experimental data?: ')
# expfiles = os.listdir(exppath)
exppath = '/home/max/Documents/10_Experimental_Data/ExpData_Sandia_Federica' #Sandia_Flames/pmCDEFarchives' #input('\nWhere is the experimental data?: ')
expfiles = os.listdir(exppath)
expfiles = [e for e in expfiles if e.endswith('.scat')]


ExpData_D = {}
# read in the data
D_path = join(exppath,'pmD.scat')
for file in os.listdir(D_path):
    print('Reading in data from: ' + file)
    df = pd.read_csv(join(exppath ,'pmD.scat' ,file), sep='\t',skiprows=3)
    print(df)
    # generate file name
    name = file.split('.Yall')[0]
    if name == 'D075':
        name = 'D07.5'
    ExpData_D[name] = df

ExpNames_D = list(ExpData_D.keys())
# get the order of the files from the file ending
exp_order = [float(f[1:]) for f in ExpNames_D]
ExpNames_D = [x for _, x in sorted(zip(exp_order, ExpNames_D))]


ExpData_E = {}
# read in the data
E_path = join(exppath,'pmE.scat')
for file in os.listdir(E_path):
     if file.endswith(".Yall"):
         print('Reading in data from: '+file)
         df = pd.read_csv(join(exppath ,'pmE.scat' ,file), sep='\t',skiprows=3)
         # generate file name
         name = file.split('.Yall')[0]
         if name == 'E075':
             name = 'E07.5'
         ExpData_E[name] = df

ExpNames_E = list(ExpData_E.keys())
# get the order of the files from the file ending
exp_order = [float(f[1:]) for f in ExpNames_E]
ExpNames_E = [x for _, x in sorted(zip(exp_order, ExpNames_E))]


ExpData_F = {}
# read in the data
F_path = join(exppath,'pmF.scat')
for file in os.listdir(F_path):
     if file.endswith(".Yall"):
         print('Reading in data from: '+file)
         df = pd.read_csv(join(exppath ,'pmF.scat' ,file), sep='\t',skiprows=3)
         # generate file name
         name = file.split('.Yall')[0]
         if name == 'F075':
             name = 'F07.5'
         ExpData_F[name] = df

ExpNames_F = list(ExpData_F.keys())
# get the order of the files from the file ending
exp_order = [float(f[1:]) for f in ExpNames_F]
ExpNames_F = [x for _, x in sorted(zip(exp_order, ExpNames_F))]


#############################################
# reads in the 8 stochastic fields
#############################################
# mypath_8 = input('\n Where did you save the data of the fine simulation?, type in: ')
#
# try:
#     files_8 = os.listdir(mypath_8)
#
#     data_8 = {}
#     # read in the files
#     for file in files_8:
#         if file.endswith(".txt"):
#             print('Reading in data from: ' + file)
#             df = pd.read_csv(mypath_8 + '/' + file, sep='\t')
#             # generate file name
#             name = file[0:-4]
#             data_8[name] = df
#
#     scatterPlanes_8 = list(data.keys())
#     # get the order of the files
#     file_order_8 = [int(f[-3:]) for f in scatterPlanes_8]
#     # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
#     scatterPlanes_8 = [x for _, x in sorted(zip(file_order_8, scatterPlanes_8))]
# except FileNotFoundError:
#    print('No 8 Fields Data')



#############################################
# plots
#############################################
def plotData(spec='T',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i + 1)
            thisData = data[scatterPlanes[i]].sample(sampleSize)
            plt.scatter(thisData['f'], thisData[spec], marker='.', s=0.3)
            plt.xlabel('Mixture fraction f')
            plt.ylabel(spec)
            plt.xlim(0, 1)
            minSpec = min(thisData[spec]) * 0.999
            maxSpec = max(thisData[spec]) * 1.05
            plt.ylim(minSpec, maxSpec)
            plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
    except:
        print('Species not available')

    plt.show(block=False)


def plotCompare(case, spec='T',sampleSize=5000):
    # creates a scatter plot of the defined species over the mixture fraction

    # switch for case
    if case=='D':
        ExpData=ExpData_D
        ExpNames=ExpNames_D
    elif case=='E':
        ExpData = ExpData_E
        ExpNames = ExpNames_E
    elif case=='F':
        ExpData = ExpData_F
        ExpNames = ExpNames_F

    if spec == 'T':
        specE = 'T(K)'
    else:
        specE = 'Y'+spec

    for i in range(len(scatterPlanes)):
        plt.figure(i+1)
        thisData = data[scatterPlanes[i]].sample(sampleSize)
        thisExp = ExpData[ExpNames[i]]

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10,6))
        #ax1.grid()
        ax1.scatter(thisData['f'], thisData[spec], marker='.', s=0.3)
        ax1.set_xlabel('f')
        ax1.set_ylabel(spec)

        ax1.set_title('Simulation Flame %s' % case)

        #ax2.grid()
        ax2.scatter(thisExp['F'], thisExp[specE], marker='.', s=0.3, color='k')
        ax2.set_title('Experiment')
        ax2.set_xlabel('f Bilger')

        if spec=='T':
            ax1.set_xlim(0, 1)
            ax2.set_xlim(0, 1)
        minSpec = min(thisData[spec]) * 0.999
        maxSpec = max(thisData[spec]) * 1.1
        ax1.set_ylim(minSpec, maxSpec)
        ax2.set_ylim(minSpec, maxSpec)
        f.suptitle('Plane: '+ location_dict[i])

    plt.show(block=False)


def plotDataPlane(spec='T',plane=3,sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction
    i=plane

    # loop over the different planes:
    try:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)
        ax.set_xticks([0, 0.2,0.4,0.6,0.8,1])

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(alpha=0.3, color='k')
        thisData = data[scatterPlanes[i]].sample(sampleSize)
        plt.scatter(thisData['f'], thisData[spec], marker='.', s=0.3, color='k')
        # plt.xlabel('Mixture fraction f')
        # plt.ylabel(spec)

        minSpec = min(thisData[spec]) * 0.999
        maxSpec = max(thisData[spec]) * 1.05
        if spec is 'T':
            plt.xlim(0, 1)
            plt.ylim(300, 2500)
            ax.set_yticks([500, 1000, 1500, 2000, 2500])
        else:
            plt.xlim(0, 1)
            plt.ylim(0, maxSpec)
            yticks = np.linspace(0,maxSpec,5)
            ax.set_yticks(yticks)

        plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + '.png', bbox_inches='tight', pad_inches=0)

    except:
        print('Species not available')

    plt.show(block=False)



def plotDataPlaneExp(case,spec='T(K)',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction

    # switch for case
    if case == 'D':
        ExpData = ExpData_D
        ExpNames = ExpNames_D
    elif case == 'E':
        ExpData = ExpData_E
        ExpNames = ExpNames_E
    elif case == 'F':
        ExpData = ExpData_F
        ExpNames = ExpNames_F

    for i in range(0,len(ExpNames)):
        # loop over the different planes:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)

        thisExp = ExpData[ExpNames[i]].sample(sampleSize)
        ax.set_xticks([0, 0.25, 0.5, 0.75,1.0])
        ax.set_yticks([500, 1000, 1500, 2000, 2500])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(alpha=0.3, color='k')
        plt.scatter(thisExp['F'], thisExp[spec], marker='.', s=0.3, color='k')
        # plt.xlabel('Mixture fraction f')
        # plt.ylabel(spec)
        plt.xlim(0, 1)
        minSpec = min(thisExp[spec]) * 0.999
        maxSpec = max(thisExp[spec]) * 1.05
        plt.ylim(300, 2500)
        plt.title('Scatter plot at: x/D=' + str(float(location_dict[i]) ))
        # ax.axis('off')

        plt.savefig(str(spec) + '_xD_' + str(float(location_dict[i])) + '.png', bbox_inches='tight', pad_inches=0)
        plt.show(block=False)

