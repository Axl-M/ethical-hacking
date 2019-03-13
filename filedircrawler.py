#!/usr/local/bin/python3

# Dependencies:
# pip install requests
# pip3 install requests

import requests
import argparse
import sys


def get_arguments():
    # Parse the passed arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="target", help="Subdomain to be analyzed (ex: www.example.com)")

    arguments = parser.parse_args()

    if not arguments.target:
        parser.error("[-] Missing -t argument (--target), please use --help for more details.")

    return arguments


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.InvalidURL:
        print ("\n[-] Invalid URL: " + url)
        pass


options             = get_arguments()
target_url          = options.target
valid_filedirs      = []

try:
    with open("wordlists/files-and-dirs-list.txt", "r") as subdomains_list:
        for line in subdomains_list:
            # time.sleep(0.1)
            filedir     = target_url + "/" + line.strip()
            response    = request(filedir)
            if response and response.status_code != 300:
                print(response.status_code)
                valid_filedirs.append(filedir)
                print("\n[+] Discovered file or directory: " + filedir)
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
        print(valid_filedirs)

except KeyboardInterrupt:
    print("\n")
    print(valid_filedirs)
    print ("\n[-] Quitting filedircrawler.py")