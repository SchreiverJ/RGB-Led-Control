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

import json

app = Flask(__name__)
api = Api(app)


def hexToInt(hex):
    return int(hex, 16)

def colorToHex(c):
    h =  "#%6x" % ((c[0] << 16) + (c[1] << 8) + c[2] )
    return h.replace(' ','0')

def getBulb():
    ip_addr = '192.168.116.53'
    return WifiLedBulb(ip_addr)

def setState(bulb, json_data):
    
    if 'red' in json_data:
        red = int(json_data['red'])
        green = int(json_data['green'])
        blue = int(json_data['blue'])

        if not bulb.isOn():
            bulb.turnOn()
            time.sleep(.1)
            bulb.update_state()
        bulb.setRgb(red,green,blue)
        time.sleep(.1)
        bulb.update_state()
        
    if 'state' in json_data:
        if 'on' in json_data['state']:
            bulb.turnOn()
        else:
            bulb.turnOff() 
        time.sleep(.1)
        bulb.update_state()

    return bulb

def getBulbState(bulb):
    c = bulb.getRgb()
    print colorToHex(c)

    state = 'off'
    if bulb.isOn():
        state = 'on'
    d = {"color":colorToHex(c),"state":state}
    return json.dumps(d)


@app.route("/on")
def on():
    dict = {}
    dict['state'] = 'on'               
    bulb = getBulb()
    setState(bulb, dict)
    return getBulbState(bulb)

@app.route("/off")
def off():
    dict = {}
    dict['state'] = 'off'
    bulb = getBulb()
    setState(bulb, dict)
    return getBulbState(bulb)

@app.route("/poll")
def poll():
    bulb = getBulb()
    return getBulbState(bulb)

@app.route("/macros/getData")
def getData():
    bulb = getBulb()
    return getBulbState(bulb)
    

@app.route("/macros/set")
def set():
    color = request.args.get('color')
    dict = {}
    dict['red'] = hexToInt(color[0:2])
    dict['green'] = hexToInt(color[2:4])
    dict['blue'] = hexToInt(color[4:6])
    bulb = getBulb()
    setState(bulb, dict)
    return getBulbState(bulb)

#For having buttons flip individual colors
def toggleColor(color):
    bulb = getBulb()
    bulb.update_state()
    if bulb.isOn():
        c = bulb.getRgb()
    else:
        c = (0,0,0)
    dict = {}
    
    dict['red'] = c[0]
    dict['green'] = c[1]
    dict['blue'] = c[2]
    if dict[color] > 127:
        dict[color] = 0
    else:
        dict[color] = 255
    if dict['red'] == 0 and dict['green'] == 0 and dict['blue'] == 0:
        dict['state'] = 'off'

    setState(bulb, dict)
    return getBulbState(bulb)


@app.route("/macros/toggle")
def toggle():
    color = request.args.get('color')
    return toggleColor(color)

@app.route("/macros/button")
def buttonPressed():
    num = request.args.get('num')
    if num == '0':
        return toggleColor('red')
    if num == '1':
        return toggleColor('green')
    if num == '2':
        return toggleColor('blue')
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000 ,debug=True)
