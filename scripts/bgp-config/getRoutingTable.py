#!/usr/bin/env python

import re
import sys
import getpass
import telnetlib

HOST = "localhost"

def main():
	
	if len(sys.argv) < 2:
		print("error, parameter missing")
	else:
		if sys.argv[1] == "-g":

			regexOid = "(\.1\.3\.6\.1\.4\.1\.8072\.2\.267\.)(\d{1,5})\.(\d{4})"
			
			result = re.match(regexOid, sys.argv[2])
			
			asn = 0
			port = 0
			
			if result:
				asn = result.group(2)
				port = result.group(3)
			else:
				print sys.argv[2]
				print "string"
				print "error"
				return
			

			tn = telnetlib.Telnet(HOST, port)
			
			tn.read_until("AS"+asn+">")
			
			tn.write("show ip bgp\n")
			tn.write("exit\n")
			
			output = tn.read_all()
			
			#output = "K>* 0.0.0.0/0 via 160.45.111.1, eth0\nC>* 127.0.0.0/8 is directly connected, lo\nC>* 160.45.111.0/24 is directly connected, eth0\nC>* 192.168.1.2/32 is directly connected, tap1\nC>* 192.168.1.3/32 is directly connected, tap2\n"
			
			lines = output.split("\r\n")
			
			regex = "\*\>?\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})?\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+\s+\d+\s+.+"
			regexHead = "\s*Network\s*Next\sHop\s*Metric\s*LocPrf\s*Weight\s*Path\s*"
			
			resultStr = ""
			
			for line in lines:
					result = re.match(regex, line)
					resultHead = re.match(regexHead, line)
					if result:
							resultStr += line + "\\n"
					if resultHead:
							resultStr += line + "\\n"

					
			
			print sys.argv[2]
			print "string"
			print resultStr


# start main method
main()
