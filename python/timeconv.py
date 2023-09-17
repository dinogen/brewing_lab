import math

def secs2hhmm(secs):
    if secs == None:
        return "00:00"
    if secs < 0:
        return "00:00"
    hh = math.trunc(secs / (3600))
    remain = secs - hh * 3600
    mm = math.trunc(remain/60)
    return "{:02d}:{:02d}".format(hh,mm)

def hhmm2secs(s):
    if s == "":
        return 0
    try:
        hh = int(s[0:2])
        mm = int(s[3:5])
    except:
        hh = 0
        mm = 0
        
    return hh*3600 + mm*60
    
