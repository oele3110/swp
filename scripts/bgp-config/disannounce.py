#!/usr/bin/env python

import sys
import subprocess
import re


def main():
	
	regexIp = "\.1\.3\.6\.1\.4\.1\.8072\.2\.265\.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
	
	if len(sys.argv) < 5:
		print("error, parameter missing")
	else:
		if sys.argv[1] == "-s":
			regexResult = re.match(regexIp, sys.argv[2])
			ip = regexResult.group(1)
			length = sys.argv[4]
			
			prefix = ip + "/" + length
			
			# debug
			"""
			file = open("/home/skims/test.txt","a")
			file.write(ip + "/" +  sys.argv[4] + "\n")
			file.close()
			"""
			
			subprocess.call("/home/skims/disannounce.sh " + prefix, shell=True)

main()


