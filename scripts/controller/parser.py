import sys
import re

# files read out and write to
inputFile = 'bgpMRTFormat.mrt'
outputFile = '../../html/controller/bgpDump.json'

# open readable file
def openReadFile(file):
    f = open(file, 'r')
    return f

# open writable file
def openWriteFile(file):
    f = open(file, 'w')
    return f

#main program
def main():
    	#file_to_json()
	print "main"	

def test():
	print "das ist ein test"

# this method parses announces in MRT format to json NODES ONLY !!!
def file_to_json():
	f1 = openReadFile(inputFile)
	file = f1.readlines()
	parse(file)
	f1.close()

def string_to_json(string):
	lines = string.split("\n")
	parse(lines)

def parse(input_str):
	nodes = {}
	# BGP4MP|03/15/12 11:45:28|A|198.32.124.146|25152| 2.92.137.0/24 |25152 6939 3216 8402|IGP
	regex = ".*\|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})\|(\d{1,5}\s?)*\|.*"
	
	for line in input_str:
		matching = re.match(regex,line)
		if matching:
			asn = matching.group(2)
			prefix = matching.group(1)
			# new asn found, add it
			if not asn in nodes:
				nodes[asn] = []
			# and its prefixes
			if not prefix in nodes[asn]:
				nodes[asn].append(prefix)

	# write data to file in json style 
	output = "{\n\t\"nodes\":[\n"
	for key,val in nodes.items():
		output += "\t\t{\"asn\":\"" + key + "\",\"prefix\":[\"" + "\",\"".join(val) + "\"]},\n"
	output =  output[:-2] + "\n\t],\n\t\"links\":[\n\t]\n}"
	f2 = openWriteFile(outputFile)
	f2.write(str(output))
	f2.close()

def parse_atr(input_str):
	# asn|ip|port|snmp version|community|password|||
	return "parsing atr"

# start
main()
