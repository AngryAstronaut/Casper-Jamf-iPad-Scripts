import sys
import csv

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import base64
from io import BytesIO

from lxml import etree
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

wallpaperfile = 'RiverStream.jpg' # png or jpg

# Readme

# To Run:

# CSV Mode:
# in terminal, cd to directory containing script
# then enter: python3 CSV_Wallpaper.py csvfile
# csv file format is: ipad serial or asset,text you want on wallpaper
# if no csv file is specified, program goes into manual mode

# Manual Mode:
# is a loop of asking for ipad asset and text you want on wallpaper
# if asset number is entered for both asset and text, script will look up
# the current name for the ipad in jamf and enter it as the wallpaper text.
# This function is not available in csv mode but can be added by uncommenting
# a code block I've noted near the bottom.

# Notes
# Every time a background has been uploaded the script auto saves the last background
# as lastbackground.png to the working directory. The image is overwritten every run
# and is useful for debugging or reference.
# The file used for the background should be in same folder as script, file name should
# be entered above.
# Script can be modified so that a different image could be specified
# as an option or specified as a third csv field with some small code tweaks.
# Different iPads models use different size images.


# https://gist.github.com/bradschm/3fe129a308876b81381a

# bash code
# base64 <<< username:pass to encode here
# base64 -D <<< base64 encoded text here to decode

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
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    # tree2 = etree.tostring(tree, encoding='UNICODE', xml_declaration=False)
    print(tree)
    find_text = etree.XPath(xpathvar)
    apiresults = find_text(tree)

    return apiresults
    # return m


def apioperator3(jamfurl2, ipadid, txtimg):
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }

    ## this sec is from bradschm git hub
    data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_command>" \
           "<command>Wallpaper</command><wallpaper_setting>3</wallpaper_setting><wallpaper_content>" \
           + txtimg + \
           "</wallpaper_content><mobile_devices><mobile_device><id>%s</id></mobile_device></mobile_devices>" \
           "</mobile_device_command>"
    # Adds the mobile_device_id to the body - I would think if you wanted to, you could expand an array here to handle an unknown amount of devices if you wanted to apply it to a group.
    body = data % ipadid
    ## the above sec is from bradscm git hub
    url = 'https://casperjamfurlinstancehere:8443/' + jamfurl2
    r = requests.post(url, data=body, headers=headers, verify=False)
    m = r.text
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    # tree2 = etree.tostring(tree, encoding='UNICODE', xml_declaration=False)
    find_text = etree.XPath('//*/status/text()')
    apiresults2 = find_text(tree)
    return apiresults2


def text2image(asset, text):
    # much of this from
    # http://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil

    # get an image
    # To do, change image based on building, staff, checkout
    base = Image.open(wallpaperfile).convert('RGBA')
    X, Y = base.size


    # print(x,y)
    # make a blank image for the text, initialized to transparent text color
    # txt = Image.new('RGBA', (X, Y), (255, 255, 255, 128))
    txt = Image.new('RGBA', (X, Y), (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype("Arial.ttf", 55)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # get text size
    w, h = d.textsize(text, font=fnt)

    # draw text centered, half opacity
    d.text(((X - w) / 2, ((Y - h) / 2) - 50), text, font=fnt, fill=(255, 255, 255, 255))

    # get text size
    w, h = d.textsize(str(asset), font=fnt)

    # draw text centered, full opacity
    d.text(((X - w) / 2, ((Y - h) / 2) + 75), str(asset), font=fnt, fill=(255, 255, 255, 255))

    out = Image.alpha_composite(base, txt)

    buffer = BytesIO()
    out.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue())

    out.save("lastbackground.png")

    # out.show()
    s = str(img_str)[1:]
    return s


def ipadcommander(num, text):
    # add image file selection
    # add option for more text
    jamfurl = 'JSSResource/mobiledevices/match/%s' % num
    xpathvar = '//*/id/text()'
    # jamfurl = 'uapi/inventory/obj/mobileDevice/'+str(num)+'/subset/id & name' #% num
    # get
    ipadid = []
    m = apioperator(jamfurl, xpathvar)
    n = 0
    n += int(m[0])
    asset = '' + str(n)

    # create image
    txtimg = text2image(num, text)

    # upload image to ipad
    jamfurl2 = 'JSSResource/mobiledevicecommands/command/Wallpaper'  # % str(n)
    # post or put
    n = apioperator3(jamfurl2, asset, txtimg)
    r = ''
    r += str(n[0])
    return r
    # return asset

# looks up ipad name in jamf
def jamfname(asset):
    jamfurl = 'JSSResource/mobiledevices/match/%i' % int(asset)
    xpathvar = '//*/name/text()'
    m = apioperator(jamfurl, xpathvar)

    name, num = m[0].split(" - ")
    ipadname = name

    print(ipadname)
    return ipadname

try:
    f = open(sys.argv[1], 'U')
    reader = csv.DictReader(f, fieldnames=['serial', 'name'])
    next(reader)
    for row in reader:
        serial = row['serial']
        name, asset = row['name'].split(" - ")
        a = asset
        b = name
        # print(serial)
        # print(name)
        # print(asset)
        try:
            print("Connecting to JAMF...")
            c = ipadcommander(a, b)
            print(c)

            # Uncomment the code block below to enable ipad name lookup with asset,asset csv file.
            # Be sure to comment out the first three lines after the above 'try:' statement.

            # if a != b:
            #     c = ipadcommander(a, b)
            #     print(c)
            # # If you set the iPad asset as the name also, then it will use the name that is already in JAMF
            # if a == b:
            #     try:
            #         print("Locating iPad name...")
            #         b = jamfname(a)
            #         # print("JAMF has iPad %s as being named %s") % a, b
            #         c = ipadcommander(a, b)
            #         print(c)
            #
            #     except:
            #         print("An error has occurred, the ipad may not be in the system.")
            #         # print("Please check enrollment status of %s, or try specifying wallpaper text.") % a

        except etree.XMLSyntaxError:
            print("Reconnecting to JAMF...")
            c = ipadcommander(a, b)
            print(c)
            continue

except:
    print("Text-2-Wallpaper ")

    print("Manual Entry: ")

    while True:

        a = input("Enter iPad Asset Here: ")
        if a in "exit, quit, q":
            exit()
            break

        b = input("Enter Additional Text: ")
        if b in "exit, quit, q":
            exit()
            break

        try:
            print("Connecting to JAMF...")

            if a != b:
                c = ipadcommander(a, b)
                print(c)
            # If you set the iPad name as the asset, then it will use the name that is already in JAMF
            if a == b:
                try:
                    print("Locating iPad name...")
                    b = jamfname(a)
                    # print("JAMF has iPad %s as being named %s") % a, b
                    c = ipadcommander(a, b)
                    print(c)

                except:
                    print("An error has occurred, the ipad may not be in the system.")
                    # print("Please check enrollment status of %s, or try specifying wallpaper text.") % a

        except etree.XMLSyntaxError:
            print("Reconnecting to JAMF...")
            c = ipadcommander(a, b)
            print(c)
            continue
            # break


