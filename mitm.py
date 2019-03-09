#!/usr/local/bin/python3

import re
import os
import sys
import socket
# import argparse
import subprocess
import scapy.all as scapy


def check_os():
    # Check the Operating System
    from sys import platform
    if platform == "linux" or platform == "linux2":
        print("[+] You are running: Linux\n")
        return "Linux"
    elif platform == "darwin":
        print("[+] You are running: OSX\n")
        return "OSX"
    else:
        print("[-] You are running: Other Operating System\n")
        print("[-] This operating system is not supported yet.\n")
        sys.exit()


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_current_mac(interface):
    # Check if MAC has been changed correctly
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')

    spoofed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if spoofed_mac:
        return spoofed_mac.group(0)
    else:
        print("[-] Could not find MAC address")


def get_router_ip(opsys):
    if opsys == "Linux":
        return os.popen('ip route show | grep - i \'default via\' | awk \'{print $3 }\'').read()
    else:
        return os.popen('netstat -nr | grep default | grep -o \'[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\'').read()


def scan_network(ip):
    print("\n[+] Scanning IP range for connected clients: " + ip)

    # combine two packets and send
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # send the packet
    print("\n[+] Sending packets...\n")
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)  # packet, timeout
    print("[+] Received " + str(len(answered_list)) + " responses:\n")

    # process responses
    clients_list = []
    for answer in answered_list:
        client_dict = {"mac": answer[1].hwsrc, "ip": answer[1].psrc}
        clients_list.append(client_dict)

    return clients_list


def print_clients(clients_list):

    print("IP\t\t\tMAC Address\n-----------------------------------------")

    # received responses
    for client in clients_list:
        print(client["ip"] + "\t\t" + client["mac"])

    print(" ")


# Launch script
os.system('clear')

# Get main IPs
opsys       = check_os()
my_ip       = get_my_ip()
my_mac      = get_current_mac("en0")
router_ip   = get_router_ip(opsys)

print("[+] Your local IP:\t" + my_ip)
print("[+] Your device's MAC:\t" + my_mac)
print("[+] Your router's IP:\t" + router_ip)

# Get network IPs
my_subnet       = my_ip.rpartition('.')[0] + ".1/24"
router_subnet   = router_ip.rpartition('.')[0] + ".1/24"

scan_result = scan_network(my_subnet)
print_clients(scan_result)

if my_subnet != router_subnet:
    scan_result = scan_network(router_subnet)
    print_clients(scan_result)

