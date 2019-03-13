#!/usr/local/bin/python3

# Dependencies:
# pip install requests
# pip3 install requests

import requests
import argparse
import time
import sys


def get_arguments():
    # Parse the passed arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="Website to be analyzed (ex: example.com)")

    arguments = parser.parse_args()

    if not arguments.target:
        parser.error("[-] Missing -t argument (--target), please use --help for more details.")

    return arguments


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.InvalidURL:
        print ("\n[-] Invalid URL: " + url)
        pass


options             = get_arguments()
target_url          = options.target
valid_subdomains    = []

try:
    with open("wordlists/subdomains-list.txt", "r") as subdomains_list:
        for line in subdomains_list:
            # time.sleep(0.1)
            subdomain   = line.strip() + "." + target_url
            response    = request(subdomain)
            if response:
                valid_subdomains.append(subdomain)
                print("\n[+] Discovered subdomain: " + subdomain)
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
        print(valid_subdomains)

except KeyboardInterrupt:
    print("\n")
    print(valid_subdomains)
    print ("\n[-] Quitting subdomaincrawler.py")