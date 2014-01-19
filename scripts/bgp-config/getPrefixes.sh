#!/bin/bash

(
echo "show ip bgp"
sleep 1
echo -e "exit\r"
) | telnet localhost 2001
