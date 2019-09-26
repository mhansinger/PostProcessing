#/usr/local/bin/python3.6

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy import stats
import os.path

try:
    import seaborn as sns
except:
    print('Install seaborn package for python!')

'''
Extract the probes data and does radial averaging
subsequently it creats PDF plots

@author: mhansinger 

latest change: may 2019
'''


############################
# User adjustment
############################

# how many planes at x/D?
planes = np.array([1,2,3,4,5,6,7,8,9,10,15,20,25,30])

# slices
slices = 8
nr_probes = 18

# probe over which radial line to which distance from center?
dist = 0.012    # [m]

# probe spacing?
spacing = 0.00075  # [m]

# which fields you want to read in?
fields = ['H2O', 'O2', 'CH4', 'CO2', 'T', 'f_Bilger','CO', 'T_1','T_2','T_3','T_4','T_5','T_6','T_7','T_8']

# read in the data
#path='postProcessing/probes/'
path = input('Where is the probes data?, type in: ')

# diameter of Burner
D = 0.0075  # [m]


############################
# Do not change
###########################


nr_planes=int(len(planes))
datapoints_all = int(nr_probes*nr_planes*slices)

# find time step directories:
timesteps = os.listdir(path)
timesteps = [f for f in timesteps if os.path.isdir(path)]

print('time steps are: ', timesteps)

# number of radial probes
nr_probes = int(dist/spacing + 2)

# read in the data
# header lines
header_lines = int(nr_probes*slices*len(planes))

# data structure:
# every nr_probes^th step you enter a new slice
# every slices*nr_probes you enter a new plane

# set up data container:
# contains for every field, the different planes and radial averaged data points
# first entry is the fields, second the planes, timestep rows * slice, and the number of probes per slice

# this has be done to initialize the data container!
rows = 0
for i in range(len(timesteps)):
    data_raw = np.genfromtxt(path + '/' + timesteps[i] + '/' + fields[0], dtype='float')
    data_raw = data_raw[:, 1:]  # skips the first entry, which is actually the time step
    rows += data_raw.shape[0]

####################################
# contains ALL the data:
data_container = np.zeros((len(fields), int(nr_planes), int(nr_probes), (rows*slices)))
####################################

# loop over the different fields
print('Reading in the data\n')
for f in range(len(fields)):

    for j in range(len(timesteps)):
        if j == 0:
            data_raw = np.genfromtxt(path + '/' + timesteps[j] + '/' + fields[f], dtype='float')
            data_raw = data_raw[:, 1:]  # skips the first entry, which is actually the time step
        else:
            data_raw2 = np.genfromtxt(path + '/' + timesteps[j] + '/' + fields[f], dtype='float')
            data_raw2 = data_raw2[:, 1:]  # skips the first entry, which is actually the time step
            # stack the data to the existing data_raw
            data_raw=np.vstack((data_raw, data_raw2))

    # loop over the time steps
    for t in range(data_raw.shape[0]):

        # loop over planes: every nr_probes*slices is the next plane
        slice_count=0
        for p in range(nr_planes):
            #print(slice_count)

            for s in range(0,8):
                bin_counter=(slices*t+s)
                for i in range(int(nr_probes)):
                    data_container[f][p][i][bin_counter] = data_raw[t][(i+0+slice_count)]

                slice_count += nr_probes
                #print(bin_counter)


def plotPDFs():
    species = input('Which fields? ')
    bins = input('How many bins? ')
    bins = int(bins)

    position = input('Radial position? ')
    position = int(position)

    #get species index
    idx_species = fields.index(species)

    for i in range(0,nr_planes):

        data = data_container[idx_species][i][position][:]
        plt.figure(i)
        plt.hist(data , bins, facecolor='red')

        # To plot correct percentages in the y axis
        #to_percentage = lambda y, pos: str(round((y / float(len(data))) * 100.0, 2))
        #plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        plt.title(str(fields[idx_species])+ ' at r = '+str(round(spacing*position*1000, 3)) + 'mm and x/D = '+ str(planes[i]))
        plt.ylabel('Hits')
        # To plot correct percentages in the y axis
        to_percentage = lambda y, pos: str(round( ( y / float(len(data))) * 100.0, 2)) + '%'
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        if species == 'T':
            plt.xlabel('Temperature')
            #plt.xlim(290,2400)
        else:
            plt.xlabel('Mass fraction')
            #plt.xlim(0,1)

    plt.show(block=False)


def plotPDF2():
    species = input('Which fields? ')
    bins = input('How many bins? ')
    bins = int(bins)

    position = input('Radial position? ')
    position = int(position)

    #get species index
    idx_species = fields.index(species)

    for i in range(0,nr_planes):

        data = data_container[idx_species][i][position][:]
        plt.figure(i)
        #plt.hist(data , bins, facecolor='red')

        sns.distplot(data, bins=bins, kde=False, fit=stats.lognorm)
        #sns.kdeplot(data)

        # To plot correct percentages in the y axis
        #to_percentage = lambda y, pos: str(round((y / float(len(data))) * 100.0, 2))
        #plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        plt.title(str(fields[idx_species])+ ' at r = '+str(round(spacing*position*1000, 3)) + 'mm and x/D = '+ str(planes[i]))
        plt.ylabel('Hits')
        # To plot correct percentages in the y axis
        to_percentage = lambda y, pos: str(round( ( y / float(len(data))) * 100.0, 2)) + '%'
        #plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        if species == 'T':
            plt.xlabel('Temperature')
            #plt.xlim(290,2400)
        else:
            plt.xlabel('Mass fraction')
            #plt.xlim(0,1)

    plt.show(block=False)


#plt.close('all')

def bivariatePlot(sp1,sp2):
    '''
    :param sp1: Species 1 e.g. 'CH4'
    :param sp2: Species 2 e.g.  'O2'
    :return: 
    '''

    position = input('Radial position? ')
    position = int(position)

    idx_species1 = fields.index(sp1)
    idx_species2 = fields.index(sp2)

    for i in range(0, nr_planes):

        data = {sp1:data_container[idx_species1][i][position][:], sp2:data_container[idx_species2][i][position][:]}
        #data1 = pd.DataFrame(data_container[idx_species1][i][position][:])
        #data2 = pd.DataFrame(data_container[idx_species2][i][position][:])

        data = pd.DataFrame(data)

        plt.figure(i)
        #plt.hist(data , bins, facecolor='red')

        sns.jointplot(x=data[sp1], y=data[sp2], data=data,  kind="kde");

    plt.show(block=False)


#time series plot
def getTimeSeriesT(thisField='T', plane=5,pos=10, time=0):

    columns = [thisField+'_'+str(x) for x in range(1,9)]
    columns.insert(0,thisField)
    columns.append('T_mean')

    df = pd.DataFrame(columns=columns)

    for i in range(0,9):

        if i==0:
            field = thisField
        else:
            field = thisField+'_'+str(i)
        data_series = np.genfromtxt(path + '/' + timesteps[time] + '/' + field, dtype='float')
        data_series = data_series[:, 1:]

        data_col = (nr_probes*slices)*(plane-1)+pos
        print('get data from column: ',data_col)
        df[columns[i]] = (data_series[:,(data_col-1)])

    # extract the time
    time_series = data_series[:, 0]

    df['T_mean'] = df.iloc[:,1:-2].mean(axis=1)
    df['T_std'] = df.iloc[:,1:9].std(axis=1)
    df['low_std'] = df['T_mean'] - df['T_std']
    df['high_std'] = df['T_mean'] + df['T_std']
    df['time'] = time_series

    return df


#time series plot
def getTimeSeriesT64(thisField='T', plane=5,pos= 10, time=0 ):

    columns = [thisField+'_'+str(x) for x in range(1,65)]
    columns.insert(0,thisField)
    columns.append('T_mean')

    df = pd.DataFrame(columns=columns)

    for i in range(0,9):

        if i==0:
            field = thisField
        else:
            field = thisField+'_'+str(i)
        data_series = np.genfromtxt(path + '/' + timesteps[time] + '/' + field, dtype='float')
        data_series = data_series[:, 1:]
        data_col = (nr_probes*slices)*(plane-1)+pos
        print('get data from column: ',data_col)
        df[columns[i]] = (data_series[:,(data_col-1)])

    # extract the time
    time_series = data_series[:, 0]

    df['T_mean'] = df.iloc[:,1:-2].mean(axis=1)
    df['T_std'] = df.iloc[:,1:9].std(axis=1)
    df['low_std'] = df['T_mean'] - df['T_std']
    df['high_std'] = df['T_mean'] + df['T_std']
    df['time'] = time_series

    return df


#time series plot
def plotTimeSeriesT( plane=5,pos= 10, steps=500):

    columns = ['T_'+str(x) for x in range(1,9)]
    columns.insert(0,'T')

    df = pd.DataFrame(columns=columns)
    plt.figure()

    for i in range(0,9):

        if i==0:
            field = 'T'
            plt.plot(df['T'].iloc[0:steps],'k',lw=2)
        else:
            field = 'T_'+str(i)
        data_series = np.genfromtxt(path + '/' + timesteps[-1] + '/' + field, dtype='float')
        data_series = data_series[:, 1:]
        data_col = (nr_probes*slices)*(plane-1)+pos
        print('get data from column: ',data_col)
        df[columns[i]] = (data_series[:,(data_col-1)])

        plt.plot(data_series[0:steps],'k--',lw=1)

    plt.show()

    # #return df
    # plt.figure()
    # for i in
    #
    # plt.plot(df['T'],'k',lw=2)



def plotPDFplane():
    species = input('Which fields? ')
    bins = input('How many bins? ')
    bins = int(bins)

    plane = input('Which plane? ')
    plane = int(plane)

    #get species index
    idx_species = fields.index(species)

    for i in range(0,nr_probes):

        data = data_container[idx_species][plane][i][:]
        plt.figure(i)
        plt.hist(data , bins, facecolor='red')

        # To plot correct percentages in the y axis
        #to_percentage = lambda y, pos: str(round((y / float(len(data))) * 100.0, 2))
        #plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        plt.title(str(fields[idx_species])+ ' at r = '+str(round(spacing*i*1000, 3)) + 'mm and x/D = '+ str(plane))
        plt.ylabel('Hits')
        # To plot correct percentages in the y axis
        to_percentage = lambda y, pos: str(round( ( y / float(len(data))) * 100.0, 2)) + '%'
        plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
        if species == 'T':
            plt.xlabel('Temperature')
            #plt.xlim(290,2400)
        else:
            plt.xlabel('Mass fraction')
            #plt.xlim(0,1)

    plt.show(block=False)





