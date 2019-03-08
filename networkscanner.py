#!/usr/local/bin/python3

import os
import argparse
import scapy.all as scapy


def get_arguments():
    # Parse the passed arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="IP or IP range to scan (defaults to 192.168.0.1/24)")

    arguments = parser.parse_args()

    if not arguments.target:
        # parser.error("[-] Missing -t argument (--target), please use --help for more details.")
        print("\n[-] Target IP not defined, defaulting to IP range 192.168.0.1/24")
        arguments.target = "192.168.0.1/24"

    return arguments


def scan_network(ip):
    print("\n[+] Scanning IP range for connected clients: " + ip)
    # scapy.arping(ip)

    # scapy.ls(scapy.ARP)
    arp_request = scapy.ARP(pdst=ip)
    # print(arp_request.summary())
    # arp_request.show()

    # scapy.ls(scapy.Ether)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    # broadcast.show()

    # combine two packets
    arp_request_broadcast = broadcast/arp_request
    print("\n[+] ARP Request Broadcast packet summary:")
    print(arp_request_broadcast.summary())
    print("\n[+] ARP Request Broadcast packet details:")
    arp_request_broadcast.show()

    # exit()

    # send the packet
    print("\n[+] Sending packets...\n")
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)  # packet, timeout

    # print(answered_list.summary())
    print("[+] Received " + str(len(answered_list)) + " responses:\n")

    clients_list = []
    for answer in answered_list:
        # print(answer[0])  # packet sent
        # print(answer[1].show())  # packet received
        client_dict = {"mac": answer[1].hwsrc, "ip": answer[1].psrc}
        clients_list.append(client_dict)

    return clients_list


def print_clients(clients_list):

    print("IP\t\t\tMAC Address\n-----------------------------------------")

    # received responses
    for client in clients_list:
        print(client["ip"] + "\t\t" + client["mac"])

    print(" ")


os.system('clear')
options     = get_arguments()
scan_result = scan_network(options.target)
print_clients(scan_result)

