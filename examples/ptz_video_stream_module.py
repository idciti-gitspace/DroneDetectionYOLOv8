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

class ptz_streamer():
    def __init__(self,IP,PORT,USER,PASS):
        mycam = ONVIFCamera(IP,PORT,USER,PASS)
        # Create media service object
        media = mycam.create_media_service()
        
        # Get target profile
        media_profile = media.GetProfiles()[0]

        # Get token from the first profile in the profiles list
        media_profile_token = media_profile.token

        # Setup video source configuration for image rotation
        config_req = media.create_type('GetVideoSourceConfiguration')
        config_req.ConfigurationToken = media_profile.VideoSourceConfiguration.token
        #vid_src_config = media.GetVideoSourceConfiguration(config_req)
        #vid_src_config.Extension = {'Rotate': {'Mode':'ON', 'Degree': 90}}

        # Reverse (rotate by 180 deg) image
        #media_profile.VideoSourceConfiguration.Configuration = vid_src_config
        #media_profile.VideoSourceConfiguration.ForcePersistence = False

        #Set video config(rotate image)
        #request = media.create_type('SetVideoSourceConfiguration')
        #request.Configuration = vid_src_config

        # ForcePersistence is obsolete and should always be assumed to be True
        #request.ForcePersistence = True

        # Set the video source configuration
        #media.SetVideoSourceConfiguration(request)


        # Setup stream configuration
        stream_pair = media.create_type("GetStreamUri")
        stream_pair.ProfileToken = media_profile_token
        stream_pair.StreamSetup = {'Stream':'RTP-Unicast', 'Transport' : {'Protocol': 'RTSP'}}

        # get the stream URI
        media_uri = media.GetStreamUri(stream_pair)
        uri = media_uri.Uri
        self.uri = uri[:7] + "admin:idcitic405@" + uri[7:]
        print(uri)

    def stream(self):
        # Display video streaming over the retrieved uri
        cap = cv2.VideoCapture(self.uri)
    
        time.sleep(2)
        pTime = 0

        while (True):
        
            ret, frame = cap.read()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            if ret == 1:
                cTime = time.time()
                fps = 1/(cTime - pTime)
                pTime = cTime
                cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3,(0,255,0), 2)
                cv2.imshow('frame',frame)
            else:
                print ("no video")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    ptz_stream_obj = ptz_streamer(IP,PORT,USER,PASS)
    ptz_stream_obj.stream()