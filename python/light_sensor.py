#!/usr/bin/env python3

#import pdb
import sqlite3
import com
import config

class light_sensor():
    def __init__(this,serial_object):
        this.ser = serial_object
    def read(this):
        light = 0
        com.send_command(this.ser, com.READ_LIGHT_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser) # LIGHT 25.52
        light = int(a[6:])
        return light
    def save_log(this, light):
        conn = sqlite3.connect(config.DBPATH)
        c = conn.cursor()
        c.execute('insert into light_log(light_dt,light) values(datetime("now"),' + str(light) + ')')
        conn.commit()
        conn.close()
