### Created by Helvar - Nov, 2019
# Standard module imports
import base64
import json
# 3rd Party module imports
import numpy as np
from plotly import graph_objs as go


class Luminaire:
    def __init__(self, x0, y0, x1, y1,):
        self.device = dict(
            type="rect",
            xref="x",
            yref="y",
            line=dict(
                color="Black",
                width=1,
            ),
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            fillcolor=f'hsla(55, 100%, {50}%, {0.8})',
        )

    def update(self, b, t,):
        t = 50 + (np.clip(t, 0.0, 1.0) * 50)
        b = np.clip(b, 0, 0.95)
        self.device['fillcolor'] = f'hsla(55, 100%, {t}%, {b})'


class Simulator:
    def __init__(self, speed=None, env='garage'):
        if env == 'garage':
            self.__BG_PATH = 'assets/garage.png'
            self.__INIT_PARAMS = 'assets/garage.json'
            self.__IMG_WIDTH = 1466
            self.__IMG_HEIGHT = 1706
        elif env == 'meeting':
            self.__BG_PATH = 'assets/meeting_room.png'
            self.__INIT_PARAMS = 'assets/meeting_room.json'          
            self.__IMG_WIDTH = 740
            self.__IMG_HEIGHT = 415
        self.__speed = speed if speed else 500
        with open(self.__BG_PATH, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        self.__init_figure(bg_img="data:image/png;base64," + encoded_string)
        self.__parse_luminaires()
        self.__create_labels()

    def __init_figure(self, bg_img):
        # Initialise empty figure members
        data, layout, frames = [], dict(), []

        # Set bounds by visualizing an emtpy scatter plot
        data.append({
            'type': 'scatter',
            'x': [0, self.__IMG_WIDTH],
            'y': [0, self.__IMG_HEIGHT],
            'mode': 'markers',
            'marker_opacity': 0
        })
        layout['width'] = self.__IMG_WIDTH
        layout['height'] = self.__IMG_HEIGHT
        layout['xaxis'] = {'visible': False, 'showgrid': False}
        layout['yaxis'] = {'visible': False, 'showgrid': False}
        layout['images'] = [{
            'source': bg_img,
            'x': 0,
            'y': self.__IMG_HEIGHT,
            'xref': 'x',
            'yref': 'y',
            'sizex': self.__IMG_WIDTH,
            'sizey': self.__IMG_HEIGHT,
            'sizing': 'stretch',
            'layer': 'below',
            'opacity' : 1.0,
        }]
        layout['updatemenus'] = [{
            'type': 'buttons',
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": self.__speed, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 50,
                                                                        "easing": "linear"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ]
        }]
        self.__figure_dict = {
            'data': data,
            'layout': layout,
            'frames': frames,
        }

    def __parse_luminaires(self,):
        self.luminaires = dict()
        with open(self.__INIT_PARAMS) as f:
            params = json.loads(f.read())
        for k, v in params.items():
            self.luminaires[k] = Luminaire(*v.values())
        self.__figure_dict['layout']['shapes'] = [
            item.device for item in self.luminaires.values()]

    def __create_labels(self,):
        self.__figure_dict['layout']['annotations'] = [{
            'text': k,
            'x': (v.device['x0'] + v.device['x1']) / 2,
            'y': (v.device['y0'] + v.device['y1']) / 2,
            'showarrow': False,
        } for k, v in self.luminaires.items()]

    def populate_data(self, frames):
        for frame in frames:
            shapes = []
            if len(frame) > 0:
                for k, v in frame.items():
                    self.luminaires[k].update(b=v['b'], t=v['t'])
                    shapes.append(self.luminaires[k].device)
            else:
                shapes = [v.device for k, v in self.luminaires.items()]
            self.__figure_dict['frames'].append({
                'layout': {
                    'shapes' : shapes
                }
            })

    def run(self,):
        fig = go.Figure(self.__figure_dict)
        fig.show(renderer="browser")

if __name__ == '__main__':
    # Randomly choose luminaires and change their light parameters for N time samples.
    simulatorRefObj = Simulator(speed=500, env='meeting')
    size_L = len(simulatorRefObj.luminaires)
    N = 100
    frames = []
    for i in range(N):
        frame = dict()
        # Randomly pick a subset of luminaires to change for each time instance
        for j in range(np.random.randint(0, size_L)):
            # You should specify a luminaire based on the output from your radar algorithm.
            # You can set the brightness and temperature however you like.
            curr_device = np.random.choice(list(simulatorRefObj.luminaires.keys()))
            b, t = (np.random.random_sample() for _ in range(2))

            frame[curr_device] = {
                        'b' : b,
                        't' : t
                }
        frames.append(frame)
    
    # Run below code to generate a plotly HTML animation page
    simulatorRefObj.populate_data(frames)
    simulatorRefObj.run()

