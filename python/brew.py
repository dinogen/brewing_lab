#!/usr/bin/env python3
#import pdb
import com
import time
import sched
import stirrer
import temp_sensor
import heater
import datetime
import light_sensor
import led
from timeconv import secs2hhmm
import config 

ideal_temp_max = None
ideal_temp_min = None
o_sched = None

def print_log(msg):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st + " " + msg)

def do_event_checktemp():
    global o_sched
    print_log("Check temp begin")
    config.readConfig()
    temp_dt = time.gmtime()
    o_temp = temp_sensor.temp_sensor(ser)
    t0 = o_temp.read(0)
    o_temp.save_log(0,t0,temp_dt)
    t1 = o_temp.read(1)
    o_temp.save_log(1,t1,temp_dt)
    average_t = (t0+t1) / 2.0
    print_log("avg temp = " + str(average_t))
    o_temp.save_log(3,average_t,temp_dt)
    o_sched.enter(config.TEMP_DELAY, 2, do_event_checktemp)
    print_log("Check temp end; next in " + secs2hhmm(config.TEMP_DELAY))

def do_event_heat():
    global ideal_temp_max, ideal_temp_min
    global o_sched
    config.readConfig()
    print_log("Heating begin")
    o_temp = temp_sensor.temp_sensor(ser)
    o_heater = heater.heater(ser)
    t0 = o_temp.read(0)
    t1 = o_temp.read(1)
    t  = (t0+t1)/2.0
    if t < ideal_temp_min:
        o_heater.turn_on()
        o_heater.save_log(1)
    if t > ideal_temp_max:
        o_heater.turn_off()
        o_heater.save_log(0)
    o_sched.enter(config.HEAT_DELAY,3,do_event_heat)
    print_log("Heating end; next in " + secs2hhmm(config.HEAT_DELAY))

def do_event_light_and_stir():
    global o_sched
    # light measuring
    print_log("Light measuring begin")
    config.readConfig()
    o_light = light_sensor.light_sensor(ser)
    o_led = led.led(ser)
    o_led.turn_on()
    time.sleep(1)
    light = o_light.read()
    o_led.turn_off()
    o_light.save_log(light)
    print_log("light = " + str(light))
    print_log("Light measuring end; next in " + secs2hhmm(config.STIR_DELAY))
    # stirring
    if config.STIR_TIME > 0:
        print_log("Stirring begin")
        o_stir = stirrer.stirrer(ser)
        result = o_stir.stir_for_n_seconds(config.STIR_TIME)
        o_stir.save_log(result)
        print_log("Stirring end; next just after light measuring." )
    else:
        print_log("Stirring disabled")
    o_sched.enter(config.STIR_DELAY,4,do_event_light_and_stir)

if __name__ == "__main__":
    config.readConfig()
    config.printConfig()
    ideal_temp_max = config.ideal_temp + 0.5
    ideal_temp_min = config.ideal_temp - 0.5

    o_sched = sched.scheduler(time.time, time.sleep)

    ser = com.open_serial(config.serial_dev)
    do_event_checktemp()
    do_event_heat()
    do_event_light_and_stir()
    o_sched.run()
