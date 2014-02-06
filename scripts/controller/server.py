#!/usr/bin/env python

#server
from bottle import redirect, request, route, run, static_file, template

#importing own script
import sys, os
sys.path.append(os.getcwd())
import snmp_agent
import parser

import subprocess
import re
import csv

def get_vars():
	host = 'localhost'
	port = 8000
	n = len(sys.argv)
	if n > 4:
		for i in range(1,n):
			if sys.argv[i] == "-h":
				host = sys.argv[i+1]
			if sys.argv[i] == "-p":
				port = int(sys.argv[i+1])
		return (host, port)
	else:
		return (host, port)

#data.csv
@route('/<filename>')
def get_file(filename):
	return static_file(filename, root='../../html/controller')	

#snmp bulk
@route('/bulk')
def bulk_oid():
	return """<p><form action="/bulk" method="post">
		Bulk OID:</br>
		<input name="oid" type="text"/><br/>
		<input name="Submit" type="submit"/>
		</form>"""

@route('/bulk', method='POST')
def do_bulk_oid():
	snmp_agent.bulk(request.forms.get('oid'))
	redirect("/table.html")

#snmp get
@route('/')
def index():
	redirect("/demo.html")

@route('/get')
def get_oid():
	return """<p><form action="/get" method="post">
		Get OID:</br>
		<input name="oid" type="text"/><br/>
		<input name="Submit" type="submit"/>
		</form>"""

@route('/get', method='POST')
def do_get_oid():
	snmp_agent.get(request.forms.get('oid'))
	redirect("/table.html")

#snmp set
@route('/set')
def set_oid():
	return """<p><form action="/set" method="post">
		<input type=radio name=op value=add checked> Add Prefix<br/>
		<input type=radio name=op value=del/> Del Prefix<br/>	
		ASN:</br>
		<input name="asn" type=text/><br/>
		Port:</br>
		<input name="port" type=text/><br/>
		IP:</br>
		<input name="ip" type=text/><br/>
		Length:</br>
		<input name="val" type="text"/><br/>
		<input name="Submit" type="submit"/>
		</form>"""


# add ip prefix
# snmpset private 1.3.6.1.4.1.8072.2.264.ip-address length
# remove ip prefix
# snmpset private 1.3.6.1.4.1.8072.2.265.ip-address length

@route('/set', method='POST')
def do_set_oid():
	#not possible because of missing type definition
	#snmp_agent.set(oid+ip, length)
	#redirect("/table.html")

	op = request.forms.get('op')

	if op == 'add':
		oid = '.1.3.6.1.4.1.8072.2.264'
	else:		
		oid = '.1.3.6.1.4.1.8072.2.265'
	
	ip = request.forms.get('ip')
	length = request.forms.get('val')
	_asn = request.forms.get('asn')
	_port = request.forms.get('port')

	command = "snmpset -v 2c -c private localhost "+oid+"."+_asn+"."+_port+"."+ip+" i "+length
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
		
	output = process.communicate()
	
	regex="(.+\.\d+)\.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\=\sINTEGER\:\s(\d{1,2})"
	result = re.match(regex, output[0]) 

	file  = open('../../html/controller/data.csv', "w")
	writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(["OID","Value"])
	writer.writerow([result.group(1),result.group(2)+"/"+result.group(3)])
	file.close()

	redirect("/table.html")

#snmp walk
@route('/walk')

def walk_oid():
	return """<p><form action="/walk" method="post">
		Get OID:</br>
		<input name="oid" type="text"/><br/>
		<input name="Submit" type="submit"/>
		</form>"""

@route('/walk', method='POST')
def do_walk_oid():
	snmp_agent.walk(request.forms.get('oid'))
	redirect("/table.html")

@route('/mrt')
def get_mrt():
	return """<p><form action="/config" method="post">
		      <textarea name=mrt cols=100 rows=15></textarea><br/>
		      <input name="Submit" type="submit">
		</form></p>"""

@route('/mrt', method='POST')
def parse_mrt():
	parser.string_to_json(request.forms.get('mrt'))
	redirect("/demo.html")

@route('/attacker')
def get_attacker():
	return """<p>ASN | IP | SNMP_VERSION | PORT | COMMUNITY | PASSWORD<br/>
			<form action="/attacker" method="post">
			<textarea name=atr cols=100 rows=15></textarea><br/>
			<input name="Submit" type="submit">
		</form></p>"""

@route('/attacker', method='POST')
def parse_attacker():
	return "parsing attacker: "+request.forms.get('atr')
	
@route('/demo/get', method='POST')
def demo_get():
	response = snmp_agent.get_string(request.forms.get('oid'))
	return response[1][:-2]

@route('/demo/set', method='POST')
def demo_set():
	#not possible because of missing type definition
	#snmp_agent.set(oid+ip, length)
	#redirect("/table.html")

	op = request.forms.get('op')
	if op == 'add':
		oid = '.1.3.6.1.4.1.8072.2.264'
	else:		
		oid = '.1.3.6.1.4.1.8072.2.265'
	ip = request.forms.get('ip')
	length = request.forms.get('val')
	_asn = request.forms.get('asn')
	_port = request.forms.get('port')

	command = "snmpset -v 2c -c private localhost "+oid+"."+_asn+"."+_port+"."+ip+" i "+length
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	
	output = process.communicate()
	
	regex="(.+\.\d+)\.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\=\sINTEGER\:\s(\d{1,2})"
	result = re.match(regex, output[0]) 


#starting server
HOST, PORT = get_vars()
run(host=HOST,  port=PORT)
