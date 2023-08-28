from six import u
from onvif import ONVIFCamera
import cv2 
import time
import numpy as np
import requests

import asyncio, sys

import sys

#도현 : loop가 win32환경에서 정상 작동하지 않음. 아래 코드를 적용할시 코드가 실행되지만 controller가 정상 작동하는것 같지는 않음.
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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

#Camera movement definitions
def do_move(ptz, request):
    # Start continuous move
    global active
    if active:
        ptz.Stop({'ProfileToken': request.ProfileToken})
    active = True
    ptz.RelativeMove(request)

def move_up(ptz, request, tilt):
    print ('move up...')
    request.Translation = {'PanTilt':{'x': 0, 'y':tilt}}
    do_move(ptz, request)

def move_down(ptz, request, tilt):
    print ('move down...')
    request.Translation = {'PanTilt':{'x': 0, 'y':tilt}}
    do_move(ptz, request)

def move_right(ptz, request, pan):
    print ('move right...')
    request.Translation = {'PanTilt':{'x': pan, 'y':0}}
    do_move(ptz, request)

def move_left(ptz, request, pan):
    print ('move left...')
    request.Translation = {'PanTilt':{'x': pan, 'y':0}}
    do_move(ptz, request)
    

def move_upleft(ptz, request, pan, tilt):
    print ('move up left...')
    request.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
    do_move(ptz, request)
    
def move_upright(ptz, request, pan, tilt):
    print ('move up left...')
    request.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
    do_move(ptz, request)
    
def move_downleft(ptz, request, pan, tilt):
    print ('move down left...')
    request.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
    do_move(ptz, request)
    
def move_downright(ptz, request, pan, tilt):
    print ('move down left...')
    request.Translation = {'PanTilt':{'x': pan, 'y':tilt}}
    do_move(ptz, request)

#Create camera instance, prepare the device for control.
def setup_ptz():
    mycam = ONVIFCamera(IP, PORT, USER, PASS)
    # Create media service object
    media = mycam.create_media_service()
    
    # Create ptz service object
    global ptz
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0]

    # Get token from the first profile in the profiles list
    media_profile_token = media_profile.token

    # Setup stream configuration
    stream_setup = media.create_type("GetStreamUri")
    stream_setup.ProfileToken = media_profile_token
    stream_setup.StreamSetup = {'Stream':'RTP-Unicast', 'Transport' : {'Protocol': 'RTSP'}}

    # set up ptz status for position update
    global status
    status_setup = ptz.create_type("GetStatus")
    status_setup.ProfileToken = media_profile_token
    status = ptz.GetStatus(status_setup.ProfileToken)

    # get the stream URI
    media_uri = media.GetStreamUri(stream_setup)
    uri = media_uri.Uri
    uri = uri[:7] + "admin:idcitic405@" + uri[7:]
    print(uri)



    # # Display video streaming over the retrieved uri
    # cap = cv2.VideoCapture(uri)
 
    # time.sleep(2)
    
    # while(True):
    
    #     ret, frame = cap.read()
    #     print (ret)
    #     if ret == 1:
    #         cv2.imshow('frame',frame)
    #     else:
    #         print ("no video")
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    
    # cap.release()
    # cv2.destroyAllWindows()

    # Get PTZ configuration options for getting move range
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    global moverequest
    moverequest = ptz.create_type('RelativeMove')
    moverequest.ProfileToken = media_profile.token
    # if moverequest.Velocity is None:
    #     moverequest.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position


    # # Get range of pan and tilt
    # # NOTE: X and Y are velocity vector
    # global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.RelativePanTiltTranslationSpace[0].YRange.Min


def readin():
    """Reading from stdin and displaying menu"""
    global moverequest, ptz
    
    selection = sys.stdin.readline().strip("\n")
    lov=[ x for x in selection.split(" ") if x != ""]
    if lov:
        if lov[0].lower() in ["u","up"]:
            move_up(ptz,moverequest, 0.05)
        elif lov[0].lower() in ["d","do","dow","down"]:
            move_down(ptz,moverequest, -0.05)
        elif lov[0].lower() in ["l","le","lef","left"]:
            move_left(ptz,moverequest, 0.05)
        elif lov[0].lower() in ["r","ri","rig","righ","right"]:
            move_right(ptz,moverequest, -0.05)
        elif lov[0].lower() in ["ul"]:
            move_upleft(ptz,moverequest, 0.05, 0.05)
        elif lov[0].lower() in ["ur"]:
            move_upright(ptz,moverequest, -0.05, 0.05)
        elif lov[0].lower() in ["dl"]:
            move_downleft(ptz,moverequest, 0.05, -0.05)
        elif lov[0].lower() in ["dr"]:
            move_downright(ptz,moverequest, -0.05, -0.05)
        elif lov[0].lower() in ["s","st","sto","stop"]:
            ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            active = False
        else:
            print("What are you asking?\tI only know, 'up','down','left','right', 'ul' (up left), \n\t\t\t'ur' (up right), 'dl' (down left), 'dr' (down right) and 'stop'")
         
    print("")
    print("Your command: ", end='',flush=True)

if __name__ == '__main__':
    setup_ptz()
    loop = asyncio.get_event_loop()
    try:
        loop.add_reader(sys.stdin,readin)
        print("Use Ctrl-C to quit")
        print("Your command: ", end='',flush=True)
        loop.run_forever()
    except:
        pass
    finally:
        loop.remove_reader(sys.stdin)
        loop.close()