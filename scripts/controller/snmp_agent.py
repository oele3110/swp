#!/usr/bin/env python
#snmp
from pysnmp.entity.rfc3413.oneliner import cmdgen

#csv
import csv


#snmp bulk
def bulk(oid):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().bulkCmd(
		cmdgen.CommunityData('public'),
		cmdgen.UdpTransportTarget(('localhost','161')),
		0, 25,
		oid
	)
	if errorIndication:
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[-1][int(errorIndex)-1] or '?')
			)
		else:
			file  = open('../../html/controller/data.csv', "w")
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(["OID","Value"])	

			for rows in varBinds:
				for name, val in rows:
					writer.writerow([name.prettyPrint(), val.prettyPrint()])

			file.close()

#snmp get to csv
def get(oid):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
		cmdgen.CommunityData('public'),
		cmdgen.UdpTransportTarget(('localhost','161')),
		oid
	)
	if errorIndication:
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?')
			)
		else:
			file  = open('../../html/controller/data.csv', "w")
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(["OID","Value"])	

			for name, val in varBinds:
				writer.writerow([name.prettyPrint(), val.prettyPrint()])

			file.close()

#snmp get to string
def get_string(oid):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
		cmdgen.CommunityData('public'),
		cmdgen.UdpTransportTarget(('localhost','161')),
		oid
	)
	if errorIndication:
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?')
			)
		else:
			for name, val in varBinds:
				return [name.prettyPrint(), val.prettyPrint()]

#snmp set
def set(oid, value):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
		cmdgen.CommunityData('private'),
		cmdgen.UdpTransportTarget(('localhost', 161)),
		(oid, value)
	)
	if errorIndication:
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?')
			)
		else:
			file  = open('../../html/controller/data.csv', "w")
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(["OID","Value"])	

			for name, val in varBinds:
				writer.writerow([name.prettyPrint(), val.prettyPrint()])

			file.close()


#snmp walk
def walk(oid):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
		cmdgen.CommunityData('public'),
		cmdgen.UdpTransportTarget(('localhost','161')),
		oid,
		lookupNames=True,
		lookupValues=True
	)
	if errorIndication:
		print(errorIndication)
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?')
			)
		else:
			file  = open('../../html/controller/data.csv', "w")
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(["OID","Value"])	
	
			for rows in varBinds:
				for name, val in rows:
					writer.writerow([name.prettyPrint(), val.prettyPrint()])

			file.close()
			

