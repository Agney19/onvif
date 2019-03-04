from time import sleep
import zeep
from onvif import ONVIFCamera, ONVIFService

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

# ------------------------------CONTINUOUS MOVE------------------------------
# Initialize camera 43
cam = ONVIFCamera('192.168.15.43', 80, 'agney1919', 'hDzmk0leTN0W', '/home/agney/anaconda3/lib/python3.7/site-packages/onvif_zeep-0.2.12-py3.7.egg/onvif/wsdl')
# Create media service
media_service = cam.create_media_service()
 # Get profiles
profiles = media_service.GetProfiles()
media_profile = profiles[0]
# Create PTZ service
ptz = cam.create_ptz_service()
 # Get ptz Consinuous move and Stop option
request_continuous_move = ptz.create_type("ContinuousMove")
request_continuous_move.ProfileToken = media_profile.token
request_stop = ptz.create_type("Stop")
request_stop.ProfileToken = media_profile.token

# Get Ptz Position
def get_ptz_position():
    # get & modify PTZ status
    status = ptz.GetStatus({"ProfileToken": media_profile.token})	
    print("--------------------------------------------------------------------------------")
    print("PTZ position: " + str(status.Position))
    print("--------------------------------------------------------------------------------")

# Stop
def stop():
    request_stop.PanTilt = True
    request_stop.Zoom = True
    ptz.Stop(request_stop)

# Continuous move
def do_continuous_move(timeout):
    ptz.ContinuousMove(request_continuous_move)
    sleep(timeout)
    stop()
    sleep(1)

#Tilting
def move_continuous_tilt(velocity, timeout):
    print("Tilt: velocity = " + str(velocity) + "; timeout = " + str(timeout))
    status = ptz.GetStatus({"ProfileToken": media_profile.token})
    status.Position.PanTilt.x = 0.0
    status.Position.PanTilt.y = velocity

    request_continuous_move.Velocity = status.Position
    do_continuous_move(timeout)

# Panning
def move_continuous_pan(velocity, timeout):
    print("Pan: velocity = " +str(velocity) + "; timeout = " + str(timeout) )
    status = ptz.GetStatus({"ProfileToken": media_profile.token})
    status.Position.PanTilt.x = velocity
    status.Position.PanTilt.y = 0.0

    request_continuous_move.Velocity = status.Position
    do_continuous_move(timeout)

#Zooming
def move_continuous_zoom(velocity, timeout):
    print("Zoom: velocity = " + str(velocity) + "; timeout = " + str(timeout))
    status = ptz.GetStatus({"ProfileToken": media_profile.token})
    status.Position.Zoom.x = velocity

    request_continuous_move.Velocity = status.Position
    do_continuous_move(timeout)

def continuous_move(velocity_one, timeout_one, velocity_two, timeout_two, velocity_three, timeout_three):
        move_continuous_pan(velocity_one, timeout_one)
        move_continuous_tilt(velocity_two, timeout_two)
        move_continuous_zoom(velocity_three, timeout_three)

get_ptz_position()
continuous_move(-2, 1, 1, 2, 0.5, 1)