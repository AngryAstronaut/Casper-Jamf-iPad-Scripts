from lxml import etree
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# https://gist.github.com/bradschm/3fe129a308876b81381a

def apioperator(jamfurl, xpathvar):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }

    url = 'https://casperjamfurlinstancehere:8443/' + jamfurl
    m = requests.get(url, headers=headers, verify=False)
    m = m.text
    # print(m)
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    # tree2 = etree.tostring(tree, encoding='UNICODE', xml_declaration=False)

    find_text = etree.XPath(xpathvar)
    apiresults = find_text(tree)

    return apiresults


def ipadcommander(num):
    jamfurl = 'JSSResource/mobiledevices/match/%s' % num
    xpathvar = '//*/id/text()'
    # jamfurl = 'uapi/inventory/obj/mobileDevice/'+str(num)+'/subset/id & name' #% num
    # get
    ipadid = []
    m = apioperator(jamfurl, xpathvar)
    return m

lizst = ['105364', '106222', '106214', '106208', '105361', '106205', '106218', '106219', '106216', '105352', '105367', '105365', '105369', '105344', '105356', '105341', '105324', '105345', '105360', '105363', '105354', '105342', '106458', '106459', '106463', '106466', '106462', '106465', '106464', '106467', '106457', '106460', '106456', '106461']
b = ''
# while True:
#     a = ipadcommander(input("Enter iPad Asset here: "))
#     # b = ''
#     if len(str(a))<6:
#         continue
#
#     else:
#         # b += str(a[:])
#         b += str(a[:])
#         print(int(a[0]))
#         print('current list: ' + b[:])

while True:
    for i in lizst:
        # print(i)
        b += str(ipadcommander(i)) + ","
        # print(int(lizst[0]))

    else:
        print('current list: ' + b[:])
        break
        # if int(lizst[i]) < 6:
        #     continue


    # else:
    #     # b += str(a[:])
    #     b += str(a[:])
    #     print(int(a[0]))
    #     print('current list: ' + b[:])

    # "JSSResource/mobiledevicecommands/command/EraseDevice/id/"

