import numpy as np

# conversion factor
# CF = E_h / e
CF = (4.359745 * 10**(-18)) / (1.6021766 * 10**(-19))

INPUT1 = 'qm_dftb_esp.xvg'
INPUT2 = 'esp_output'

# ESP in INPUT1 is given in Volts
# ESP in INPUT2 is given in atomic units, conversion to Volt with CF
full_esp = np.loadtxt(INPUT1) + (np.loadtxt(INPUT2, skiprows=1) * CF)
full_esp[:,0] = np.arange(0, len(full_esp[:,0] + 1))  # needed to preserve the time

np.save('esp_full.npy', full_esp)
np.savetxt('esp_full.txt', full_esp)

print('Full ESP written to file esp_full.npy and esp_full.txt')
