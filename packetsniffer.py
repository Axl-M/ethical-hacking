#!/usr/local/bin/python3

import os
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # Filter: arp, tcp, udp, port 22...


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet)

# Launch script
os.system('clear')
sniff("en0")