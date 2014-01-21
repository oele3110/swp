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
		
			regexOid = "(\.1\.3\.6\.1\.4\.1\.8072\.2\.269\.)(\d{1,5})\.(\d{4})"
			
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
			
			lines = output.split("\n")
			
			# this regex filters all announced prefixes
			regex = "\*\>\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})\s*(0.0.0.0)\s+\d+\s+(\d+)\s+.+"
			
			prefixes = []
			
			for line in lines:
				result = re.match(regex, line) 
				if result:
					prefixes.append(result.group(1))
			
			resultStr = ""
			
			for prefix in prefixes:
				resultStr += prefix + "\\n"
			
			print sys.argv[2]
			print "string"
			print resultStr
			


# start main method
main()
