import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
import matplotlib.animation as animation
import tkinter


def return_15_fps(frames):
    i=0
    averages = np.zeros(shape=(1, 19800))
    for batch in range(1,frames.shape[0]+1):
        if batch % 100 == 0:
            i_rows =i*100
#             print(i_rows, batch)
            office_data_tmp = frames[i_rows:batch, :]
            df = pd.DataFrame(office_data_tmp).rolling(6).mean()
            df = df.iloc[::6, :]
    #         display(df)
            averages = np.append(averages, df.iloc[1:16,:].to_numpy(), axis=0)
            i+=1
#             print(averages.shape)
    return(averages[1:,:])


data_folder = "data/office_full/"
rolling = 100
office_data = np.loadtxt(data_folder + 'amplitude/amplitude01',delimiter=',')
averages_from_file = return_15_fps(office_data)

df = pd.DataFrame(office_data)
df_ma = pd.DataFrame(office_data).rolling(rolling).mean()
denoised = np.reshape((df.loc[rolling:,:]-df_ma.loc[rolling:,:]).to_numpy(),(df.loc[rolling:,:].shape[0],180,110))


office_data = np.reshape(denoised,(denoised.shape[0],180,110))
matplotlib.use('TkAgg')
ims = []
fig = plt.figure()
for i in range(5,600-rolling):
    im = plt.imshow(np.clip(abs(office_data[i, :, :]-office_data[i-1, :, :]), a_min=5, a_max=None))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                repeat_delay=1000)
plt.show()