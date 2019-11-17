import numpy as np
import atexit
import sys
import cv2
import time
from rabbitmq import Subscriber
import Vtt60Processed.Sample as Vtt60Processed
import pandas as pd
import requests


class Streamer60():
    def __init__(self,url='10.84.110.2',topic='radar60',only_latest=False):

        self.url = url
        self.topic = topic
        self.only_latest = only_latest
        self.samples_in_total = 0
        self.fps = 30
        self.startTime = time.time()
        cv2.namedWindow('junction',cv2.WINDOW_NORMAL)

        # connect to RabbitMQ topic
        self.subscriber = Subscriber(self.url)
        self.subscriber.subscribe(self.topic, self.process_sample, only_latest=self.only_latest)
        atexit.register(self.exit)
        try:
            self.subscriber.run()
        except KeyboardInterrupt:
            pass
            
    def deserialize_vtt_60_processed(self,sample):
        """Deserialize raw data and config dictionary. 
        Return None is case of failure"""
        try:
            deserialized_sample = Vtt60Processed.Sample.GetRootAsSample(sample, 0)
        except Exception:
            return None
        sample_dict = {}
        sample_dict['amplitude']  = deserialized_sample.AmplitudeAsNumpy()
        sample_dict['angle'] = deserialized_sample.AngleAsNumpy()
        self.samples_in_total += 1
        return sample_dict

    def report_people(self, number):
        if number == 0:
            light = 5
            temperature = 6500
        elif number == 1:
            light = 20
            temperature = 5750
        elif number == 2:
            light = 30
            temperature = 4850
        else:
            light = 40
            temperature = 3450
        requests.post('http://10.100.15.151:8070/api/v1/set_light', json={"device_id": "EC22",
                                                                          "type": "brightness",
                                                                          "user": "radar_human_detection_live",
                                                                          "settings": {"light_level_value": light,
                                                                                       "color_temperature_value": temperature}})

    def process_sample(self, ch, method, properties, body):
        """Process a single sample from radar"""

        # data inside a dictionary
        # {'amplitude':[1.3,4.4,5...],
        # 'angle': [0.04,0.1,...]}
        sample_dict = self.deserialize_vtt_60_processed(body)

        with open('sample_2.txt', 'a') as f:
            x_arrstr = np.char.mod('%d', sample_dict['amplitude'])

            # x_arrstr -> should be 2d array "frame".
            raw_data = ",".join(x_arrstr.flatten())
            f.write(raw_data)
            f.write('\n')

            arr = np.array(sample_dict['amplitude'])

            frame = np.reshape(arr, (180,110))
            frame_transposed_flipped = np.flip(np.transpose(frame))
            frame_transposed_flipped = np.flip(np.transpose(frame))
            details_removed = frame_transposed_flipped
            details_removed = np.clip(frame_transposed_flipped, a_min=frame_transposed_flipped.max() - 15, a_max=None)
            b = sum(pd.DataFrame(frame).max().diff() / pd.DataFrame(frame).max() > 0.13)
            self.report_people(b)


        if body is None or sample_dict is None:
            print('Stream stopped.')
            return
        if self.samples_in_total % self.fps == 0:
            endTime = time.time()
            print('FPS: {:.1f}'.format(self.fps/(endTime - self.startTime)))
            self.startTime = endTime
        
        # your code here
        amplitude = sample_dict['amplitude']
        amplitude = np.reshape(amplitude,(180,110))
        amplitude = np.where(amplitude>130,130,amplitude)
        amplitude = np.uint8(255*amplitude/130)
        out = cv2.cvtColor(amplitude,cv2.COLOR_GRAY2BGR)
        out = cv2.applyColorMap(out,cv2.COLORMAP_MAGMA)
        cv2.imshow('junction',out)
        cv2.waitKey(10)



    def exit(self):
        """Perform actions before exit"""
        cv2.destroyAllWindows()
        print("Exiting..")

def main():
    """Start Streamer"""
    viewer = Streamer60()

if __name__ == '__main__':
    main()
