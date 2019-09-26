import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in data at x/D =1

LES_data = pd.read_csv( '/media/max/HDD2/HDD2_Data/OF4_Simulations/TNF_KIT/SuperMUC/case-05_ESF_linear/scatter/scatter_xD010.txt',sep='\t')

DNS_data = pd.read_csv('/home/max/Documents/05_DNS_Data/DNS_KIT/scatter/scatter_xD010.txt',sep='\t')

Exp_data = pd.read_csv('/home/max/Documents/10_Experimental_Data/TNF/02_ExpData/Dataset_2015/species-5GP-2015/FJ200-5GP-Lr75-57-xD010.csv')

print('\nLES data:')
print(LES_data.head())

print('\nDNS data:')
print(DNS_data.head())

print('\nExp data:')
print(Exp_data.head())

# shrink the data between 0.05 < Z < 0.06
LES_narrow = LES_data[(LES_data['f_Bilger']>0.05) &  (LES_data['f_Bilger']<0.06)]

DNS_narrow = DNS_data[(DNS_data['f_Bilger']>0.05) & (DNS_data['f_Bilger']<0.06)]

Exp_narrow = Exp_data[(Exp_data['Fblgr']>0.05) & (Exp_data['Fblgr']<0.06)]

# plot der T Verteilung

# %%

fig, (ax1, ax2,ax3) = plt.subplots(1, 3, figsize=(10,5))

bins = 20

#fig.suptitle('T histogram 0.05<Z<0.06')
ax1.hist(LES_narrow['T'],normed=True,bins=bins)
ax2.hist(DNS_narrow['T'],normed=True,bins=bins)
ax3.hist(Exp_narrow['Tray'],normed=True,bins=bins)

ax1.set_title('LES')
ax2.set_title('DNS')
ax3.set_title('Exp')

ax1.set_ylim([0,0.009])
ax2.set_ylim([0,0.009])
ax3.set_ylim([0,0.009])

ax1.set_ylabel('PDF')
ax1.set_xlabel('T [K]')
ax2.set_xlabel('T [K]')
ax3.set_xlabel('T [K]')
plt.savefig('Hist_T_0.05_Z_0.06.png')


fig, (ax1, ax2,ax3) = plt.subplots(1, 3, figsize=(10,5))

bins = 20

#fig.suptitle('T histogram 0.05<Z<0.06')
ax1.hist(LES_narrow['f_Bilger'],normed=True,bins=bins)
ax2.hist(DNS_narrow['f_Bilger'],normed=True,bins=bins)
ax3.hist(Exp_narrow['Fblgr'],normed=True,bins=bins)

ax1.set_title('LES')
ax2.set_title('DNS')
ax3.set_title('Exp')

# ax1.set_ylim([0,0.01])
# ax2.set_ylim([0,0.01])
# ax3.set_ylim([0,0.01])

ax1.set_ylabel('PDF')
ax1.set_xlabel('Z [-]')
ax2.set_xlabel('Z [-]')
ax3.set_xlabel('Z [-]')
plt.savefig('Hist_Z_0.05_Z_0.06.png')



fig, (ax1, ax2,ax3) = plt.subplots(1, 3, figsize=(10,5))

bins = 20

#fig.suptitle('T histogram 0.05<Z<0.06')
ax1.hist(LES_narrow['r_in_m']*1e3,normed=True,bins=bins)
ax2.hist(abs(DNS_narrow['rInmm']),normed=True,bins=bins)
ax3.hist(abs(Exp_narrow['xmm']),normed=True,bins=bins)

ax1.set_title('LES')
ax2.set_title('DNS')
ax3.set_title('Exp')

ax1.set_ylim([0,0.5])
ax2.set_ylim([0,0.5])
ax3.set_ylim([0,0.5])

ax1.set_ylabel('PDF')
ax1.set_xlabel('r [mm]')
ax2.set_xlabel('r [mm]')
ax3.set_xlabel('r [mm]')
plt.savefig('Hist_r_0.05_Z_0.06.png')


plt.show()