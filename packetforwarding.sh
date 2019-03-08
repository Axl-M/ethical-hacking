#!/bin/bash

#this command enables packet forwarding on your machine to act as man in the middle

# for Linux:
# sudo echo 1 > /proc/sys/net/ipv4/ip_forward

# for OSX:
sudo sysctl -w net.inet.ip.forwarding=1