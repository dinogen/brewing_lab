#import pdb
import time
import sqlite3
import com
import config

class stirrer:
    def __init__(this,serial_object):
        this.ser = serial_object
    def start(this):
        com.send_command(this.ser, com.START_STIR_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
    def stop(this):
        com.send_command(this.ser, com.STOP_STIR_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
    def stir_for_n_seconds(this,n):
        if this.start():
            time.sleep(n)
            if this.stop():
                return com.OK_MESSAGE
        return "KO"
    def save_log(this,result):
        conn = sqlite3.connect(config.DBPATH)
        c = conn.cursor()
        c.execute('insert into stir_log(stir_dt,result) values(datetime("now"),"' + str(result) + '")')
        conn.commit()
        conn.close()
