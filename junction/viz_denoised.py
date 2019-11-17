import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
import matplotlib.animation as animation
import tkinter
import requests
import time

def return_15_fps(frames):
    i = 0
    averages = np.zeros(shape=(1, 19800))
    for batch in range(1, frames.shape[0] + 1):
        if batch % 100 == 0:
            i_rows = i * 100
            #             print(i_rows, batch)
            office_data_tmp = frames[i_rows:batch, :]
            df = pd.DataFrame(office_data_tmp).rolling(6).mean()
            df = df.iloc[::6, :]
            #         display(df)
            averages = np.append(averages, df.iloc[1:16, :].to_numpy(), axis=0)
            i += 1
    #             print(averages.shape)
    return (averages[1:, :])


data_folder = "data/"

# hyperparameters to tune
rolling = 15
min_amplitude = 90

office_data = np.loadtxt(data_folder + 'demo_short.txt', delimiter=',')
print(office_data.shape)
# office_data = return_15_fps(office_data)
print(office_data.shape)
df = pd.DataFrame(office_data)
print("original df shape" + str(df.shape))
df_ma = pd.DataFrame(office_data).rolling(rolling).mean()
print("rolling df shape" + str(df_ma.shape))
# office_data = np.reshape((df.loc[rolling:,:]-df_ma.loc[rolling:,:]).to_numpy(),(df.loc[rolling:,:].shape[0],180,110)) # remove avg images - no background noize kind
office_data = np.reshape(office_data, (office_data.shape[0], 180, 110))

def report_people(number):
    if number==0:
        light = 5
        temperature = 6500
    elif number==1:
        light = 20
        temperature = 5750
    elif number==2:
        light = 30
        temperature = 4850
    else:
        light = 40
        temperature = 3450
    requests.post('http://10.100.15.151:8070/api/v1/set_light', json={"device_id": "EC22",
                                                                      "type": "light",
                                                                      "user": "radar_human_detection",
                                                                  "settings": {"light_level_value": light,
                                                                               "color_temperature_value": temperature}})


print(office_data.shape)
matplotlib.use('TkAgg')
ims = []
fig = plt.figure()
for i in range(rolling, office_data.shape[0]):
    # im = plt.imshow(np.clip(abs(office_data[i, :, :]-office_data[i-1, :, :]), a_min=0, a_max=None))
    original_frame = office_data[i, :, :]
    frame_transposed_flipped = np.flip(np.transpose(original_frame))
    details_removed = frame_transposed_flipped
    details_removed = np.clip(frame_transposed_flipped, a_min=frame_transposed_flipped.max()-15, a_max=None) #to remove not intense pixels
    im = plt.imshow(details_removed)
    ims.append([im])

    if i % 10 == 0:
        b = sum(pd.DataFrame(original_frame).max().diff() / pd.DataFrame(original_frame).max() > 0.13)
        report_people(b)
        print('Detected humans:', b)
        time.sleep(1)

ani = animation.ArtistAnimation(fig, ims, interval=30, blit=True, repeat=False)
# repeat_delay=1000)
plt.show()

