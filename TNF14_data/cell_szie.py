

import numpy as np
import pandas as pd
from os import listdir
from os.path import isdir

scalarTail = '_cellVol.xy'

# initialize arrays
datapoints = 200
noFiles = 40

# represents the different locations you defined in the sample dict file
nLocation = [0, 1, 2, 3, 4, 5, 6]
location_dict = ['010', '050', '100', '120', '150', '200', '300']

# get all time steps
times = listdir('postProcessing/sampleDict/')
# remove the .txt files in the times list as they are also stored in the sampleDict folder
times = [f for f in times if f[-3:] != 'txt']

# loop over the time steps for averaging

for n in range(0, len(nLocation)):
    arraySize = np.zeros((datapoints))
    #arrayDist = np.zeros((datapoints))

    for time in times:
        for j in range(0, noFiles):
            this_path = 'postProcessing/sampleDict/' + time + '/line_x' + str(nLocation[n]) + '-r' + str(j) + scalarTail
            print(this_path)
            dataScalar = np.loadtxt(this_path)
            # except OSError:
            #     dataScalar = np.loadtxt(case_path+'/postProcessing/sampleDict/' + time + '/line_x' +
            #                         str(nLocation[n]) + '-r' + str(j) + scalarTail2)

            # there is the position of the T column in your data set; check for consistency! they are summed up for different j
            arraySize += np.cbrt(dataScalar[:, 3])
            arrayYPos = dataScalar[:, 1]
            arrayZPos = dataScalar[:, 2]
            arrayDist = np.sqrt(arrayYPos * arrayYPos + arrayZPos * arrayZPos)


        # loop 2 end
        # set up to write the output file!
        Output_np = np.array((arraySize))

        # Divide by the number of files and transpose
        Output_T = Output_np.T
        Output_T = Output_T / (noFiles * len(times))
        # set up dataframe to write as CSV
        Output_df = pd.DataFrame(Output_T)

        # Name correctly the output columns
        Output_df.columns = ['cellSize']

        Output_df['r_in_m'] = arrayDist

        # remove the nan
        Output_df = Output_df.fillna(0)

        # write one output file for each position
        output_name = 'postProcessing/sampleDict/' + 'line_xD' + location_dict[n] + '_cellSize.txt'
        pd.DataFrame.to_csv(Output_df, output_name, index=False, sep='\t')

print('Sampled case \n')


