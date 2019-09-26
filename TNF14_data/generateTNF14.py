'''
This file is to generate the data structure for the TNF14 data submission.
It collects the data from the different simulations and stores it according to the data-tree

@author: mhansinger
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join
import shutil

from radial_samples_inert_TNF14 import radial_samples_inert
from radial_samples_reacting_TNF14 import radial_samples_reacting
from scatter_samples_TNF14 import scatter_samples

##############################
# define the root path, where to store the data
# example:  /home/max/Documents/07_KIT_TNF/04_TNF14/BundeswehrUniversityMunich/cold/ubulk80/radial_profiles

root_path='/home/max/Documents/07_KIT_TNF/04_TNF14/BundeswehrUniversityMunich_3/'
root_types=['cold','non_reactive','reactive']
root_cases=['ubulk57','ubulk80']
root_data=['radial_profiles','scatter_profiles']
##############################

# specify the paths to the simulation data
# ubulk57
case_13_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-13_inert_LES_cold'
case_12_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-12_inert_LES_hot'
case_05_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05'
case_19_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-19_kEq_57_ESF'

case_17_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-17_inert_kEqn_hot'
case_18_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/case-18_inert_kEqn_cold'

#DNS
case_11_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-11_inert_DNS'
case_24_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-24_inert_80_60mio'

postProc='postProcessing/sampleDict'

# ubulk80
case_20_path_i='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-20_inert_LES_hot_80'
case_21_path='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case-21_inert_LES_cold_80'
case_22_path_r='/home/max/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-22_Lr75-80'

case_20_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-20_kEqn_80_lam'#'/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-20_kEq_80_ESF'

case_22_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case_22_inert_k_80_hot'
case_23_path='/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/Cluster/Lr75_80/case_23_inert_k_80_cold'



##############################
# single file names
planes = ['line_xD010_TNF14.txt','line_xD050_TNF14.txt','line_xD100_TNF14.txt','line_xD120_TNF14.txt',
          'line_xD150_TNF14.txt','line_xD200_TNF14.txt','line_xD300_TNF14.txt']

radial_names_end = ['radial_xD010.dat','radial_xD050.dat','radial_xD100.dat',
                    'radial_xD120.dat','radial_xD150.dat','radial_xD200.dat','radial_xD300.dat']




# for loop over cases for the radial profiles
for type in root_types:
    for case in root_cases:

        # if type == 'reactive':
        #     if case == 'ubulk57':
        #         this_case = case_19_path
        #         #reacting
        #         radial_samples_reacting(case_path = this_case)
        #         read_path = join(this_case, postProc)
        #         write_path = root_path+type+'/'+case+'/radial_profiles/'
        #
        #         # rename and copy files
        #         for ix, p in enumerate(planes):
        #             plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
        #             this_read_path = join(read_path, p)
        #             shutil.copyfile(this_read_path, join(write_path, plane_name_write))
        #
        #     elif case == 'ubulk80':
        #         this_case = case_20_path
        #         radial_samples_reacting(case_path=this_case)
        #         read_path = join(this_case, postProc)
        #         write_path = root_path+type+'/'+case+'/radial_profiles/'
        #
        #         # rename and copy files
        #         for ix, p in enumerate(planes):
        #             plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
        #             this_read_path = join(read_path, p)
        #             shutil.copyfile(this_read_path, join(write_path, plane_name_write))

        if type == 'non_reactive':
            if case == 'ubulk57':
                this_case = case_11_path
                #inert
                radial_samples_inert(case_path = this_case)
                read_path = join(this_case, postProc)
                write_path = root_path + type + '/' + case + '/radial_profiles/'

                # rename and copy files
                for ix, p in enumerate(planes):
                    plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
                    this_read_path = join(read_path, p)
                    shutil.copyfile(this_read_path, join(write_path, plane_name_write))

            elif case == 'ubulk80':
                this_case = case_24_path
                radial_samples_inert(case_path=this_case)
                read_path = join(this_case, postProc)
                write_path = root_path+type+'/'+case+'/radial_profiles/'

                # rename and copy files
                for ix, p in enumerate(planes):
                    plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
                    this_read_path = join(read_path, p)
                    shutil.copyfile(this_read_path, join(write_path, plane_name_write))

        # elif type == 'cold':
        #     if case == 'ubulk57':
        #         this_case = case_18_path
        #         #inert
        #         radial_samples_inert(case_path = this_case)
        #         read_path = join(this_case, postProc)
        #         write_path = root_path + type + '/' + case + '/radial_profiles/'
        #
        #         # rename and copy files
        #         for ix, p in enumerate(planes):
        #             plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
        #             this_read_path = join(read_path, p)
        #             shutil.copyfile(this_read_path, join(write_path, plane_name_write))
        #
        #     elif case == 'ubulk80':
        #         this_case = case_23_path
        #         radial_samples_inert(case_path=this_case)
        #         read_path = join(this_case, postProc)
        #         write_path = root_path+type+'/'+case+'/radial_profiles/'
        #
        #         # rename and copy files
        #         for ix, p in enumerate(planes):
        #             plane_name_write = type + '_' + case + '_' + radial_names_end[ix]
        #             this_read_path = join(read_path, p)
        #             shutil.copyfile(this_read_path, join(write_path, plane_name_write))


# loop over the reactive cases for the scatter data


scatter_names_end = ['scatter_xD010.dat','scatter_xD050.dat','scatter_xD100.dat','scatter_xD120.dat',
                     'scatter_xD150.dat','scatter_xD200.dat','scatter_xD300.dat']

scatter_planes = ['scatter_xD010_TNF14.txt','scatter_xD050_TNF14.txt','scatter_xD100_TNF14.txt','scatter_xD120_TNF14.txt',
                  'scatter_xD150_TNF14.txt','scatter_xD200_TNF14.txt','scatter_xD300_TNF14.txt']

# for case in root_cases:
#     if case == 'ubulk57':
#         postProc = 'postProcessing/scatter/'
#         this_case = case_19_path
#         # postProcess scatter data
#         scatter_samples(case_path=this_case)
#         read_path = join(this_case, postProc)
#         write_path = root_path +  'reactive/' + case + '/scatter_profiles/'
#
#         # rename and copy files
#         for ix, p in enumerate(scatter_planes):
#             plane_name_write = 'reactive_' + case + '_' + scatter_names_end[ix]
#             this_read_path = join(read_path, p)
#             shutil.copyfile(this_read_path, join(write_path, plane_name_write))
#
#         print('Done with scatter data: %s ' % case)
#
#     elif case == 'ubulk80':
#         postProc = 'postProcessing/scatter/'
#         this_case = case_20_path
#         # postProcess scatter data
#         scatter_samples(case_path=this_case)
#         read_path = join(this_case, postProc)
#         write_path = root_path +  'reactive/' + case + '/scatter_profiles/'
#
#         # rename and copy files
#         for ix, p in enumerate(scatter_planes):
#             plane_name_write = 'reactive_' + case + '_' + scatter_names_end[ix]
#             this_read_path = join(read_path, p)
#             shutil.copyfile(this_read_path, join(write_path, plane_name_write))
#
#         print('Done with scatter data: %s ' % case)
