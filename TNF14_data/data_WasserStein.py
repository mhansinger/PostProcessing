# this is to generate the data files for the Wasser Stein metric for the Ihme grou

import numpy as np
import pandas as pd
import os
from os.path import join

# path to the scatter data
scatter_path = 'postProcessing/scatter/'

###################
# CASE? --> adjust
case='57'
##################

file_names = os.listdir(scatter_path)
file_names = [f for f in file_names if f[-9:] == 'TNF14.txt']

column_names = ['Z','T','Y_CO2','Y_CO']

nr_samples = 1000
D = 0.0075

delta = 0.125
rD_max = 2.0

nBins = int(rD_max/delta)
nrBin = range(1,nBins+1)

intervals = [b*delta for b in range(1,nBins+1)]


for f in file_names:
    this_path = join(scatter_path,f)

    this_data = pd.read_csv(this_path,'\t')

    # remove unnecessary columns
    this_data=this_data.drop(['Y_H2O','Y_O2','Y_CH4','Y_H2'],axis=1)

    this_data.insert(0, 'rD',this_data['r[m]'].values/D)

    this_data=this_data.sort_values(by=['rD'])

    # initialize the bin column
    this_data.insert(0,'#Bin_Index',0)

    this_data=this_data.reset_index(drop=True)

    for i,_ in enumerate(intervals):
        if i==0:
            crit = this_data['rD']<intervals[i]
            this_data['#Bin_Index'].loc[this_data[crit].index]=nrBin[i]
        else:
            crit1 = intervals[i-1]<= this_data['rD']#<intervals[i]
            crit2 = this_data['rD'] < intervals[i]
            # WORKS!
            this_data['#Bin_Index'].loc[this_data[crit1 & crit2].index] = nrBin[i]

    # now sample exactly 'nr_samples' from each category
    for b in nrBin:
        if b==1:
            data_array_all = this_data[this_data['#Bin_Index'] == b].sample(nr_samples).values
        else:
            data_array_new = this_data[this_data['#Bin_Index'] == b].sample(nr_samples).values
            data_array_all = np.concatenate([data_array_all,data_array_new])

        if len(data_array_all) < 1000:
            print(data_array_all.shape)

    # create final dataframe
    df_final = pd.DataFrame(data_array_all,columns=this_data.columns)

    plane = f[-13:-10]  # e.g. 050
    output_name = 'reactive_ubulk%s_wm_scatter_xD%s.dat' % (case, plane)


    df_final.to_csv(join(scatter_path,output_name),sep='\t',index=False)
    print('Done with: %s' % plane)




