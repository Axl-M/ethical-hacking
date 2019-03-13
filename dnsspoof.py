#!/usr/local/bin/python3

# Dependencies:
# pip install scapy
# pip install scapy-http
# pip install netfilterqueue (Linux)


import os
import sys
import subprocess
import netfilterqueue
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


def start_queue(opsys):
    if opsys == "Linux":
        subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
        # subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
        # subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
    else:
        # TO DO: OSX
        subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    print(packet)
    print(scapy_packet.show())
    packet.accept()     # forward packet
    packet.drop()       # cut connection


# Launch script
os.system('clear')
opsys = check_os()
start_queue(opsys)

try:
    # Process queue
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    if opsys == "Linux":
        subprocess.call("iptables --flush", shell=True)
    else:
        # TO DO: OSX
        subprocess.call("iptables --flush", shell=True)
    print ("\n\n[-] Fixing IPTABLES...")
    print ("\n[-] Quitting dnsspoof.py")


