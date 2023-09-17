from configparser import ConfigParser
DBPATH="/home/pi/brew.db"
INIPATH = "/home/pi/brew.ini"
ideal_temp = 20
_MIN_ = 60
_HOUR_ = _MIN_ * 60

# test
serial_dev = "niente"
base_url = "niente"
STIR_TIME   = 0
STIR_DELAY  = 99
TEMP_DELAY  = 99
HEAT_DELAY  = 99
#LIGHT_DELAY = 30 same as stir

# production
#serial_dev = "/dev/ttyACM0"
#base_url = "http://192.168.1.36:5000"
#STIR_TIME   = 30
#STIR_DELAY  =  4 * _HOUR_
#TEMP_DELAY  = 10 * _MIN_
#HEAT_DELAY  =  3 * _MIN_
##LIGHT_DELAY =  6 * _HOUR_

def writeConfig():
    global ideal_temp, STIR_DELAY,STIR_TIME,TEMP_DELAY,HEAT_DELAY,serial_dev,base_url
    sc = ConfigParser()
    sc.add_section("brewing")
    sc.add_section("timing")
    sc.set("brewing", "ideal_temp", str(ideal_temp))
    sc.set("brewing", "base_url", base_url)
    sc.set("brewing", "serial_dev", serial_dev)
    sc.set("timing", "stir_time", str(STIR_TIME))
    sc.set("timing", "stir_delay", str(STIR_DELAY))
    sc.set("timing", "temp_delay", str(TEMP_DELAY))
    sc.set("timing", "heat_delay", str(HEAT_DELAY))
    #sc.set("timing", "light_delay", str(LIGHT_DELAY))
    with open(INIPATH, 'w') as configfile:
        sc.write(configfile)

def readConfig():
    global ideal_temp, STIR_DELAY,STIR_TIME,TEMP_DELAY,HEAT_DELAY,serial_dev,base_url
    sc = ConfigParser()
    sc.readfp(open(INIPATH),"brew.ini")
    #print( sc.sections() )
    ideal_temp  = sc.getint("brewing", "ideal_temp", )
    base_url    = sc.get("brewing", "base_url")
    serial_dev  = sc.get("brewing", "serial_dev")
    STIR_TIME   = sc.getint("timing", "stir_time")
    STIR_DELAY  = sc.getint("timing", "stir_delay")
    TEMP_DELAY  = sc.getint("timing", "temp_delay")
    HEAT_DELAY  = sc.getint("timing", "heat_delay")
    #LIGHT_DELAY = sc.getint("timing", "light_delay")

def printConfig():
    global ideal_temp, STIR_DELAY,STIR_TIME,TEMP_DELAY,HEAT_DELAY,serial_dev,base_url
    print("ideal_temp: " + str(ideal_temp))
    print("serial_dev: " + serial_dev)
    print("base_url: " + base_url)

#if __name__ == "__main__":
#    readConfig()
#    writeConfig()
