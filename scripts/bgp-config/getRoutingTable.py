#!/usr/bin/env python

import re
import sys
import getpass
import telnetlib

HOST = "localhost"
PORT = 2000

def main():
	
	if len(sys.argv) < 2:
		print("error, parameter missing")
	else:
		if sys.argv[1] == "-g":
			
			tn = telnetlib.Telnet(HOST, PORT)
			
			tn.read_until("Zebra>")
			
			tn.write("show ip route\n")
			tn.write("exit\n")
			
			output = tn.read_all()
			
			lines = output.split("\n")
			
			regex = "(K|C|S|R|O|I|B|A)\>\*\s(.*)"
			
			resultStr = ""
			
			for line in lines:
					result = re.match(regex, line)
					if result:
							#print line
							resultStr += line + "\n"
					"""
					if "Codes: K - kernel route, C - connected, S - static, R - RIP," in line:
							#print line
							resultStr += line + "\\n"
					if "O - OSPF, I - IS-IS, B - BGP, A - Babel," in line:
							#print line
							resultStr += line + "\n"
					if "> - selected route, * - FIB route" in line:
							#print line + "\n"
							resultStr += line + "\\n\\n"
					"""
			
			print sys.argv[2]
			print "string"
			print resultStr


# start main method
main()
