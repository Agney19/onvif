from time import sleep
import zeep
from onvif import ONVIFCamera, ONVIFService

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

# ------------------------------ABSOLUTE MOVE------------------------------
# Initialize camera 42
cam = ONVIFCamera('192.168.15.42', 80, 'agney1919', 'hDzmk0leTN0W', '/home/agney/anaconda3/lib/python3.7/site-packages/onvif_zeep-0.2.12-py3.7.egg/onvif/wsdl')
# Create media service
media_service = cam.create_media_service()
 # Get profiles
profiles = media_service.GetProfiles()
media_profile = profiles[0]
# Create PTZ service
ptz = cam.create_ptz_service()
 # Get ptz absolute move option
request_absolute_move = ptz.create_type("AbsoluteMove")
request_absolute_move.ProfileToken = media_profile.token

# Get Ptz Position
def get_ptz_position():
    # get & modify PTZ status
    status = ptz.GetStatus({"ProfileToken": media_profile.token})	
    print("--------------------------------------------------------------------------------")
    print("PTZ position: " + str(status.Position))
    print("--------------------------------------------------------------------------------")

# Absolute Move Function
def absolute_move(x, y, zoom):
    print("Absolute move: " + str(x) + ":" + str(y) + ":" + str(zoom))
	# get & modify PTZ status
    status = ptz.GetStatus({"ProfileToken": media_profile.token})
    status.Position.PanTilt.x = x
    status.Position.PanTilt.y = y
    status.Position.Zoom.x = zoom
	# set position
    request_absolute_move.Position = status.Position
    ptz.AbsoluteMove(request_absolute_move)
	
# Perform absolute moves
# Absolute Move 1
absolute_move(0.1, -0.5, 1)
sleep(3)
get_ptz_position()

# Absolute Move 2
absolute_move(0, 0, 0)
sleep(3)
get_ptz_position()
