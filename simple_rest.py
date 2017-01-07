#!/usr/bin/env python

"""
REST API for controling RGB Led Strips/Bulbs
"""

import os
import sys
import time
this_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_folder)
from flux_led import WifiLedBulb

from flask import Flask, jsonify, request
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class ControlRGB(Resource):
    def post(self):
        json_data = request.get_json()
        print (json_data)
        ip_addr = json_data['ip_address']

        bulb = WifiLedBulb(ip_addr)
        if 'red' in json_data:
            red = int(json_data['red'])
            green = int(json_data['green'])
            blue = int(json_data['blue'])
            if not bulb.isOn():
                bulb.turnOn()
            bulb.setRgb(red,green,blue)
            time.sleep(1)
            bulb.update_state()
            return {"bulb":str(bulb)}
        if 'state' in json_data:
            if 'on' in json_data['state']:
                print ("Turning On")
                bulb.turnOn()
            else:
                bulb.turnOff()
            time.sleep(1)
            bulb.update_state()
            return {"bulb":str(bulb)}

api.add_resource(ControlRGB, '/controlRGB')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5444 ,debug=True)
