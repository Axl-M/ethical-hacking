#!/bin/bash
#this script enables packet forwarding on your machine to act as man in the middle

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [[ "$machine" = "Mac" ]]
then
    sudo sysctl -w net.inet.ip.forwarding=1
else
    sudo echo 1 > /proc/sys/net/ipv4/ip_forward
fi