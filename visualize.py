import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
import matplotlib.animation as animation
import tkinter

data_folder = "data/meeting/office_full/"
office_data = np.loadtxt(data_folder + 'amplitude/amplitude01',delimiter=',')
office_data = np.reshape(office_data,(office_data.shape[0],180,110))
matplotlib.use('TkAgg')
ims = []
fig = plt.figure()
for i in range(600):
    im = plt.imshow(office_data[i, :, :])
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=16, blit=True,
                                repeat_delay=1000)
plt.show()
