#!/usr/bin/env python3
#import pdb
import time
import sqlite3
import com
import config
import sys

def save_stir_log(result):
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('insert into stir_log(stir_dt,result) values(datetime("now"),"' + str(result) + '")')
    conn.commit()
    conn.close()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Usage: stir nnn")
		print("where nnn is time in seconds")
		sys.exit()
	delay = int(sys.argv[1])
	print("Starting stir")
	ser = com.open_serial()
	com.send_command(ser, com.START_STIR_COMMAND, com.EMPTY_PARAMETER)
	a = com.poll(ser)
	print("Poll result = " + str(a))
	print("Waiting " + str(delay) + " seconds")
	time.sleep(delay)
	com.send_command(ser, com.STOP_STIR_COMMAND, com.EMPTY_PARAMETER)
	a = com.poll(ser)
	ser.close()
	print("Poll result = " + str(a))
	#pdb.set_trace()
	if a == com.OK_MESSAGE:
		print("All right")
	else:
		print("Error " + str(a))
	save_stir_log(a)

