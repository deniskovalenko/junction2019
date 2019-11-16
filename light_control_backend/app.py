from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import sys

from light_control_service import LightControlService

app = Flask(__name__)
CORS(app)
light_control = LightControlService(app.config)

@app.route('/')
def build_path():
    return "light control API. Send POST to /api/v1/set_light"


@app.route('/api/v1/get_state')
def deals():
    state = light_control.get_state()
    return jsonify(state)

@app.route('/api/v1/set_light', methods=['POST'])
def routes():
    print("got set light request")
    print(request.get_json())
    lightChangeRequest = request.get_json()
    res = light_control.set_light(lightChangeRequest)
    result = {"status": res, "current_state": light_control.get_state()}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8070)
