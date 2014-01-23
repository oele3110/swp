#!/bin/bash

/usr/local/sbin/zebra -f /etc/quagga/zebra.conf -i /usr/local/quagga/zebra.pi-p 2000 -P 2000 &
#bgpd -f /etc/quagga/AS65001.conf -i /usr/local/quagga/AS65001.pid -p 20001 -P 2001 &
bgpd -f /etc/quagga/AS65002.conf -i /usr/local/quagga/AS65002.pid -p 20002 -P 2002 &
bgpd -f /etc/quagga/AS65003.conf -i /usr/local/quagga/AS65003.pid -p 20003 -P 2003 &
#snmpd -f -Lo -Ducd-snmp/pass


