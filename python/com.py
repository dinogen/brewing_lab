import serial
import time
#import pdb
import sys

OK_MESSAGE = b'OK'
EMPTY_PARAMETER    = b'0000'
START_STIR_COMMAND = b'START STIR'
STOP_STIR_COMMAND  = b'STOP STIR '
START_HEAT_COMMAND = b'START HEAT'
STOP_HEAT_COMMAND  = b'STOP HEAT '
READ_TEMP_COMMAND  = b'READ TEMP '
START_LED_COMMAND  = b'START LED ' 
STOP_LED_COMMAND   = b'STOP LED  '
READ_LIGHT_COMMAND = b'READ LIGHT'

def open_serial(serial_device):
    ser = serial.Serial(serial_device,9600,timeout=5,dsrdtr=False)
    
    time.sleep(5)
    if ser:
        print("Seriale ok \n") 
    else:
        print("Seriale KO\n")
        sys.exit()
    return ser

def send_command(ser, command,parameter):
    #print("Sending command " + str(command) + " with parameter " + str(parameter))
    ser.write(command)
    ser.write(b' ')
    ser.write(parameter)
    #print("Command sent")
    return True

def poll(ser):
    done = True
    for i in range(5):
        time.sleep(1)
        read_serial=ser.readline()
        if read_serial:
            return read_serial[:-2]
    return None



# if __name__ == "__main__":
    # print("Inizio \n")
    # ser = open_serial()
    # send_command(ser, START_STIR_COMMAND, EMPTY_PARAMETER)
    # a = poll(ser)
    # print("Poll result = " + str(a))
    # time.sleep(5)
    # send_command(ser, STOP_STIR_COMMAND, EMPTY_PARAMETER)
    # a = poll(ser)
    # ser.close()
    # print("Poll result = " + str(a))
    # #pdb.set_trace()
    # if a == OK_MESSAGE:
        # print("Tutto ok")
    # else:
        # print("Errore" + str(a))


