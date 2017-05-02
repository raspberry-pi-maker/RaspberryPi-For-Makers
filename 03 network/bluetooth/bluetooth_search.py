#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from bluetooth import *

print "performing inquiry..."

def search_service(addr):
    service = find_service(address=addr)
    print service


nearby_devices = discover_devices(duration=20, lookup_names = True)

print "found %d devices" % len(nearby_devices)

for addr, name in nearby_devices:
     print "---- %s - %s -----" % (addr, name)
     search_service(addr)

