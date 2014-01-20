#!/usr/bin/env python

import re
import sys
import getpass
import telnetlib

HOST = "localhost"
PORT = 2001

def main():

	if len(sys.argv) < 2:
		print("error, parameter missing")
	else:
		if sys.argv[1] == "-g":
			
			tn = telnetlib.Telnet(HOST, PORT)
			
			tn.read_until("AS65001>")
			
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
