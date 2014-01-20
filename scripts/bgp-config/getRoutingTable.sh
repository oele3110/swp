#!/bin/bash

(
echo "show ip route"
sleep 1
echo -e "exit\r"
) | telnet localhost 2000
