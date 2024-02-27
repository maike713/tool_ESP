import numpy as np
import math

# conversion factor
# cf = 4 Pi epsilon_0 * a_0/e = e / E_h
cf = (1.6021766 * 10**(-19)) / (4.359745 * 10**(-18))

input1 = 'qm_dftb_esp.xvg'
input2 = 'esp_output'

# ESP in input1 is with the wrong sign convention, so multiplied with -1
full_esp = ((np.loadtxt(input1) * (-1)) + np.loadtxt(input2, skiprows = 1)) *  cf
full_esp[:,0] = (full_esp[:,0] / cf) / 2
print(full_esp)

np.save('esp_full.npy', full_esp)
np.savetxt('esp_full.txt', full_esp)
