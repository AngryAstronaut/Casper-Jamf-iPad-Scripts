from lxml import etree
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# modifing app install scopes
def scope2app(appid):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }
    # make available in self service (with extra xml)
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
    #        "<mobile_device_application><general><deployment_type>Make Available in Self Service</deployment_type>" \
    #        "<deploy_automatically>false</deploy_automatically></general></mobile_device_application>"

    # make available in self service (to manual install)
    # also makes app visible to all devices in site
    data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
           "<mobile_device_application><general>" \
           "<deploy_automatically>false</deploy_automatically></general>" \
           "<scope><all_mobile_devices>false</all_mobile_devices></scope></mobile_device_application>"

    # install automatically (hidden)
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
    #        "<mobile_device_application><general>" \
    #        "<deploy_automatically>true</deploy_automatically></general></mobile_device_application>"

    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
    #        "<mobile_device_application><general><deployment_type>" \
    #        "Install Automatically / Prompt Users to Install" \
    #        "</deployment_type>" \
    #        "<deploy_automatically>true</deploy_automatically></general></mobile_device_application>"

    # with required tags
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
    #        "<mobile_device_application>" \
    #        "<general>" \
    #        "<name>Color Bump 3D</name>" \
    #        "<bundle_id>com.colorup.game</bundle_id>" \
    #        "<version>1.1.3</version>" \
    #        "<category><name>No category assigned</name></category>" \
    #        "<deployment_type>Install Automatically/Prompt Users to Install</deployment_type>" \
    #        "<deploy_automatically>true</deploy_automatically>" \
    #        "<site><name>None</name></site></general>" \
    #        "</mobile_device_application>"



    # ['Color Bump 3D', 'com.colorup.game', '1.1.3', 'No category assigned', 'None']




    # < preferences > < dict > < key > abc < / key > < string > xyz < / string > < / dict > < / preferences >
    # Adds the mobile_device_id to the body - I would think if you wanted to, you could expand an array here to handle an unknown amount of devices if you wanted to apply it to a group.

    url = 'https://casperjamfurlinstance:8443/JSSResource/mobiledeviceapplications/id/'+str(appid)
    r = requests.put(url, data=data, headers=headers, verify=False)
    m = r.text

    try:
        utf8_parser = etree.XMLParser(encoding='utf-8')
        tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
        find_text = etree.XPath('//*/status/text()')
        xpathresults = find_text(tree)
        return xpathresults

    except:
        return [appid, 'xml put cmd fail', m]

def runapirun(jamfurl, xpathvar, n):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }

    # enter your casper jamf url with port # and forward slash below:
    url = 'https://casperjamfurlinstance:8443/' + jamfurl #+ " HTTP/1.1"
    m = requests.get(url, headers=headers, verify=False)
    # print(str(m.encoding))
    m = m.text
    try:
        utf8_parser = etree.XMLParser(encoding='utf-8')
        tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
        find_text = etree.XPath(xpathvar)
        # f1, f2, f4, f3 = find_text(tree)
        f1, f2, f3, f4, f5 = find_text(tree)
        # # xpathresults f1=id, f2=app name, f3=vpp name, f4=free?
        # # skips pupil services purchased apps
        # # pupil services vpp has an id of '2'
        # if '2' == f3:
        #     return [f1, f2, 'pupil services app']
        # # scope2app(n)
        # else:
        #     # sends the jamf app id on to the function that will
        #     # upload the new xml install settings
        #     submit = scope2app(f1)
        #     return [f1, f2, f3, submit]
        # # return m

        # if '2' == f3:
        #     return [f1, f2, 'pupil services app']
        #
        # elif 'false' == f4:
        #     submit = scope2app(f1)
        #     return [f1, f2, f3, submit]
        #
        # else:
        #     return [f1,f2,f3,f4]
        return [f1,f2,f3,f4,f5]
    except:
        return [n,'deleted or error']

# //*[@id="collapsible14"]/div[1]/div[2]/div[1]/span[2]
def appscope(n):
    jamfurl = 'JSSResource/mobiledeviceapplications/id/' + str(n)
    # jamfurl += number
    # Uses xpath to filter the xml and return the app text values
    # xpathvar = "//general/name/text() | //scope/mobile_device_groups/*/*/text()"
    # xpathvar = "//general/name/text() | //general/bundle_id/text() | //general/version/text() | //general/category/name/text() | //general/site/name/text()"
    # xpathvar = "//general/id/text() | //general/name/text() | //general/site/name/text() | //scope/all_mobile_devices/text() | //vpp/vpp_admin_account_id/text()"
    # xpathvar = "//general/id/text() | //general/name/text() | //vpp/vpp_admin_account_id/text() | //general/free/text()"
    xpathvar = "//general/id/text() | //general/name/text() | //vpp/vpp_admin_account_id/text() | //general/free/text() | //scope/all_mobile_devices/text()"
    # < scope > < all_mobile_devices > false
    # xpathvar = "//general/text() | //general/description/text() | //scope/mobile_device_groups/*/*/text()"
    appnames = runapirun(jamfurl, xpathvar, n)
    return appnames
#
results = input("Enter jamf app number to info: ")
# Will give you current scope of app:
print(appscope(results))


# ['Emotions 2 from I Can Do Apps', 'PS APPS', 'None', 'false', '2'] 22
# ['Color Bump 3D', 'No category assigned', 'None', 'true', '1']

# To make mass changes change the end range to last jamf app id #, leave start point at 3.
# Commented for Safety, Uncomment to use. This will take a while best to do after school. Set your laptop power settings
# accordingly.

# for i in range(3,2148):
#     print(appscope(i))
