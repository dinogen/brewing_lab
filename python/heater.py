#import pdb
import com
import config
import sqlite3


class heater:
    def __init__(this,serial_object):
        this.ser = serial_object
    def turn_on(this):
        com.send_command(this.ser, com.START_HEAT_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
    def turn_off(this):
        com.send_command(this.ser, com.STOP_HEAT_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
    def save_log(this,status):
        conn = sqlite3.connect(config.DBPATH)
        c = conn.cursor()
        c.execute('insert into heat_log(heat_dt,status) values(datetime("now"),' + str(status) + ')')
        conn.commit()
        conn.close()
