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
  longitude = db.Column(db.String(16))
  latitude = db.Column(db.String(16))
  timestamp = db.Column(db.String(16))

  def __init__(self, deviceId, altitude, longitude, latitude, timestamp):
    self.deviceId = deviceId
    self.altitude = altitude
    self.longitude = longitude
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

class callbacks(db.Model):
  __tablename__ = 'callbacks'

# specify the column names here
  deviceId = db.Column(db.String(10), primary_key=True)
  url = db.Column(db.String(256), primary_key=True)

  def __init__(self, deviceId, url):
    self.deviceId = deviceId
    self.url = url

  def __refr__(self):
    return '<callbacks %r>' % self.name


@application.route("/1/iotDeviceDetails/<deviceid>")
def details(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  queryrows = deviceDetails.query.filter(deviceDetails.deviceId == deviceid)
  row = queryrows.first()
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
  queryrows = deviceLocation.query.filter(deviceLocation.deviceId==deviceid)
  row = queryrows.first()
  details = {"altitude":row.altitude, "longitude":row.longitude,
	     "latitude":row.latitude, "timestamp":row.timestamp}
  return jsonify({"iotLocationDetails":details})

@application.route("/1/iotDeviceStatus/<deviceid>")
def status(deviceid):
  pattern = re.compile("^\d\d\d\d$")
  if not pattern.match(deviceid):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
  queryrows = deviceStatus.query.filter(deviceStatus.deviceId==deviceid)
  row = queryrows.first()
  details = {"pollutionLevel":row.pollutionLevel, "timestamp":row.timestamp, "operationalState":row.operationalState}
  return jsonify({"iotDeviceStatus":details})

@application.route("/1/iotDeviceEvent", methods=["POST"])
def event():
  #post request including the deviceid and a notifyURL
  deviceId = request.form['deviceId']
  url = request.form['notifyURL']

  # Need to check that the deviceID exists in the DB
  row = deviceStatus.query.filter(deviceStatus.deviceId==deviceId).first()
  if row is None:
    response = jsonify({'error': 'deviceId not found'})
    response.status_code = 404 # check if this is a valid response code
    return response

  # Add the notify URL into a table  to iterate and update on a change
  callback = callbacks(deviceId, url)
  db.session.add(callback)
  db.session.commit()
  
  # Send a post request to the callback URL
  details = {"deviceId":deviceId, "pollutionLevel":row.pollutionLevel, "timestamp":row.timestamp}
  r = requests.post(url, json=details)
  return jsonify(details), 201

@application.route("/buttonpress")
def press():
  # This is called when the 1btn is pressed
  # It updates the timestamp and state for the dID of 1234
  timestamp = unicode(datetime.now()).partition('.')[0]
  states = ["Red", "Amber", "Green"]
  row = deviceStatus.query.filter(deviceStatus.deviceId=="1234").first()

  # remove the existing state from the states list
  states.remove(row.pollutionLevel)
  print states

  row.timestamp = timestamp
  row.pollutionLevel = random.choice(states)
  db.session.commit()

  # post the changes to the registered URLs
  details = {"deviceId":"1234", "pollutionLevel":row.pollutionLevel, "timestamp":row.timestamp}

  urlRows =  callbacks.query.filter(callbacks.deviceId=="1234")
  for urlrow in urlRows:
    r = requests.post(urlrow.url, json=details)

  return jsonify({"ButtonPress":"Success"})



if __name__ == "__main__":
  application.run(debug=True)

