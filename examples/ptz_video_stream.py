from six import u
from onvif import ONVIFCamera
import cv2 
import time
import numpy as np
import requests

#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

ptz = None

# class ptz_control(IP,PORT,USER,PASS):


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

    # Setup video source configuration for image rotation
    config_req = media.create_type('GetVideoSourceConfiguration')
    config_req.ConfigurationToken = media_profile.VideoSourceConfiguration.token
    vid_src_config = media.GetVideoSourceConfiguration(config_req)
    vid_src_config.Extension = {'Rotate': {'Mode':'ON','Degree':180}}

    # Reverse (rotate by 180 deg) image
    media_profile.VideoSourceConfiguration.Configuration = vid_src_config
    media_profile.VideoSourceConfiguration.ForcePersistence = False


    # Setup stream configuration
    stream_pair = media.create_type("GetStreamUri")
    stream_pair.ProfileToken = media_profile_token
    stream_pair.StreamSetup = {'Stream':'RTP-Unicast', 'Transport' : {'Protocol': 'RTSP'}}

    # get the stream URI
    media_uri = media.GetStreamUri(stream_pair)
    uri = media_uri.Uri
    uri = uri[:7] + "admin:idcitic405@" + uri[7:]
    print(uri)




    # Display video streaming over the retrieved uri
    cap = cv2.VideoCapture(uri)
 
    time.sleep(2)
    
    while(True):
    
        ret, frame = cap.read()
        print (ret)
        if ret == 1:
            cv2.imshow('frame',frame)
        else:
            print ("no video")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    setup_ptz()