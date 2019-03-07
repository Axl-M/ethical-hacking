# ethical-hacking
Ethical Hacking Scripts in Python and Shell for OSX

By Angel Diaz (https://twitter.com/entpnomad)

## Quick Start
You will need to install Python3 on your Mac to execute these scripts. You will also need to install Scapy:

https://github.com/secdev/scapy 

### MAC Changer

This script modifies the MAC address for the specified interface.

Usage:

```sh
    $ python3 macchanger.py -i <interface> -m <mac>
```  

Both the --interface and the --mac parameters are optional.


### Network Scanner

This script pings the current network for active devices.

Usage:

```sh
    $ python3 networkscanner.py -t <IP or IP range>
``` 