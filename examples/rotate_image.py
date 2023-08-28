from onvif import ONVIFCamera

def rotate_image_180():
    ''' Rotate the image '''

    # Create the media service
    mycam = ONVIFCamera('192.168.0.2', 80, 'admin', 'idcitic405')
    media_service = mycam.create_media_service()

    profiles = media_service.GetProfiles()[0]

    # Use the first profile and Profiles have at least one
    token = profiles.token

    # Get all video source configurations
    configurations_list = media_service.GetVideoSourceConfigurations()

    # Use the first profile and Profiles have at least one
    video_source_configuration = configurations_list[0]

    # Enable rotate
    video_source_configuration.Extension = {'Rotate':{'Mode':'ON', 'Degree' : 90}}
    #video_source_configuration.Extension[0].Rotate[0].Mode[0] = 'ON'

    # Create request type instance
    request = media_service.create_type('SetVideoSourceConfiguration')
    request.Configuration = video_source_configuration

    # ForcePersistence is obsolete and should always be assumed to be True
    request.ForcePersistence = True

    # Set the video source configuration
    media_service.SetVideoSourceConfiguration(request)

if __name__ == '__main__':
    rotate_image_180()
