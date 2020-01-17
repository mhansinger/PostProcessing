'''
This file is to check if the T shift is also present if Z is computed with species (and not f_Bilger)
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from os.path import join
import cantera as ct

plt.close('all')

######################################
# some parameters
Z_st = 0.351 # Sandia
Y_CH4_F = 0.1563714
Y_H2_F = 0
Y_O2_Ox = 0.232917 # Sandia

# Oxygen-Fuel to mass ratio. See Peters, p.172
nu = (1-Z_st)/Z_st * Y_O2_Ox/(Y_CH4_F+Y_H2_F)

try:
    from matplotlib2tikz import save as tikz_save
except:
    print('Install matplotlib2tikz: pip3 install matplotlib2tikz')


location_dict =['07.5','15','30','45']

mypath = 'scatter' #input('Where did you save the scatter data?, type in: ')

files = os.listdir(mypath)

LESdata = {}

# # read in the files
# for file in files:
#      if file.endswith(".txt") and file.startswith("scatter_xD"):
#          print('Reading in data from: '+file)
#          df = pd.read_csv(mypath+'/'+file,sep='\t')
#          # generate file name
#          name = file.split('.txt')[0]
#          LESdata[name] = df
# read in the files and ignore xD10 as we dont have ExpData for it
for file in files:
     if file.endswith(".txt") and not file.endswith('xD10.txt'):
         print('Reading in data from: '+file)
         df = pd.read_csv(mypath+'/'+file,sep='\t')
         # generate file name
         name = file[0:-4]
         LESdata[name] = df

scatterPlanes = list(LESdata.keys())
# get the order of the files
file_order = [float(f.split('xD')[1]) for f in scatterPlanes]
#sort_vec = sorted(range(len(file_order)), key=lambda k: file_order[k])
scatterPlanes = [x for _,x in sorted(zip(file_order,scatterPlanes))]

############################################
# plots
def plotZ_compare(sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction

    # loop over the different planes:
    try:
        for i in range(len(scatterPlanes)):
            plt.figure(i + 1)
            thisData = LESdata[scatterPlanes[i]] #.sample(sampleSize)
            thisData['Z_species'] = (nu* (thisData['CH4'] + thisData['H2']) - thisData['O2'] + Y_O2_Ox)/(nu*(Y_H2_F + Y_CH4_F) + Y_O2_Ox)
            plt.scatter(thisData['f_Bilger'], thisData['T'], marker='.', s=0.2,c='k')
            plt.scatter(thisData['Z_species'], thisData['T'], marker='.', s=0.2, c='r')
            plt.xlabel('Mixture fraction')
            plt.ylabel('T')
            plt.xlim(0, 0.3)
            plt.plot([Z_st,Z_st],[0,2500],'--',lw=0.5)
            minSpec = min(thisData['T']) * 0.999
            maxSpec = max(thisData['T']) * 1.05
            plt.ylim(minSpec, maxSpec)
            plt.legend(['Bilger','Species','Z_st'])
            plt.title('Scatter plot at: x/D=' + str(int(location_dict[i]) ))

    except:
        print('Species not available')

    plt.show(block=False)


#############################################
# RADIATION
#############################################
'''
Estimate the radiation of the Flame based on Optically-Thin Layer
check TNF Radiation models and TNF Proceeding Nr6

Under the assumptions that these flames are optically thin, such that each radiating point source has an 
unimpeded isotropic view of the cold surroundings, the radiative loss rate per unit volume may be calculated as:

Q(T,species) = 4  SUM{pi*ap,i} *(T4-Tb4)

where

    sigma=5.669e-08 W/m2K4 is the Steffan-Boltzmann constant, 
    SUM{ } represents a summation over the species included in the radiation calculation, 
    pi is the partial pressure of species i in atmospheres (mole fraction times local pressure),
    ap,i is the Planck mean absorption coefficient of species i,
    T is the local flame temperature (K), and 
    Tb is the background temperature (300K unless otherwise specified in the experimental data).

Note that the Tb term is not consistent with an emission-only model. 
It is included here to eliminate the unphysical possibility of calculated temperatures in the coflowing air 
dropping below the ambient temperature. In practice, this term has a negligible effect on results.

CO2 and H2O are the most important radiating species for hydrocarbon flames. As an example, 
Jay Gore reports that the peak temperature in a strained laminar flame calculation decreased by 50K when 
radiation by CO2 and H2O was included. Inclusion of CH4 and CO dropped the peak temperature by another 5K. 
On the rich side of the same flames the maximum effect of adding the CH4 and CO radiation was an 8K reduction 
in temperature (from 1280 K to 1272 K for a particular location). These were OPPDIF calculations 
(modified to include radiation) of methane/air flames with 1.5 cm separation between nozzles and 8 cm/s fuel and air velocities.

ap = c0 + c1*(1000/T) + c2*(1000/T)2 + c3*(1000/T)3 + c4*(1000/T)4 + c5*(1000/T)5

The coefficients are:
 	 H2O	        CO2
c0	-0.23093	    18.741
c1	-1.12390	    -121.310
c2	9.41530	        273.500
c3	-2.99880	    -194.050
c4	0.51382	        56.310
c5	-1.86840E-05	-5.8169

A fourth-order polynomial in temperature is used for CH4:

ap,ch4 = 6.6334 – 0.0035686*T + 1.6682e-08*T2 + 2.5611e-10*T3 – 2.6558e-14*T4

A fit for CO is given in two temperature ranges:

ap,co = c0+T*(c1 + T*(c2 + T*(c3 + T*c4)))
'''

# set up cantera gas to get molar weights
gas = ct.Solution('gri30.xml')

# sampled species
species = ['CO','H2O','H2','O2','CH4','OH','CO2']

T_b = 294 # Background temperature [K]

sigma=5.669e-08 # W/m2K4 is the Steffan-Boltzmann constant,

# Absorption coefficient for CO2
ap_CO2 = lambda T: 18.741 -121.310*(1000/T) + 273.500*(1000/T)**2 -194.050*(1000/T)**3 + 56.310*(1000/T)**4 -5.8169*(1000/T)**5

# Absorption coefficient for H2O
ap_H2O = lambda T: 	-0.23093 -1.12390*(1000/T) + 9.41530*(1000/T)**2 -2.99880*(1000/T)**3 + 0.51382*(1000/T)**4  -1.86840E-05*(1000/T)**5

# Absorption coefficient for CH4
ap_CH4 = lambda T: 6.6334- 0.0035686 * T + 1.6682e-08 * T**2 + 2.5611e-10 * T**3 - 2.6558e-14 * T**4

# Absorption coefficient for CO
ap_CO = lambda T: 10.09 - 0.001183 * T + 4.775e-06 * T**2  - 5.872e-10 * T**3 - 2.533e-14 * T**4


# plots
def plot_Radiation(sampleSize=50000):
    # creates a scatter plot of the defined species over the mixture fraction

    for i in range(len(scatterPlanes)-1):
        plt.figure(i + 1)
        thisData = LESdata[scatterPlanes[i]]#.sample(sampleSize)
        thisData = compute_mol_fractions(thisData)
        T = thisData['T']

        # absorption coefficients x molar fraction of species
        Q_CO2 = thisData['x_CO2'] * ap_CO2(T)
        Q_H2O = thisData['x_H2O'] * ap_H2O(T)
        Q_CH4 = thisData['x_CH4'] * ap_CH4(T)
        Q_CO = thisData['x_CO'] * ap_CO(T)

        thisData['Q_radiation'] = 4*sigma*(T**4- T_b**4)*(Q_CO2 + Q_H2O + Q_CH4 + Q_CO)

        thisData_sample = thisData.sample(sampleSize)
        #plt.scatter(thisData_sample['f_Sandia'], thisData_sample['heatRelease'], s=0.2,c='r')
        plt.scatter(thisData_sample['f_Sandia'],thisData_sample['Q_radiation'],s=0.2,c='k')

        plt.xlabel('Mixture fraction')
        plt.ylabel('Q_radiation [W]')
        # plt.xlim(0, 0.3)
        plt.xlim(0, max(thisData_sample['f_Sandia']))
        #plt.plot([Z_st,Z_st],[0,2500],'--',lw=0.5)
        minSpec = min(thisData_sample['Q_radiation']) * 0.999
        maxSpec = max(thisData_sample['Q_radiation']) * 1.05
        plt.ylim(minSpec, maxSpec)
        #plt.legend(['Bilger','Species','Z_st'])
        plt.title('Scatter plot at: x/D=' + str(round(float(location_dict[i]),1)))

        #write back the data to LESdata
        LESdata[scatterPlanes[i]] = thisData

        # plot the change in % due to radiation
        plt.figure(i + 10)
        Q_reduced = abs(thisData_sample['heatRelease'] - thisData_sample['Q_radiation'])
        thisData_sample['ratio'] = thisData_sample['Q_radiation'] / Q_reduced
        thisData_sample['ratio'].loc[thisData_sample['heatRelease']<5e7] = 0
        plt.scatter(thisData_sample['f_Sandia'], thisData_sample['ratio'], s=0.2, c='k')
        plt.xlabel('Mixture fraction')
        plt.ylabel('dQ [%]')
        #plt.xlim(0, 0.3)
        plt.xlim(0, max(thisData_sample['f_Sandia']))
        #plt.plot([Z_st,Z_st],[0,2500],'--',lw=0.5)
        minSpec = 0
        maxSpec = 10
        plt.ylim(minSpec, maxSpec)
        #plt.legend(['Bilger','Species','Z_st'])
        plt.title('Scatter plot at: x/D=' + str(round(float(location_dict[i]),1)))

    plt.show(block=False)


def compute_mol_fractions(thisData):

    assert type(thisData) == pd.DataFrame

    Nenner = [(thisData[f] / gas.molecular_weights[gas.species_index(f)]) for f in species]
    Nenner = sum(Nenner)

    thisData['x_CO'] = thisData['CO'] / gas.molecular_weights[gas.species_index('CO')] / Nenner
    thisData['x_CO2'] = thisData['CO2'] / gas.molecular_weights[gas.species_index('CO2')] / Nenner
    thisData['x_H2O'] = thisData['H2O'] / gas.molecular_weights[gas.species_index('H2O')] / Nenner
    thisData['x_CH4'] = thisData['CH4'] / gas.molecular_weights[gas.species_index('CH4')] / Nenner
    thisData['x_H2'] = thisData['CO'] / gas.molecular_weights[gas.species_index('H2')] / Nenner
    thisData['x_OH'] = thisData['OH'] / gas.molecular_weights[gas.species_index('OH')] / Nenner
    thisData['x_O2'] = thisData['O2'] / gas.molecular_weights[gas.species_index('O2')] / Nenner

    return thisData



