from flask import Flask, request, jsonify
from datetime import datetime
import re
import requests
import json
import random

application = Flask(__name__)

@application.route("/1/iotDeviceDetails/<deviceid>")
def details(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  details = {"make":"Siemens", "model":"Air Monitor S3rJ",
	     "function":"Air Pollution Monitor", "pm10Particles":"12"}
  return jsonify({"iotDeviceDetails":details})

@application.route("/1/iotLocationDetails/<deviceid>")
def location(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  timestamp = datetime.now()
  details = {"altitude":"1001.0", "latitude":"-80.86302",
	     "longitude":"41.277306", "timestamp":timestamp}
  return jsonify({"iotLocation":details})

@application.route("/1/iotDeviceStatus/<deviceid>")
def status(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  levels = ["Red", "Amber", "Green"]
  timestamp = datetime.now()
  details = {"pollutionLevel":random.choice(levels), "timestamp":timestamp}
  return jsonify({"iotDeviceStatus":details})

@application.route("/1/iotDeviceEvent", methods=["POST"])
def event():
  #post request including the deviceid and a notifyURL
  did = request.form['deviceId']
  url = request.form['notifyURL']
  states = ["Up", "Down", "Maintenance", "Undetermined"]
  timestamp = unicode(datetime.now()).partition('.')[0]
  details = {"operationalState":random.choice(states), "timestamp":timestamp}
  d2 = json.dumps({"iotDeviceStatus":details})
  r = requests.post(url, data=d2)
  return d2, 201

if __name__ == "__main__":
  application.run(debug=True)
