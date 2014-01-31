#!/bin/bash


# start zebra daemon
#/usr/local/sbin/zebra -f /etc/quagga/zebra.conf -i /usr/local/quagga/zebra.pi-p 2000 -P 2000 &

# start all bgpd daemons
#bgpd -f /etc/quagga/AS65001.conf -i /usr/local/quagga/AS65001.pid -p 20001 -P 2001 &
#bgpd -f /etc/quagga/AS65002.conf -i /usr/local/quagga/AS65002.pid -p 20002 -P 2002 &
#bgpd -f /etc/quagga/AS65003.conf -i /usr/local/quagga/AS65003.pid -p 20003 -P 2003 &
#bgpd -f /etc/quagga/AS65004.conf -i /usr/local/quagga/AS65004.pid -p 20004 -P 2004 &
#bgpd -f /etc/quagga/AS65005.conf -i /usr/local/quagga/AS65005.pid -p 20005 -P 2005 &
#bgpd -f /etc/quagga/AS65006.conf -i /usr/local/quagga/AS65006.pid -p 20006 -P 2006 &
#bgpd -f /etc/quagga/AS65007.conf -i /usr/local/quagga/AS65007.pid -p 20007 -P 2007 &

bgpd -f /etc/quagga/AS65001.conf -i /usr/local/quagga/AS65001.pid -P 2001 &
bgpd -f /etc/quagga/AS65002.conf -i /usr/local/quagga/AS65002.pid -P 2002 &
bgpd -f /etc/quagga/AS65003.conf -i /usr/local/quagga/AS65003.pid -P 2003 &
bgpd -f /etc/quagga/AS65004.conf -i /usr/local/quagga/AS65004.pid -P 2004 &
bgpd -f /etc/quagga/AS65005.conf -i /usr/local/quagga/AS65005.pid -P 2005 &
bgpd -f /etc/quagga/AS65006.conf -i /usr/local/quagga/AS65006.pid -P 2006 &
bgpd -f /etc/quagga/AS65007.conf -i /usr/local/quagga/AS65007.pid -P 2007 &



# command for starting snmp in debugging mode with pass outprint
#snmpd -f -Lo -Ducd-snmp/pass


