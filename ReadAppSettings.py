from lxml import etree
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings()


def runapirun(jamfurl, xpathvar):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'Authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }

    # enter your casper jamf url with port # and forward slash below:
    url = 'https://casperjamfurlinstance:8443/' + jamfurl #+ " HTTP/1.1"
    m = requests.get(url, headers=headers, verify=False)
    # print(str(m.encoding))
    m = m.text

    # try:
    #     utf8_parser = etree.XMLParser(encoding='utf-8')
    #     tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    #     find_text = etree.XPath(xpathvar)
    #     f1, f2, f3 = find_text(tree)
    #     #xpathresults
    #     if '20' or '21' == f3:
    #         return [f1, f2, f3, 'el app']
    #
    #     # scope2app(n)
    #     else:
    #         submit = "submitted " + f1 + " to next function"
    #         return [f1, f2, f3, submit]
    #     # return m
    # except:
    #     return ['error']

    try:
        utf8_parser = etree.XMLParser(encoding='utf-8')
        tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
        find_text = etree.XPath(xpathvar)
        xpathresults = find_text(tree)
        return xpathresults
        # return m
    except:
        # return m
        return "Error"

# //*[@id="collapsible14"]/div[1]/div[2]/div[1]/span[2]
def appscope(n):
    jamfurl = 'JSSResource/mobiledeviceapplications/id/' + str(n)
    # jamfurl += number
    # Uses xpath to filter the xml and return the app text values
    # xpathvar = "//general/name/text() | //scope/mobile_device_groups/*/*/text()"
    # xpathvar = "//general/name/text() | //general/bundle_id/text() | //general/version/text() | //general/category/name/text() | //general/site/name/text()"
    # xpathvar = "//general/name/text() | //general/category/name/text() | //scope/all_mobile_devices/text() | //general/site/name/text() | //vpp/vpp_admin_account_id/text()"
    # xpathvar = "//general/text() | //general/description/text() | //scope/mobile_device_groups/*/*/text()"
    # xpathvar = "//general/id/text() | //general/name/text() | //scope/all_mobile_devices/text() | //general/deployment_type/text() | //vpp/vpp_admin_account_id/text()"
    xpathvar = "//general/id/text() | //general/name/text() | //vpp/vpp_admin_account_id/text()"
    appnames = runapirun(jamfurl, xpathvar)
    return appnames

# results = input("Enter jamf app number to get installed apps: ")
#
# for i in range(1000,1015):
#     print("id = " + str(i))
#     print(appscope(i))

print(appscope(1011))

# ['Emotions 2 from I Can Do Apps', 'PS APPS', 'None', 'false', '2'] 22