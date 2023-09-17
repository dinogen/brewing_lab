#!/usr/bin/env python3

#import pdb
import time
import com
import stirrer
import led
import heater
import temp_sensor
import light_sensor

if __name__ == "__main__":
    ser = com.open_serial("/dev/ttyACM0")

    # stir for 5 sec
    print("Stirring for 5 seconds.")
    print("Please, check if the fan is rotating")
    s = stirrer.stirrer(ser)
    result = s.stir_for_n_seconds(5)
    print("Stirring off.")
    s.save_log(result)

    #led on for 5 sec
    print("Led on")
    l = led.led(ser)
    l.turn_on()
    time.sleep(5)
    l.turn_off()
    print("Led off")

    # heat for 10 sec
    h = heater.heater(ser)
    h.turn_on()
    print("Tourning the heating on.")
    h.save_log(1)
    time.sleep(5)
    h.turn_off()
    print("Tourning the heating off.")
    h.save_log(0)

    # read temp
    t = temp_sensor.temp_sensor(ser)
    temp = t.read(0)
    print("Temperature is " + str(temp) + " degrees.")
    t.save_log(0,temp)

    # read light 
    ls = light_sensor.light_sensor(ser)
    light = ls.read()
    print ("Light intensity with the led off is " + str(light))
    l.turn_on()
    time.sleep(1)
    light = ls.read()
    print ("Light intensity with the led on is " + str(light))
    l.turn_off()
    print("Led off")

    print("Test ended")
