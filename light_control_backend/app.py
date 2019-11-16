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


@app.route('/deals')
def deals():
    deals = deals_service.getPipeDriveDeals()
    return jsonify(deals)

@app.route('/api/v1/set_light', methods=['POST'])
def routes():
    lightChangeRequest = request.get_json()
    res = light_control.set_light(lightChangeRequest)

    return jsonify(routeInfo)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
