import numpy as np
import matplotlib.pyplot as plt
import math

plt.style.use('tableau-colorblind10')

# conversion factor and * (-1) to get right sign convention
# cf = 4 Pi epsilon_0 * a_0/e = e / H
cf = (1.6021766 * 10**(-19)) / (4.359745 * 10**(-18)) * (-1)

time = np.loadtxt('qm_dftb_esp.xvg')[:,0] * 0.5 / 1000
esp_CYS22 = np.loadtxt('qm_dftb_esp.xvg')[:,4]
esp_CYS2  = np.loadtxt('qm_dftb_esp.xvg')[:,8]
esp_CYS27 = np.loadtxt('qm_dftb_esp.xvg')[:,12]

corr_22 = np.loadtxt('esp_output', skiprows = 1)[:,4]
corr_2  = np.loadtxt('esp_output', skiprows = 1)[:,8]
corr_27 = np.loadtxt('esp_output', skiprows = 1)[:,12]


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex = True, figsize = (16,8))


ax1.plot(time, esp_CYS22 * cf, label = 'CYS22')
ax2.plot(time, esp_CYS2 * cf,  label = 'CYS2')
ax3.plot(time, esp_CYS27 * cf, label = 'CYS27')

ax1.plot(time, esp_CYS22 + corr_22, label = 'with correction')
ax2.plot(time, esp_CYS2,  label = 'with correction')
ax3.plot(time, esp_CYS27, label = 'with correction')

ax1.set_title('ESP of the S-Atoms of the respective Cystein')

ax1.set_ylabel('ESP')
ax2.set_ylabel('ESP')
ax3.set_ylabel('ESP')

ax3.set_xlabel('Time in ps')

ax1.legend(loc = 'upper left')
ax2.legend(loc = 'upper left')
ax3.legend(loc = 'upper left')

plt.show()
