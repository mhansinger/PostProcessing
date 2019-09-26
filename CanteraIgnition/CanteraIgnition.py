'''
This is to visualize differences in Lu19 Lu30 and GRI3.0
@author: mhansinger
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join

cantera_path = '/home/max/HDD2_Data/OF4_Simulations/CanteraIgnition/'

cases = ['IgniteGRI', 'IgniteLu30','IgniteLu19','IgniteLu13']


t_step = '/postProcessing/probes/0/'

def compare_species(spec='CH4'):
    #plt.figure()
    for case in cases:
        thisPath = cantera_path+case+t_step+spec

        this_data = np.genfromtxt(thisPath)
        plt.plot(this_data[:,0],this_data[:,1])
        plt.xlim(0,8e-5)

    plt.xlabel('time [s]')
    plt.ylabel('mass fraction [-]')
    plt.grid(True)
    plt.legend(cases)
    fig = plt.gcf()
    fig.set_size_inches(10,8)
    plt.title('Ignition delay for %s' % spec)
    plt.savefig(cantera_path+spec)
    plt.show(block=False)


