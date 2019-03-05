#!/usr/bin/env python

from ncclient import manager
import sys


# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)
import env_lab  # noqa


# create a main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    with manager.connect(
            host=env_lab.IOS_XE_1["host"],
            port=env_lab.IOS_XE_1["netconf_port"],
            username=env_lab.IOS_XE_1["username"],
            password=env_lab.IOS_XE_1["password"],
            hostkey_verify=False
            ) as m:

        # print all NETCONF capabilities
        print('***Here are the Remote Devices Capabilities***')
        for capability in m.server_capabilities:
            print(capability.split('?')[0])

if __name__ == '__main__':
    sys.exit(main())
