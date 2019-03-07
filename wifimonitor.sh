#!/bin/bash

# This script prints the signal strength of the current WiFi

while true
  do airport -I | grep agrCtlRSSI
  sleep 0.5
done
