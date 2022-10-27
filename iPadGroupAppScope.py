from lxml import etree
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings()

# https://gist.github.com/bradschm/3fe129a308876b81381a

def ipad2group():
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }
    # add
    # adds to current devices in group scope
    #['1296']['1298']['1301']
    data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>" \
           "<mobile_device_group><mobile_device_additions>" \
           "<mobile_device><id>551</id></mobile_device>" \
           "<mobile_device><id>554</id></mobile_device>" \
           "<mobile_device><id>553</id></mobile_device>" \
           "<mobile_device><id>552</id></mobile_device>" \
           "<mobile_device><id>550</id></mobile_device>" \
           "<mobile_device><id>548</id></mobile_device>" \
           "<mobile_device><id>549</id></mobile_device>" \
           "<mobile_device><id>547</id></mobile_device>" \
           "<mobile_device><id>561</id></mobile_device>" \
           "<mobile_device><id>555</id></mobile_device>" \
           "<mobile_device><id>562</id></mobile_device>" \
           "<mobile_device><id>560</id></mobile_device>" \
           "<mobile_device><id>556</id></mobile_device>" \
           "<mobile_device><id>557</id></mobile_device>" \
           "<mobile_device><id>559</id></mobile_device>" \
           "<mobile_device><id>558</id></mobile_device>" \
           "<mobile_device><id>566</id></mobile_device>" \
           "<mobile_device><id>565</id></mobile_device>" \
           "<mobile_device><id>569</id></mobile_device>" \
           "<mobile_device><id>570</id></mobile_device>" \
           "<mobile_device><id>572</id></mobile_device>" \
           "<mobile_device><id>573</id></mobile_device>" \
           "<mobile_device><id>574</id></mobile_device>" \
           "<mobile_device><id>575</id></mobile_device>" \
           "<mobile_device><id>497</id></mobile_device>" \
           "<mobile_device><id>567</id></mobile_device>" \
           "<mobile_device><id>563</id></mobile_device>" \
           "<mobile_device><id>564</id></mobile_device>" \
           "<mobile_device><id>568</id></mobile_device>" \
           "<mobile_device><id>571</id></mobile_device>" \
           "<mobile_device><id>576</id></mobile_device>" \
           "<mobile_device><id>577</id></mobile_device>" \
           "</mobile_device_additions></mobile_device_group>"

    # overwrite
    # effectively clears current device list, and then adds devices listed
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_group>" \
    #        "<mobile_devices><mobile_device><id>1301</id></mobile_device>" \
    #        "<mobile_device><id>1298</id></mobile_device></mobile_devices>" \
    #        "</mobile_device_group>"

    # ['1296']['1298']['1301']['1300']['1297']['1299']['392']['454']['435']['413']['430']['402']['434']
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_group>" \
    #        "<mobile_devices>" \
    #        "<mobile_device><id>1301</id></mobile_device>" \
    #        "<mobile_device><id>1298</id></mobile_device>" \
    #        "<mobile_device><id>1296</id></mobile_device>" \
    #        "<mobile_device><id>1301</id></mobile_device>" \
    #        "<mobile_device><id>1300</id></mobile_device>" \
    #        "<mobile_device><id>1297</id></mobile_device>" \
    #        "<mobile_device><id>1299</id></mobile_device>" \
    #        "<mobile_device><id>392</id></mobile_device>" \
    #        "<mobile_device><id>454</id></mobile_device>" \
    #        "<mobile_device><id>435</id></mobile_device>" \
    #        "<mobile_device><id>413</id></mobile_device>" \
    #        "<mobile_device><id>430</id></mobile_device>" \
    #        "<mobile_device><id>402</id></mobile_device>" \
    #        "<mobile_device><id>434</id></mobile_device>" \
    #        "</mobile_devices></mobile_device_group>"

    # empty
    # remove all devices from group
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_group>" \
    #        "<mobile_devices></mobile_devices>" \
    #        "</mobile_device_group>"

    # delete
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_group>" \
    #        "<mobile_device_deletions><mobile_device><id>846</id></mobile_device>" \
    #        "</mobile_device_deletions></mobile_device_group>"

    # Adds the mobile_device_id to the body
    body = data
    ## the above sec is from bradscm git hub
    ## 302 is test group
    url = 'https://casperjamfurlinstancehere:8443/JSSResource/mobiledevicegroups/id/355'
    r = requests.put(url, data=body, headers=headers, verify=False)
    m = r.text
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    # tree2 = etree.tostring(tree, encoding='UNICODE', xml_declaration=False)
    find_text = etree.XPath('//*/status/text()')
    apiresults2 = find_text(tree)
    return tree

# adds ipad group to app scope
def group2app():
    headers = {
        # the basic authorization string is a base64 encoded user:pass
        'authorization': 'Basic amFtZmFwaXVzZXJuYW1lOmphbWZhcGlwYXNzd29yZA==',
        'Accept': 'application/xml',
        'Connection': 'keep-alive',
    }
    ## this sec is from bradschm git hub

    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_group>" \
    #        "<mobile_device_additions><mobile_device><id>10</id></mobile_device>" \
    #        "</mobile_device_additions></mobile_device_group>"

    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><mobile_device_application>" \
    #        "<mobile_device_groups><mobile_device_group><id>302</id>" \
    #        "</mobile_device_group></mobile_device_group>"


    # Add / Remove the following from the xml to add remove the group
    # <mobile_device_group><id>302</id></mobile_device_group>

    # delete
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><mobile_device_application>" \
    #        "<scope><mobile_device_groups>" \
    #        "</mobile_device_groups></scope></mobile_device_application>"
    # add
    # data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><mobile_device_application>" \
    #        "<scope><mobile_device_groups>" \
    #        "<mobile_device_group><id>234</id></mobile_device_group>" \
    #        # "<mobile_device_group><id>114</id></mobile_device_group>" \
    #        # "<mobile_device_group><id>136</id></mobile_device_group>" \
    #        # "<mobile_device_group><id>135</id></mobile_device_group>" \
    #        "</mobile_device_groups></scope></mobile_device_application>"

    # Adds the mobile_device_id to the body
    data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><mobile_device_application>" \
           "<scope><mobile_device_groups>" \
           "<mobile_device_group><id>370</id></mobile_device_group>" \
           "<mobile_device_group><id>234</id></mobile_device_group>" \
           "</mobile_device_groups></scope></mobile_device_application>"

    body = data

    # url = 'https://casperjamfurlinstancehere:8443/JSSResource/mobiledeviceapplications/name/Quick Blocks'
    url = 'https://casperjamfurlinstancehere:8443/JSSResource/mobiledeviceapplications/id/2148'
    r = requests.put(url, data=body, headers=headers, verify=False)
    m = r.text
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(m.encode('utf-8'), parser=utf8_parser)
    # tree2 = etree.tostring(tree, encoding='UNICODE', xml_declaration=False)
    find_text = etree.XPath('//*/status/text()')
    apiresults2 = find_text(tree)
    # print(m)
    return m

print(str(group2app()))
# ipad2group()
# print(str(ipad2group()))