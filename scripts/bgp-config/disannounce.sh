#!/bin/bash


#snmpget -v 2c -c private localhost .1.3.6.1.2.1.1.4.0

(
echo "enable"
#sleep 1;
echo "conf t"
#sleep 1;
echo "router bgp 65001"
#sleep 1;
echo "no network $1"
#sleep 1;
echo -e "exit\r"
#sleep 1;
echo -e "exit\r"
#sleep 1;
#echo "wr"
#sleep 1;
#echo "show ip bgp"
#sleep 1;
echo -e "exit\r"
) | telnet localhost 2001

