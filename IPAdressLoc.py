#!/usr/bin/python3.8

#pré-requis:
#pip install geocoder
#pip install pyfiglet (module Ascii)

import pyfiglet
import geocoder
import socket

ascii_banner = pyfiglet.figlet_format("IP Location")
print(ascii_banner)

g = geocoder.ipinfo('me')
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("Votre hostname est",hostname)
print("Votre IP Publique est",g.ip)
#print("Votre IP Privée est",local_ip)
print("Vos latitude et longitude sont",g.latlng)
print("Votre ville est",g.city)
