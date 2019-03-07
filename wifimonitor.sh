#!/bin/bash
while true
  do airport -I | grep agrCtlRSSI
  sleep 0.5
done
