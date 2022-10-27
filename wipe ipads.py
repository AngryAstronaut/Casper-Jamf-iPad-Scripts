#Sends wipe command to ipad ids in the ipads2wipe function

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def apioperator(jamfurl2):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }
    #
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_command>" \
    #        "<command>DisableLostMode</command><wallpaper_setting>3</wallpaper_setting><wallpaper_content>" \
    #        + txtimg + \
    #        "</wallpaper_content><mobile_devices><mobile_device><id>%s</id></mobile_device></mobile_devices>" \
    #        "</mobile_device_command>"


    #
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_command>" \
    #        "<command>DisableLostMode</command><mobile_devices><mobile_device><id>%s</id></mobile_device></mobile_devices>" \
    #        "</mobile_device_command>"
    #
    # body = data % ipadid
    url = 'https://casperjamfurlinstancehere:8443/' + jamfurl2
    r = requests.post(url, headers=headers, verify=False)
    # r = requests.post(url, body=data, headers=headers, verify=False)
    #
    m = r.text
    return str(m)

def ipads2wipe():
    ipadids = 'list of assets go here csv'
    jamfurl = 'JSSResource/mobiledevicecommands/command/EraseDevice/id/' + ipadids
    # post or put
    return apioperator(jamfurl)
#Commented for safety, uncomment to use
# print(str(ipads2wipe()))