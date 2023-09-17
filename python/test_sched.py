#!/usr/bin/env python3
import sched
import time
import datetime

o_sched = sched.scheduler(time.time, time.sleep)

def do_eventA():
    for i in range(5):
        time.sleep(1)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st + " eventA " + str(i) )
    o_sched.enter(60, 1, do_eventA)

def do_eventB():
    for i in range(3):
        time.sleep(1)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st + "     eventB " + str(i) )
    o_sched.enter(10, 2, do_eventB)

if __name__ == "__main__":
    do_eventA()
    do_eventB()
    o_sched.run()
