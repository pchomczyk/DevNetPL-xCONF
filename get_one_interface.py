#!/usr/bin/env python
#
# Get configured interfaces using Netconf
#
# darien@sdnessentials.com
#

import os
import sys
from ncclient import manager
import xmltodict
import xml.dom.minidom

# Import the env files
import env_lab  # noqa

# Create filter
netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet1</name>
    </interface>
  </interface>
</filter>"""

print("Opening NETCONF Connection to {}".format(env_lab.IOS_XE_1["host"]))

# Open a connection to the network device using ncclient
with manager.connect(
        host=env_lab.IOS_XE_1["host"],
        port=env_lab.IOS_XE_1["netconf_port"],
        username=env_lab.IOS_XE_1["username"],
        password=env_lab.IOS_XE_1["password"],
        hostkey_verify=False
        ) as m:

    print("Sending a <get-config> operation to the device.\n")
    # Make a NETCONF <get-config> query using the filter
    netconf_reply = m.get_config(source = 'running', filter = netconf_filter)

print("Here is the raw XML data returned from the device.\n")
# Print out the raw XML that returned
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")

# Parse the returned XML to an Ordered Dictionary
netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

# Create interface data
interface = netconf_data["interfaces"]["interface"]

print("The interface status of the device is: ")
# Loop over interfaces and report status
print("Interface {} enabled status is {}".format(
        interface["name"]["#text"],
        interface["enabled"]
        )
     )
print("\n")
