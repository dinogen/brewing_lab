#!/usr/bin/env python3
#import pdb
import time
import com
import config
import sys



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: heat on|off")
        sys.exit()
    onoff = sys.argv[1]
    print("Setting heat " + onoff)
    ser = com.open_serial()
    if onoff == "on":
        com.send_command(ser, com.START_HEAT_COMMAND, com.EMPTY_PARAMETER)
    else:
        com.send_command(ser, com.STOP_HEAT_COMMAND, com.EMPTY_PARAMETER)
    a = com.poll(ser)
    ser.close()
    print("Poll result = " + str(a))

