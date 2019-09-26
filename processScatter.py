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

mypath = input('Where did you save the scatter data?, type in: ')

files = os.listdir(mypath)

LESdata = {}

# read in the files
for file in files:
     if file.endswith(".txt"):
         print('Reading in data from: '+file)
         df = pd.read_csv(mypath+'/'+file,sep='\t')
         # generate file name
         name = file[0:-4]
         LESdata[name] = df

scatterPlanes = list(LESdata.keys())
# get the order of the files
file_order = [int(f[-3:]) for f in scatterPlanes]
#sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
scatterPlanes = [x for _,x in sorted(zip(file_order,scatterPlanes))]


#############################################
# reads in the experimental data
#############################################
# exppath = input('\nWhere is the experimental data?: ')
# expfiles = os.listdir(exppath)
exppath = '/home/max/Documents/07_KIT_TNF/04_TNF14/Exp_Data/species-5GP-2015' #'/home/max/Dropbox/TNF_DNS_LES/02_ExpData/Reacting_Species-5GP' #input('\nWhere is the experimental data?: ')
expfiles = os.listdir(exppath)

# consider only data from FJ200-5GP-Lr75-57:
expfiles = [e for e in expfiles if e.startswith('FJ200-5GP-Lr75-57')]

# reduce to location dict list
expfiles = [e for e in expfiles if any(xs in e[-7:-4] for xs in location_dict)]

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
# reads in the 8 stochastic fields
#############################################
mypath_8 = input('\n Where did you save the data of the fine simulation?, type in: ')

try:
    files_8 = os.listdir(mypath_8)

    data_8 = {}
    # read in the files
    for file in files_8:
        if file.endswith(".txt"):
            print('Reading in data from: ' + file)
            df = pd.read_csv(mypath_8 + '/' + file, sep='\t')
            # generate file name
            name = file[0:-4]
            data_8[name] = df

    scatterPlanes_8 = list(LESdata.keys())
    # get the order of the files
    file_order_8 = [int(f[-3:]) for f in scatterPlanes_8]
    # sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
    scatterPlanes_8 = [x for _, x in sorted(zip(file_order_8, scatterPlanes_8))]
except FileNotFoundError:
   print('No 8 Fields Data')



#############################################
# plots
#############################################
def plotData(spec='T',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i + 1)
            thisData = LESdata[scatterPlanes[i]].sample(sampleSize)
            plt.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2)
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


def plotDataColorPlane(spec='T',plane=0,color_by='T',colormap='inferno',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')
    # loop over the different planes:
    i=plane
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
    thisData = LESdata[scatterPlanes[i]].sample(sampleSize)
    this_color = thisData[color_by]

    plt.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2, c=this_color, cmap=colormap)
    # plt.xlabel('Mixture fraction f')
    # plt.ylabel(spec)
    plt.xlim(0, 0.3)
    minSpec = min(thisData[spec]) * 0.999
    maxSpec = max(thisData[spec]) * 1.05
    # plt.ylim(300, 2500)
    if spec == 'T':
        plt.ylim(300, 2500)
        ax.set_yticks([500, 1000, 1500, 2000, 2500])
    elif spec == 'CO':
        plt.ylim(0, 0.1)
        ax.set_yticks([0, 0.033, 0.066, 0.1])
    else:
        plt.ylim(0, 0.3)
        ax.set_yticks([0, 0.1, 0.2, 0.3])
    # plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
    # ax.axis('off')

    plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + '_color.png', bbox_inches='tight', pad_inches=0)
    plt.show(block=False)




def plotCompare(spec='T',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction
    if spec == 'T':
        specE = 'Tray'
    else:
        specE = spec

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i+1)
            thisData = LESdata[scatterPlanes[i]].sample(sampleSize)
            thisExp = ExpData[ExpNames[i]]

            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10,6))
            #ax1.grid()
            ax1.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2)
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
        ax.set_xticks([0, 0.1, 0.2, 0.3])
        ax.set_yticks([500, 1000, 1500, 2000, 2500])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(alpha=0.3, color='k')
        thisData = LESdata[scatterPlanes[i]].sample(sampleSize)
        plt.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2, color='k')
        # plt.xlabel('Mixture fraction f')
        # plt.ylabel(spec)
        plt.xlim(0, 0.3)
        minSpec = min(thisData[spec]) * 0.999
        maxSpec = max(thisData[spec]) * 1.05
        #plt.ylim(300, 2500)
        if spec == 'T':
            plt.ylim(300, 2500)
            ax.set_yticks([500, 1000, 1500, 2000, 2500])
        elif spec == 'CO':
            plt.ylim(0, 0.1)
            ax.set_yticks([0, 0.033, 0.066, 0.1])
        else:
            plt.ylim(0, 0.3)
            ax.set_yticks([0, 0.1, 0.2, 0.3])
        # plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
        # ax.axis('off')

        plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + '.png', bbox_inches='tight', pad_inches=0)

    except:
        print('Species not available')

    plt.show(block=False)



def plotDataPlaneExp(spec='Tray',sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')

    if spec == 'CO':
        spec='COLIF'

    for i in range(0,8):
        # loop over the different planes:
        try:
            fig = plt.figure(i + 1, frameon=False)
            ax = plt.gca()
            # ax = plt.Axes(fig, [0., 0., 1., 1.])
            # ax.set_axis_off()
            # fig.add_axes(ax)

            thisExp = ExpData[ExpNames[i]].sample(sampleSize)
            #print(thisExp)
            ax.set_xticks([0, 0.1, 0.2, 0.3])

            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(alpha=0.3, color='k')
            plt.scatter(thisExp['Fblgr'], thisExp[spec], marker='.', s=0.2, color='k')
            # plt.xlabel('Mixture fraction f')
            # plt.ylabel(spec)
            plt.xlim(0, 0.3)
            # minSpec = min(thisExp[spec]) * 0.999
            # maxSpec = max(thisExp[spec]) * 1.05
            if spec == 'Tray':
                plt.ylim(300, 2500)
                ax.set_yticks([500, 1000, 1500, 2000, 2500])
            elif spec == 'COLIF':
                plt.ylim(0, 0.1)
                ax.set_yticks([0, 0.033, 0.066, 0.1])
            else:
                plt.ylim(0,0.3)
                ax.set_yticks([0, 0.1, 0.2, 0.3])

            plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + 'Exp.png', bbox_inches='tight', pad_inches=0)

        except:
            print('Species not available')

        plt.show(block=False)


def plotDataPlaneExpColor(spec='Tray', color_by='Tray', colormap='inferno', sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')

    if spec == 'CO':
        spec='COLIF'

    for i in range(0,len(ExpNames)):#range(0,8):
        # loop over the different planes:
        try:
            fig = plt.figure(i + 1, frameon=False)
            ax = plt.gca()
            # ax = plt.Axes(fig, [0., 0., 1., 1.])
            # ax.set_axis_off()
            # fig.add_axes(ax)

            thisExp = ExpData[ExpNames[i]].sample(sampleSize)
            ax.set_xticks([0, 0.1, 0.2, 0.3])
            ax.set_yticks([500, 1000, 1500, 2000, 2500])
            ax.set_xticklabels([])

            ax.grid(alpha=0.3, color='k')
            plt.scatter(thisExp['Fblgr'], thisExp[spec], marker='.', c=thisExp[color_by], s=0.2, cmap=plt.get_cmap(colormap))
            # plt.xlabel('Mixture fraction f')
            # plt.ylabel(spec)
            plt.xlim(0, 0.3)
            minSpec = min(thisExp[spec]) * 0.999
            maxSpec = max(thisExp[spec]) * 1.05
            if spec == 'Tray':
                plt.ylim(300, 2500)
                ax.set_yticks([500, 1000, 1500, 2000, 2500])
            elif spec == 'COLIF':
                plt.ylim(0,0.1)
                ax.set_yticks([0, 0.033, 0.066, 0.1])
            else:
                plt.ylim(0,0.3)
                ax.set_yticks([0, 0.1, 0.2, 0.3])

            # plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) / 10))
            # ax.axis('off')

            plt.savefig(str(spec) + '_xD_' + str(int(location_dict[i])) + 'Exp_color.png', bbox_inches='tight', pad_inches=0)

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
            thisData = LESdata[scatterPlanes[i]]
            thisData_8 = data_8[scatterPlanes_8[i]]
            thisExp = ExpData[ExpNames[i]]
            f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(10,6))
            #ax1.grid()
            ax1.scatter(thisData['f_Bilger'], thisData[spec], marker='.', s=0.2)
            ax1.set_xlabel('f Bilger')
            ax1.set_ylabel(spec)

            ax1.set_title('Simulation: coarse')

            #ax2.grid()
            ax2.scatter(thisData_8['f_Bilger'], thisData_8[spec], marker='.', s=0.2)
            ax2.set_xlabel('f Bilger')
            ax2.set_ylabel(spec)

            ax2.set_title('Simulation: fine')

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


def writeConditionedExp(nr_bins):
    '''
    Writes the mean quantities conditioned on Mixture fraction
    :return:
    '''

    for this_name in ExpNames:
        this_set_df = ExpData[this_name]

        f_condition = np.linspace(0,1,nr_bins)

        this_np_array=np.zeros((1,this_set_df.shape[1]))
        this_np_std_array = np.zeros((1, this_set_df.shape[1]))

        for f in range(0,len(f_condition)-1):
            this_mean = this_set_df[this_set_df['Fblgr'].between(f_condition[f],f_condition[f+1])].mean()
            this_std = this_set_df[this_set_df['Fblgr'].between(f_condition[f], f_condition[f + 1])].std()
            #this_mean_np = np.array()

            #print(this_mean_np.shape)

            this_np_array = np.concatenate((this_np_array,[this_mean.values]))
            this_np_std_array = np.concatenate((this_np_std_array, [this_std.values]))

            #print(this_np_array.shape)

        this_mean_df = pd.DataFrame(data=this_np_array[1:,:],columns=this_set_df.columns)
        this_std_df = pd.DataFrame(data=this_np_std_array[1:, :], columns=this_set_df.columns)

        # plt.figure()
        # plt.plot(this_mean_df['Fblgr'],this_mean_df['Tray'])
        # plt.show(block=False)

        this_mean_df.to_csv('scatter/Exp_conditioned_mean_%s' % this_name[-5:],sep=',',index=False)
        this_std_df.to_csv('scatter/Exp_conditioned_std_%s' % this_name[-5:],sep=',',index=False)


def writeConditionedSim(nr_bins):
    '''
    Writes the mean quantities conditioned on Mixture fraction
    :return:
    '''

    for this_name in scatterPlanes:
        this_set_df = LESdata[this_name]

        f_condition = np.linspace(0,1,nr_bins)

        this_np_array=np.zeros((1,this_set_df.shape[1]))
        this_np_std_array = np.zeros((1, this_set_df.shape[1]))

        for f in range(0,len(f_condition)-1):
            this_mean = this_set_df[this_set_df['f_Bilger'].between(f_condition[f], f_condition[f + 1])].mean()
            this_std = this_set_df[this_set_df['f_Bilger'].between(f_condition[f], f_condition[f + 1])].std()
            # this_mean_np = np.array()

            # print(this_mean_np.shape)

            this_np_array = np.concatenate((this_np_array, [this_mean.values]))
            this_np_std_array = np.concatenate((this_np_std_array, [this_std.values]))

            # print(this_np_array.shape)

        this_mean_df = pd.DataFrame(data=this_np_array[1:, :], columns=this_set_df.columns)
        this_std_df = pd.DataFrame(data=this_np_std_array[1:, :], columns=this_set_df.columns)

    #     plt.figure()
    #     plt.plot(this_mean_df['f_Bilger'],this_mean_df['T'])
    # plt.show(block=False)

        this_mean_df.to_csv('scatter/LES_conditioned_mean_%s.csv' % this_name[-5:],sep=',',index=False)
        this_std_df.to_csv('scatter/LES_conditioned_std_%s.csv' % this_name[-5:],sep=',',index=False)


def getHistogramsExp(spec='Tray',sampleSize=1000,f_min=0.05,f_max=0.06,bins=50):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')

    if spec == 'CO':
        spec='COLIF'

    for i in range(0,7):
        # loop over the different planes:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        # ax.set_axis_off()
        # fig.add_axes(ax)

        thisExp = ExpData[ExpNames[i]]

        thisExp_reduced = thisExp[(thisExp.Fblgr > f_min) & (thisExp.Fblgr < f_max)].sample(sampleSize)
        # print(thisExp)
        plt.figure()
        plt.hist(thisExp_reduced[spec], bins=50, normed=True)
        plt.title(spec + ' at x/D=' + location_dict[i])

        pdf, vals = np.histogram(thisExp_reduced[spec], bins=bins, normed=True)

        vals_new = np.zeros(bins)

        for j in range(bins):
            vals_new[j] = (vals[j] + vals[j + 1]) / 2

        data_stack = np.stack((pdf, vals_new), axis=-1)

        # write the data
        data_stack_pd = pd.DataFrame(data=data_stack, columns=['pdf', spec])
        file_name = 'scatter/Exp/P_' + spec + '_xD_' + location_dict[i] + '_f_min' + str(f_min) + '_Exp.csv'
        data_stack_pd.to_csv(file_name, index=False, sep=',')

        file_name2 = 'scatter/Exp/reduced_' + spec + '_xD_' + location_dict[i] + '_f_min' + str(f_min) + '_Exp.csv'
        thisExp_reduced.to_csv(file_name2,index=False)

        plt.show(block=False)


def getHistogramsSim(spec='T',sampleSize=1000,f_min=0.05,f_max=0.06,bins=50):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')
    #
    # if spec == 'CO':
    #     spec='COLIF'

    for i in range(0,7):
        # loop over the different planes:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()

        thisSim = LESdata[scatterPlanes[i]]

        try:
            thisSim_reduced = thisSim[(thisSim.f_Bilger > f_min) & (thisSim.f_Bilger < f_max)].sample(sampleSize)
        except ValueError:
            print('sample size is reduced')
            thisSim_reduced = thisSim[(thisSim.f_Bilger > f_min) & (thisSim.f_Bilger < f_max)].sample(sampleSize,replace=True)
        # print(thisExp)
        plt.figure()
        plt.hist(thisSim_reduced[spec], bins=bins, normed=True)
        plt.title(spec + ' at x/D=' + location_dict[i])

        pdf, vals = np.histogram(thisSim_reduced[spec], bins=bins, normed=True)
        # vals = np.histogram_bin_edges(thisSim_reduced[spec],bins=bins-1)

        vals_new = np.zeros(bins)

        for j in range(bins):
            vals_new[j] = (vals[j] + vals[j + 1]) / 2

        data_stack = np.stack((pdf, vals_new), axis=-1)

        # write the data
        data_stack_pd = pd.DataFrame(data=data_stack, columns=['pdf', spec])
        file_name = 'scatter/Sim/P_' + spec + '_xD_' + location_dict[i] + '_f_min' + str(f_min) + '_Sim.csv'
        data_stack_pd.to_csv(file_name, index=False, sep=',')

        file_name2 = 'scatter/Sim/reduced_' + spec + '_xD_' + location_dict[i] + '_f_min' + str(f_min) + '_Sim.csv'
        thisSim_reduced.to_csv(file_name2,index=False)

        plt.show(block=False)

def getBurningIndexSim(spec='T',sampleSize=1000,f_min=0.05,f_max=0.06,bins=50,Tmax=2100):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')
    #
    # if spec == 'CO':
    #     spec='COLIF'

    BI = pd.DataFrame(data=np.zeros((7,2)),columns=['pos','BI'])

    for i in range(0,7):
        # loop over the different planes:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()

        thisSim = LESdata[scatterPlanes[i]]

        try:
            thisSim_reduced = thisSim[(thisSim.f_Bilger > f_min) & (thisSim.f_Bilger < f_max)]
        except ValueError:
            print('sample size is reduced')
            thisSim_reduced = thisSim[(thisSim.f_Bilger > f_min) & (thisSim.f_Bilger < f_max)]

        this_BI = (thisSim_reduced['T'].mean() - 300)/ (Tmax - 300)

        BI['pos'].iloc[i] = scatterPlanes[i]
        BI['BI'].iloc[i] = this_BI

        print('BI at %s is %f' % (location_dict[i],this_BI))

    BI.to_csv('scatter/Sim/BI.csv',sep=',',index=False)



def getBurningIndexExp(spec='T',sampleSize=1000,f_min=0.05,f_max=0.06,bins=50,Tmax=2100):
    # creates a scatter plot of the defined species over the mixture fraction
    plt.close('all')
    #
    # if spec == 'CO':
    #     spec='COLIF'

    BI = pd.DataFrame(data=np.zeros((7,2)),columns=['pos','BI'])

    for i in range(0,7):
        # loop over the different planes:
        fig = plt.figure(i + 1, frameon=False)
        ax = plt.gca()

        thisExp = ExpData[ExpNames[i]]

        try:
            thisSim_reduced = thisExp[(thisExp.Fblgr > f_min) & (thisExp.Fblgr < f_max)]
        except ValueError:
            print('sample size is reduced')
            thisSim_reduced = thisExp[(thisExp.Fblgr > f_min) & (thisExp.Fblgr < f_max)]

        this_BI = (thisSim_reduced['Tray'].mean() - 300) / (Tmax - 300)

        BI['pos'].iloc[i] = scatterPlanes[i]
        BI['BI'].iloc[i] = this_BI

        print('BI at %s is %f' % (location_dict[i],this_BI))

    BI.to_csv('scatter/Exp/BI.csv',sep=',',index=False)
