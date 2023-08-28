import serial
import time
from ptz_control_module import ptz_controller  as ptz_c

#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1
moverequest = None
ptz = None
active = False

ser = serial.Serial('COM4', 9600) #arduino serial
ptz = ptz_c(IP,PORT,USER,PASS)

try:
    while True:
        if ser.readable():
            print("u d r l : ")
            val = input()
            
            
            if val == 'u':
                val = val.encode('utf-8')
                ser.write(val)
                ptz.move_up()
                
                val = 'b'
                val = val.encode('utf-8')
                ser.write(val)

            elif val == 'd':   
                val = val.encode('utf-8')      
                ser.write(val)
                ptz.move_down()
                
                val = 'b'
                val = val.encode('utf-8')
                ser.write(val)
                
            elif val == 'l':
                val = val.encode('utf-8')        
                ser.write(val)
                ptz.move_left()
                
                val = 'b'
                val = val.encode('utf-8')
                ser.write(val)

            elif val == 'r':  
                val = val.encode('utf-8')    
                ser.write(val)
                ptz.move_right()
                
                val = 'b'
                val = val.encode('utf-8')
                ser.write(val)

            val = 's'
            val = val.encode('utf-8')    
            ser.write(val)
except(KeyboardInterrupt):
    ser.close()
          