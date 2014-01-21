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
		
			regexOid = "(\.1\.3\.6\.1\.4\.1\.8072\.2\.270\.)(\d{1,5})\.(\d{4})"
			
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
			
			tn.write("show ip bgp neighbors\n")
			tn.write("exit\n")
			
			output = tn.read_all()
			
			lines = output.split("\n")
			
			#BGP neighbor is 192.168.1.3, remote AS 65003, local AS 65001, external link

			
			# this regex filters the neighbors
			regex = "BGP neighbor is (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}), remote AS (\d{1,5}), local AS (\d{1,5}), external link"
			
			neighbors = {}
			
			for line in lines:
				result = re.match(regex, line) 
				if result:
					neighbors[result.group(1)] = result.group(2)
			
			resultStr = ""
			
			for neighbor in neighbors:
				resultStr += neighbors[neighbor] + " " + neighbor + "\\n"
			
			print sys.argv[2]
			print "string"
			print resultStr
			


# start main method
main()
