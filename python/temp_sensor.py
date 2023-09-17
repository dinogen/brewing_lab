#!/usr/bin/env python3

#import pdb
import sqlite3
import com
import config
import time

class temp_sensor():
    def __init__(this,serial_object):
        this.ser = serial_object
    def read(this,sensor_id):
        temp = 99.0
        par =  "{0:04}".format(sensor_id).encode()
        com.send_command(this.ser, com.READ_TEMP_COMMAND, par)
        a = com.poll(this.ser) # TEMP 25.52
        temp = float(a[5:])
        return temp
    def save_log(this,sensor_id, temp,temp_dt=None):
        if temp_dt == None:
            temp_dt = time.gmtime()
        temp_string = time.strftime("%Y-%m-%d %H:%M:%S",temp_dt)
        conn = sqlite3.connect(config.DBPATH)
        c = conn.cursor()
        c.execute("insert into temp_log(temp_dt,sensor_id,temp) values('{}',{},{})".format(temp_string, sensor_id, temp))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    t = temp_sensor(None)
    t.save_log(9, 99,time.gmtime())


