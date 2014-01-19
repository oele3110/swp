#!/usr/bin/env python

import sys
import subprocess

# import snmp
from pysnmp.entity.rfc3413.oneliner import cmdgen


# this function executes a snmpget at the specified oid and returns its value
def snmpGet(oid):
	cmdGen = cmdgen.CommandGenerator()

	errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		cmdgen.CommunityData('private'),
		cmdgen.UdpTransportTarget(('localhost', 161)),
		oid
	)

	# Check for errors and print out results
	if errorIndication:
		print "error"
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?'
				)
			)
		else:
			for name, val in varBinds:
				return val.prettyPrint()
				#print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# this function returns the prefix at the specified oid
def getPrefix(oid):
	prefix = snmpGet(oid)
	return prefix


def main():
	oid = ""
	if len(sys.argv) < 3:
		print("error, parameter missing")
	else:
		for i in range(1, len(sys.argv)):
			if(sys.argv[i] == "-o"):
				oid = sys.argv[i+1]

	prefix = snmpGet(oid)
	print prefix
	prefix2 = "160.45.114.0/26"
	
	subprocess.call("./hijack.sh " + prefix + " " + prefix2, shell=True)





main()


