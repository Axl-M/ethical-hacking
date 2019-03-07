#!/usr/local/bin/python3

import subprocess
import optparse
import os
import re


def get_arguments():
    # Parse the passed arguments
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address (random generated if not set).")

    (options, arguments) = parser.parse_args()

    # parser.error("[-] die")
    return options


def random_mac():
    # TO DO
    v = 'xx'
    return v


def get_current_mac(interface):
    # Check if MAC has been changed correctly
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')

    spoofed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if spoofed_mac:
        return spoofed_mac.group(0)
    else:
        print("[-] Could not find MAC address")


def check_os():
    # Check the Operating System
    from sys import platform
    if platform == "linux" or platform == "linux2":
        print("[+] You are running: Linux")
        return "Linux"
    elif platform == "darwin":
        print("[+] You are running: OSX")
        return "OSX"
    elif platform == "win32":
        print("[+] You are running: Windows")
        return "Windows"
    else:
        print("[+] You are running: Other Operating System")
        return "Other"


opsys       = check_os()
options     = get_arguments()
interface   = options.interface
new_mac     = options.new_mac


# If the "interface" argument is empty, list the existing ones and ask the user:
if not interface:
    print("[+] Please select the device you want to change the MAC address for:")
    subprocess.call("networksetup -listallhardwareports | grep Device", shell=True)
    print(" ")
    interface = input("Device > ")


# only for Linux
if opsys == "linux":
    subprocess.call(["sudo", "ifconfig", interface, "down"])

if not new_mac:
    # random MAC changer
    print("[+] Changing MAC interface for " + interface + " to random MAC")
    os.system("sudo macchanger -r " + interface)
else:
    # user defined
    print("[+] Changing MAC interface for " + interface + " to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "ether", new_mac])

# only for Linux
if opsys == "linux":
    subprocess.call(["sudo", "ifconfig", interface, "up"])


current_mac = get_current_mac(interface)
print("Current MAC = " + str(current_mac))

print(random_mac())
