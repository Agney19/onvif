from time import sleep
import zeep
from onvif import ONVIFCamera, ONVIFService

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue

# ------------------------------FOCUS------------------------------
# Initialize camera 43
cam = ONVIFCamera('192.168.15.43', 80, 'agney1919', 'hDzmk0leTN0W', '/home/agney/anaconda3/lib/python3.7/site-packages/onvif_zeep-0.2.12-py3.7.egg/onvif/wsdl')
# Create media service
media_service = cam.create_media_service()
 # Get profiles
profiles = media_service.GetProfiles()
media_profile = profiles[0]
# Create PTZ service
ptz = cam.create_ptz_service()
# Creating imaging service
imaging = cam.create_imaging_service()
 # Getting imaging move options
request_focus_change = imaging.create_type("Move")
request_focus_change.VideoSourceToken = media_profile.VideoSourceConfiguration.SourceToken
request_stop = ptz.create_type("Stop")
request_stop.ProfileToken = media_profile.token

# Stop any movement
def stop():
    request_stop.PanTilt = True
    request_stop.Zoom = True
    ptz.Stop(request_stop)
		
		
def get_focus_options():
    # Get imaging status
    imaging_status = imaging.GetStatus({"VideoSourceToken": media_profile.VideoSourceConfiguration.SourceToken})
    print("Imaging status: " + str(imaging_status))
    print("--------------------------------------------------------------------------------")

 # Contunuous focus change
def change_focus_continuous(speed, timeout):
    print("Continuous focus change: speed = " + str(speed) + "; timeout = " + str(timeout))
    request_focus_change.Focus = {
        "Continuous": {
            "Speed": speed
        }
    }
    imaging.Move(request_focus_change)
    sleep(timeout)
    stop()
    sleep(3)

# Absolute focus change
def change_focus_absolute(position, speed):
    print("Absolute focus change: position = " + str(position) + "; speed = " + str(speed))
    request_focus_change.Focus = {
        "Absolute": {
            "Position": position,
            "Speed": speed
        }
    }
    imaging.Move(request_focus_change)
    sleep(5)

get_focus_options()
# Focus change 1
change_focus_continuous(0.5, 2)
sleep(5)

get_focus_options()
# Focus change 2
change_focus_absolute(0.5, 2)
sleep(5)
get_focus_options()
