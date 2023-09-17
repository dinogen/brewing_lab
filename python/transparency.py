#!/usr/bin/env python3
#import pdb
import time
import sqlite3
import com
import config
import sys

def save_transparency_log(result):
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('insert into transparency_log(transp_dt,result) values(datetime("now"),"' + str(result) + '")')
    conn.commit()
    conn.close()

if __name__ == "__main__":
	print("Starting reading transparency")
	ser = com.open_serial()#!/usr/bin/env python3

	light_total = 0;
	for i in range(10):
		com.send_command(ser, com.READ_LIGHT_COMMAND, com.EMPTY_PARAMETER)
		a = com.poll(ser) # LIGHT 1000
		print("Poll result("+str(i)+") = " + str(a))
		light = int(a[6:])
		light_total += light
	ser.close()
	light = light_total / 10
	#pdb.set_trace()
	
	save_transparency_log(light)

