#!/usr/bin/env python

import subprocess
import re

def main():
	
	command = "/home/skims/swp/scripts/bgp-config/getRoutingTable.sh"
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	
	output = process.communicate()
	
	lines = str(output[0]).split("\n")
	
	regex = "(K|C|S|R|O|I|B|A)\>\*\s(.*)"
	
	
	for line in lines:
		result = re.match(regex, line)
		if result:
			print line
		if "Codes: K - kernel route, C - connected, S - static, R - RIP," in line:
			print line
		if "O - OSPF, I - IS-IS, B - BGP, A - Babel," in line:
			print line
		if "> - selected route, * - FIB route" in line:
			print line + "\n"
	
	



# start main method
main()
