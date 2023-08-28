from onvif import ONVIFCamera

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

        # Setup stream configuration
        stream_pair = media.create_type("GetStreamUri")
        stream_pair.ProfileToken = media_profile_token
        stream_pair.StreamSetup = {'Stream':'RTP-Unicast', 'Transport' : {'Protocol': 'RTSP'}}

        # get the stream URI
        media_uri = media.GetStreamUri(stream_pair)
        uri = media_uri.Uri
        self.uri = uri[:7] + "admin:idcitic405@" + uri[7:]
        print(self.uri)
        print(uri)