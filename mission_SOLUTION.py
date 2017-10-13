#!/usr/bin/env python
#

from ncclient import manager
import sys
import xml.dom.minidom
import xmltodict
from pprint import pprint
import requests
import json

# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
HOST = '198.18.133.218'
# use the NETCONF port for your CSR1000V device
PORT = 2022
# use the user credentials for your CSR1000V device
USER = 'admin'
PASS = 'C1sco12345'
# XML file to open
FILE = 'get_interface_stats.xml'

# Function to retrieve information via NETCONF
def get_netconf(xml_filter):
    """
    Main method that retrieves information via NETCONF get.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            return(m.get(f.read()))

def create_message(interface):
    """
    Create a Markdown formatted message about interface state
    """
    # MISSION: Replace XXX with the correct leaf
    message = "## Interface Stats: Interface %s \n" % (interface["name"])
    message += "* Speed: %s \n" % (interface["speed"])
    message += "* Status: %s \n" % (interface["oper-status"])
    message += "* MAC Address: %s \n" % (interface["phys-address"])
    message += "* Statistics \n"
    message += "    * Octets In: %s \n" % (interface["statistics"]["in-octets"])
    message += "    * Octets Out: %s \n" % (interface["statistics"]["out-octets"])
    message += "    * Errors In: %s \n" % (interface["statistics"]["in-errors"])
    message += "    * Errors Out: %s \n" % (interface["statistics"]["out-errors"])
    return(message)

def main():
    """
    Mission Entry Point
    """

    ############################################################
    # Mission Step 1: Make the NETCONF Connection
    ############################################################
    print("Mission Step 1: Making NETCONF Connection to Router")
    # Make NETCONF connection
    netconf = get_netconf(FILE)

    # PREREQ: perform a `pip install xmltodict` in the virtualenv
    # Create an Python Ordered Dict object containing the interface details
    interface = xmltodict.parse(netconf.xml)["rpc-reply"]["data"]["interfaces-state"]["interface"]

    # Mission Step Verification
    if not interface["name"] == "GigabitEthernet1":
        print("  FAILED!!!  ")
        sys.exit("Mission Failed")
    else:
        print("The Interface Details: ")
        pprint(interface)
        print("")


    ############################################################
    # Mission Step 2: Create the message
    ############################################################
    print("Mission Step 2: Create the message (Markdown Formatted)")
    message = create_message(interface)
    print("The message would be: ")
    print(message)
    print("")

if __name__ == '__main__':
    sys.exit(main())
