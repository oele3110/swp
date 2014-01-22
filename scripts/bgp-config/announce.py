#!/usr/bin/env python

import sys
import subprocess
import re
import telnetlib

HOST = "localhost"

def main():
	
	regexIp = "\.1\.3\.6\.1\.4\.1\.8072\.2\.264\.(\d{1,5})\.(\d{1,4})\.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
	
	if len(sys.argv) < 5:
		print("error, parameter missing")
	else:
		if sys.argv[1] == "-s":
			regexResult = re.match(regexIp, sys.argv[2])
			if regexResult:
				asn = regexResult.group(1)
				port = regexResult.group(2)
				ip = regexResult.group(3)
				length = sys.argv[4]
				
				prefix = ip + "/" + length
				
				tn = telnetlib.Telnet(HOST, port)
			
				tn.read_until("AS"+asn+">")
				
				tn.write("enable\n")
				
				tn.read_until("AS"+asn+"#")
				
				tn.write("conf t\n")
				
				tn.read_until("AS"+asn+"(config)#")
				
				tn.write("router bgp "+asn+"\n")
				
				tn.read_until("AS"+asn+"(config-router)#")
				
				tn.write("network "+prefix+"\n")
				
				tn.write("exit\n")
				
				tn.read_until("AS"+asn+"(config)#")
				
				tn.write("exit\n")
				
				tn.read_until("AS"+asn+"#")
				
				tn.write("exit\n")


main()


