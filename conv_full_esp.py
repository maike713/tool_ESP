import numpy as np

# conversion factor
# CF = 4 Pi epsilon_0 * a_0/e = e / E_h
CF = (1.6021766 * 10**(-19)) / (4.359745 * 10**(-18))

INPUT1 = 'qm_dftb_esp.xvg'
INPUT2 = 'esp_output'

# ESP in INPUT1 is with the wrong sign convention, so multiplied with -1
full_esp = ((np.loadtxt(INPUT1) * (-1)) + np.loadtxt(INPUT2, skiprows = 1)) *  CF
full_esp[:,0] = np.arange(0, len(full_esp[:,0] + 1))  # needed to preserve the time

np.save('esp_full.npy', full_esp)
np.savetxt('esp_full.txt', full_esp)

print('Full ESP written to file esp_full.npy and esp_full.txt')
