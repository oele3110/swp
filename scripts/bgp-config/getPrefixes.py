#!/usr/bin/env python

import subprocess
import re

def main():
	
	command = "/home/skims/getPrefixes.sh"
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	
	output = process.communicate()
	
	lines = str(output[0]).split("\n")
	
	regex = "\*\>\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\d+\s+(\d+)\s+.+"
	
	prefixes = []
	
	for line in lines:
		#print line
		result = re.match(regex, line) 
		if result:
			prefixes.append(result.group(1))
	
	for prefix in prefixes:
		print prefix
	
	



# start main method
main()
