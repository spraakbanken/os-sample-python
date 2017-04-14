DROP TABLE IF EXISTS deviceDetails;
DROP TABLE IF EXISTS deviceLocation;
DROP TABLE IF EXISTS deviceStatus;
DROP TABLE IF EXISTS callbacks;

CREATE TABLE deviceDetails(
deviceId VARCHAR(10) NOT NULL,
make VARCHAR(20) NOT NULL,
model VARCHAR(20) NOT NULL,
function VARCHAR(30) NOT NULL,
pm10Particles int NOT NULL,
PRIMARY KEY (deviceId)
);

CREATE TABLE deviceLocation(
deviceId VARCHAR(10) NOT NULL,
altitude VARCHAR(20) NOT NULL,
longitude VARCHAR(20) NOT NULL,
latitude VARCHAR(20) NOT NULL,
timestamp VARCHAR(30) NOT NULL,
PRIMARY KEY (deviceId)
);

CREATE TABLE deviceStatus(
deviceId VARCHAR(10) NOT NULL,
pollutionLevel VARCHAR(10) NOT NULL,
timestamp VARCHAR(30) NOT NULL,
operationalState VARCHAR(10) NOT NULL,
PRIMARY KEY (deviceId)
);

CREATE TABLE callbacks(
deviceId VARCHAR(10) NOT NULL,
url VARCHAR(256) NOT NULL,
PRIMARY KEY (deviceId, url)
);

INSERT INTO deviceDetails (deviceId, make, model, function, pm10Particles)
VALUES ('1234', 'Fujitsu', 'PM403-Monitor', 'Monitor Pollution Levels', 43);

INSERT INTO deviceLocation (deviceId, altitude, longitude, latitude, timestamp)
VALUES ('1234', '100', '-80.86302', '41.277306', '2017-01-04T02:51:39.000Z');

INSERT INTO deviceStatus (deviceId, pollutionLevel, timestamp, operationalState)
VALUES ('1234', 'Green', '2017-01-04T02:51:39.000Z', 'Up');
