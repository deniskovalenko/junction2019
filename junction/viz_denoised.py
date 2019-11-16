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


data_folder = "data/"
rolling = 15
office_data = np.loadtxt(data_folder + 'demo_short.txt', delimiter=',')
print(office_data.shape)
# office_data = return_15_fps(office_data)
print(office_data.shape)
df = pd.DataFrame(office_data)
print("original df shape" + str(df.shape))
df_ma = pd.DataFrame(office_data).rolling(rolling).mean()
print("rolling df shape" + str(df_ma.shape))
# office_data = np.reshape((df.loc[rolling:,:]-df_ma.loc[rolling:,:]).to_numpy(),(df.loc[rolling:,:].shape[0],180,110))
office_data = np.reshape(office_data,(office_data.shape[0],180,110))

print(office_data.shape)
matplotlib.use('TkAgg')
ims = []
fig = plt.figure()
for i in range(rolling, office_data.shape[0]):
    # im = plt.imshow(np.clip(abs(office_data[i, :, :]-office_data[i-1, :, :]), a_min=0, a_max=None))
    details_removed = np.clip(office_data[i, :, :], a_min=0, a_max=None)
    details_removed = np.clip(details_removed[:, :], a_min=90, a_max=None)
    im = plt.imshow(details_removed)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=38, blit=True, repeat=False)
                                # repeat_delay=1000)
plt.show()