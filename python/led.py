#!/usr/bin/env python3
#import pdb
import time
import sqlite3
import com
import config

class led:
    def __init__(this,serial_object):
        this.ser = serial_object
    def turn_on(this):
        brightness = 250
        par =  "{0:04}".format(brightness).encode()
        com.send_command(this.ser, com.START_LED_COMMAND, par)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
    def turn_off(this):
        com.send_command(this.ser, com.STOP_LED_COMMAND, com.EMPTY_PARAMETER)
        a = com.poll(this.ser)
        if a == com.OK_MESSAGE:
            return True
        else:
            return False
   


