import numpy as np
import matplotlib.pyplot as plt

plt.style.use('tableau-colorblind10')

time = np.loadtxt('qm_dftb_esp.xvg')[:,0] + np.loadtxt('esp_output2', delimiter = ',')[:,0] * 0.5 / 1000
esp_CYS22 = np.loadtxt('qm_dftb_esp.xvg')[:,4] + np.loadtxt('esp_output2', delimiter = ',')[:,4] 
esp_CYS2  = np.loadtxt('qm_dftb_esp.xvg')[:,8] + np.loadtxt('esp_output2', delimiter = ',')[:,8] 
esp_CYS27 = np.loadtxt('qm_dftb_esp.xvg')[:,12] + np.loadtxt('esp_output2', delimiter = ',')[:,12] 

time1 = np.loadtxt('qm_dftb_esp.xvg')[:,0]
esp1_CYS22 = np.loadtxt('qm_dftb_esp.xvg')[:,4]
esp1_CYS2  = np.loadtxt('qm_dftb_esp.xvg')[:,8]
esp1_CYS27 = np.loadtxt('qm_dftb_esp.xvg')[:,12]


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex = True, figsize = (16,8))


ax1.plot(time, esp_CYS22, label = 'CYS22')
ax2.plot(time, esp_CYS2,  label = 'CYS2')
ax3.plot(time, esp_CYS27, label = 'CYS27')

ax1.plot(time1, esp1_CYS22, label = 'with correction')
ax2.plot(time1, esp1_CYS2,  label = 'with correction')
ax3.plot(time1, esp1_CYS27, label = 'with correction')

ax1.set_title('ESP of the S-Atoms of the respective Cystein')

ax1.set_ylabel('ESP')
ax2.set_ylabel('ESP')
ax3.set_ylabel('ESP')

ax3.set_xlabel('Time in ps')

ax1.legend(loc = 'upper left')
ax2.legend(loc = 'upper left')
ax3.legend(loc = 'upper left')

plt.show()
