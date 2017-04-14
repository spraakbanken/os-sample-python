#!/bin/sh

cd /var/lib/mysql

/opt/rh/rh-mysql57/root/usr/bin/mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < iotbuilddb.sql 
