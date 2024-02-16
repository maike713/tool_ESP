import numpy as np
import matplotlib.pyplot as plt
import math

plt.style.use('tableau-colorblind10')

input_file = 'esp_full.txt'

time = np.loadtxt(input_file)[:,0] * 160 / 1000
esp_22 = np.loadtxt(input_file, usecols = 4)
esp_2  = np.loadtxt(input_file, usecols = 8)
esp_27 = np.loadtxt(input_file, usecols = 12)

window_size = 50
kernel = np.ones(window_size) / window_size
esp_22_ma = np.convolve(esp_22, kernel, mode = 'valid')
esp_2_ma = np.convolve(esp_2, kernel, mode = 'valid')
esp_27_ma = np.convolve(esp_27, kernel, mode = 'valid')


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex = True, figsize = (16,8))

ax1.plot(time, esp_22, alpha = 0.5, label = 'CYS22')
ax2.plot(time, esp_2,  alpha = 0.5, label = 'CYS2')
ax3.plot(time, esp_27, alpha = 0.5, label = 'CYS27')

ax1.plot(time[window_size-1:], esp_22_ma, label = 'Moving Average')
ax2.plot(time[window_size-1:], esp_2_ma, label = 'Moving Average')
ax3.plot(time[window_size-1:], esp_27_ma, label = 'Moving Average')

ax1.set_title('ESP of the S-Atoms of the respective Cystein')

ax1.set_ylabel('ESP in Volt')
ax2.set_ylabel('ESP in Volt')
ax3.set_ylabel('ESP in Volt')

ax3.set_xlabel('Time in ps')

ax1.legend(loc = 'upper left')
ax2.legend(loc = 'upper left')
ax3.legend(loc = 'upper left')

plt.show()
