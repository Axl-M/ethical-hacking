#!/bin/bash

# This script prints the signal strength of the WiFi you're currently connected to.

while true
  do airport -I | grep agrCtlRSSI
  sleep 0.5
done
