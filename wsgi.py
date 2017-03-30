from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime
import os
import re
import requests
import json
import random

user = os.environ["MYSQL_USER"]
passwd = os.environ["MYSQL_PASSWORD"]
dbhost = os.environ["MYSQL_SERVICE_HOST"]
dbname = os.environ["MYSQL_DATABASE"]

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = \
  'mysql://%s:%s@%s/%s' % (user, passwd, dbhost, dbname)

application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
bootstrap = Bootstrap(application)

class deviceDetails(db.Model):
  __tablename__ = 'deviceDetails'

# specify the column names here
  deviceId = db.Column(db.String(10), primary_key=True)
  make = db.Column(db.String(10))
  model = db.Column(db.String(16))
  function = db.Column(db.String(16))
  pm10Particles = db.Column(db.Integer)

  def __init__(self, deviceId, make, model, function, pm10Particles):
    self.deviceId = deviceId
    self.make = make
    self.model = model
    self.function = function
    self.pm10Particles = pm10Particles

  def __refr__(self):
    return '<deviceDetails %r>' % self.name


class deviceLocation(db.Model):
  __tablename__ = 'deviceLocation'

# specify the column names here
  deviceId = db.Column(db.String(10), primary_key=True)
  altitude = db.Column(db.String(10))
  latitude = db.Column(db.String(16))
  timestamp = db.Column(db.String(16))

  def __init__(self, deviceId, altitude, latitude, timestamp):
    self.deviceId = deviceId
    self.altitude = altitude
    self.latitude = latitude
    self.timestamp = timestamp

  def __refr__(self):
    return '<deviceLocation %r>' % self.name


class deviceStatus(db.Model):
  __tablename__ = 'deviceStatus'

# specify the column names here
  deviceId = db.Column(db.String(10), primary_key=True)
  pollutionLevel = db.Column(db.String(10))
  timestamp = db.Column(db.String(16))
  operationalState = db.Column(db.String(16))

  def __init__(self, deviceId, pollutionLevel, timestamp, operationalState):
    self.deviceId = deviceId
    self.pollutionLevel = pollutionLevel
    self.timestamp = timestamp
    self.operationalState = operationalState

  def __refr__(self):
    return '<deviceStatus %r>' % self.name


@application.route("/1/iotDeviceDetails/<deviceid>")
def details(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  query-rows = deviceDetails.query.filter(deviceDetails.deviceId==deviceid)
  row = query-rows.first()
  details = {"make":row.make, "model":row.model,
	     "function":row.function, "pm10Particles":row.pm10Particles}
  return jsonify({"iotDeviceDetails":details})

@application.route("/1/iotLocationDetails/<deviceid>")
def location(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  query-rows = deviceLocation.query.filter(deviceLocation.deviceId==deviceid)
  row = query-rows.first()
  details = {"altitude":row.altitude, "latitude":row.latitude,
	     "longitude":row.longitude, "timestamp":row.timestamp}
  return jsonify({"iotLocationDetails":details})

@application.route("/1/iotDeviceStatus/<deviceid>")
def status(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  query-rows = deviceStatus.query.filter(deviceStatus.deviceId==deviceid)
  row = query-rows.first()
  details = {"pollutionLevel":row.pollutionLevel, "timestamp":row.timestamp, "operationalState":row.operationalState}
  return jsonify({"iotDeviceStatus":details})

@application.route("/1/iotDeviceEvent", methods=["POST"])
def event():
  #post request including the deviceid and a notifyURL
  deviceId = request.form['deviceId']
  url = request.form['notifyURL']
  states = ["Red", "Amber", "Green"]
  timestamp = unicode(datetime.now()).partition('.')[0]
  details = {"pollutionRange":random.choice(states), "timestamp":timestamp}
  d2 = json.dumps({"iotPollutionStatus":details})
  r = requests.post(url, data=d2)
  return d2, 201

if __name__ == "__main__":
  application.run(debug=True)

