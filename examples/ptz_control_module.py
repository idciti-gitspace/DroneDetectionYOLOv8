from six import u
from onvif import ONVIFCamera
import cv2 
import time
import numpy as np
import requests
import asyncio, sys

#YOLOv8 update : 더 부드러운 카메라 트래킹을 위해 move의 tilt와 pan의 수치를 1/10으로 바꿈. 

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

class ptz_controller():
    def __init__(self,IP,PORT,USER,PASS):
        mycam = ONVIFCamera(IP, PORT, USER, PASS)
        # Create media service object
        self.media = mycam.create_media_service()
        
        # Create ptz service object
        self.ptz = mycam.create_ptz_service()

        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]

        # Get token from the first profile in the profiles list
        self.media_profile_token = self.media_profile.token

        #setup request msgs for ptz move
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration.token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        self.moverequest = self.ptz.create_type('RelativeMove')
        self.moverequest.ProfileToken = self.media_profile.token

        # # Get range of pan and tilt
        # # NOTE: X and Y are velocity vector
        # global XMAX, XMIN, YMAX, YMIN
        XMAX = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].XRange.Max
        XMIN = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].XRange.Min
        YMAX = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].YRange.Max
        YMIN = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].YRange.Min
        pass
    #Camera movement definitions
    def do_move(self, request):
        # Start continuous move
        global active
        if active:
            self.ptz.Stop({'ProfileToken': request.ProfileToken})
        active = True
        self.ptz.RelativeMove(request)

    def move_up(self, tilt = 0.02):
        print ('move up...')
        self.moverequest.Translation = {'PanTilt':{'x': 0, 'y':tilt}}
        self.do_move(self.moverequest)

    def move_down(self, tilt = -0.02):
        print ('move down...')
        
        self.moverequest.Translation = {'PanTilt':{'x': 0, 'y':tilt}}
        self.do_move(self.moverequest)

    def move_right(self, pan = -0.03):
        print ('move right...')
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':0}}
        self.do_move(self.moverequest)

    def move_left(self, pan = 0.03):
        print ('move left...')
        
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':0}}
        self.do_move(self.moverequest)
        

    def move_upleft(self, pan = 0.03, tilt = 0.02):
        print ('move up left...')
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
        self.do_move(self.moverequest)
        
    def move_upright(self, pan = -0.03, tilt = 0.02):
        print ('move up right...')
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
        self.do_move(self.moverequest)
        
    def move_downleft(self, pan = 0.03, tilt = -0.02):
        print ('move down left...')
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
        self.do_move(self.moverequest)
        
    def move_downright(self, pan = -0.03, tilt = -0.02):
        print ('move down right...')
        self.moverequest.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
        self.do_move(self.moverequest)

if __name__ == '__main__':
    ptz = ptz_controller(IP,PORT,USER,PASS)
    
    while True:
        print("u d r l ur ul dr dl: ")
        val = input()
        
        
        if val == 'u':
            val = val.encode('utf-8')
            ptz.move_up()
        elif val == 'd':   
            val = val.encode('utf-8')      
            ptz.move_down()
        elif val == 'l':
            val = val.encode('utf-8')        
            ptz.move_left()
        elif val == 'r':  
            val = val.encode('utf-8')    
            ptz.move_right()
        elif val == 'ul':
            val = val.encode('utf-8')    
            ptz.move_upleft()
        elif val == 'ur':
            val = val.encode('utf-8')    
            ptz.move_upright()
        elif val == 'dl':
            val = val.encode('utf-8')    
            ptz.move_downleft()
        elif val == 'dr':
            val = val.encode('utf-8')    
            ptz.move_downright()
            
           
    
