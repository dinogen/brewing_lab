#!/usr/bin/env python3

#import pdb
import time
import sqlite3
import com
import config
import sys

def read_temp(sensor_id):
    print("Starting reading temp")
    ser = com.open_serial()
    temp = 99
    par =  "{0:04}".format(sensor_id).encode()
    com.send_command(ser, com.READ_TEMP_COMMAND, par)
    a = com.poll(ser) # TEMP 25.52
    ser.close()
    print("a= " + str(a))
    temp = float(a[5:])
    return temp



def save_temp_log(sensor_id, temp):
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('insert into temp_log(temp_dt,sensor_id,temp) values(datetime("now"),' + str(sensor_id) + ',' + str(temp) + ')')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: checktemp nnn")
        print("where nnn is the sensor id")
        sys.exit()
    #pdb.set_trace()
    sensor_id = int(sys.argv[1])
    temp = read_temp(sensor_id)
    print("temperature of sensor " + str(sensor_id) + " = " + str(temp))

    save_temp_log(sensor_id,temp)

