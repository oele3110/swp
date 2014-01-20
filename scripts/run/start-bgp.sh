#!/bin/bash

bgpd -f /etc/quagga/AS65002.conf -i /usr/local/quagga/AS65002.pid -p 20002 -P 2002 &
bgpd -f /etc/quagga/AS65003.conf -i /usr/local/quagga/AS65003.pid -p 20003 -P 2003 &


