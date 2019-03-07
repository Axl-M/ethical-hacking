#!/bin/bash
  # Check the current subnet you're connected to
  ifconfig | grep "inet " | grep broadcast

  # Change base address 192.168.1 according to your network.
  for ip in 192.168.1.{1..255};
  do
    (
      ping $ip -c2 &> /dev/null ;
      if [ $? -eq 0 ];
      then
        echo $ip is alive
      fi
)& done
wait
