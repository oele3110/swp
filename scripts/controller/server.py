#!/usr/bin/env python

#server
from bottle import redirect, request, route, run, static_file, template

#importing own script
import sys, os
sys.path.append(os.getcwd())
import snmp_agent

import subprocess
import re

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
		IP:</br>
		<input name="ip" type=text/><br/>
		Length:</br>
		<input name="val" type="text"/><br/>
		<input name="Submit" type="submit"/>
		</form>"""

# add ip prefix
# snmpset private 1.3.6.1.4.1.8072.2.264.ip-address int_prefix
# remove ip prefix
# snmpset private 1.3.6.1.4.1.8072.2.265.ip-address int_prefix

@route('/set', method='POST')
def do_set_oid():
	op = request.forms.get('op')

	if op == 'add':
		oid = '.1.3.6.1.4.1.8072.2.264.'
	else:		
		oid = '.1.3.6.1.4.1.8072.2.265.'
	
	ip = request.forms.get('ip')
	length = request.forms.get('val')
	
	#snmp_agent.set(oid+ip, length)
	command = "snmpset -v 2c -c private localhost "+oid+ip+" i "+length
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
		
	#redirect("/table.html")
	output = process.communicate()
	
	regex="(.+\.\d+)\.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\=\sINTEGER\:\s(\d{1,2})"
	result = re.match(regex, output[0]) 
	
	return "oid: "+result.group(1)+" ip: "+result.group(2)+"/"+result.group(3)

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

@route('/config')
def config():
	return """<p><form action="/config" method="post">
		<table>
		  <tr>
		    <td>
		      <textarea name=attacker cols=50 rows=10></textarea>
		    </td>
		    <td>
		      <textarea name=target cols=50 rows=10></textarea>
		    </td>
		  <tr><td><input name=Submit type=submit></td></tr>
		  </tr>
		</table>
		</form></p>"""

#@route('/config', method='POST')
#def change():
	
	



#starting server
HOST, PORT = get_vars()
run(host=HOST,  port=PORT)
