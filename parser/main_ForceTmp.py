# coding: utf8                                      # IMPORTANT(!) for UTF-8 paths

import subprocess                                   # for executing shell commands
import urllib2                                      # for downloading a file
import sys
import os
import webbrowser                                   # for opening HTML file in web browser
import json                                         # for parsing to JSON

# Terminal:
# python parseBGPDump.py http://data.ris.ripe.net/rrc16/2012.03/updates.20120315.1145.gz
# -ODER-
# python parseBGPDump.py updates.20120315.1145.gz


inputFile = 'bgpMRTFormat.txt'
outputFile = 'bgpDump.json'


def openReadFile(file):
    f = open(file, 'r')
    return f

def openWriteFile(file):
    f = open(file, 'w')
    return f
#-----------------------

def main():
    parse()

# this method parses only the ASPATH's and creates a good 'outputFile'
def parse():
    f1 = openReadFile(inputFile)
    file = f1.readlines()
    nodes = ""
    links = ""

    for line in file:
        if '|A|' in line:
            s = line.split("|")
            aspath = s[6].split()
            asn = aspath[0]
            
            # ignore AS-Sets (=AS-Paths that contain '{}')
            if not '{' in line or not '}' in line:
                # iterate through the array 'aspath'
                for i in range(0,len(aspath)):
                    nodes += "{\"asn\" : \"" + aspath[i] + "\"},"
                    
                    # 'target' is a AS
                    if (i != len(aspath)-1):
                        links += "{\"source\" : \"" + aspath[i] + "\", \"target\" : \"" + aspath[i+1] + "\"}"
                    # 'target' is a prefix
                    else:
                        links += "{\"source\" : \"" + aspath[i] + "\", \"target\" : \"" + s[5] + "\"}"
            
                    # current line is not the last line
                    if (line != file[-1]):
                        links += ","
                    # current line is the last line and 'target' is not a prefix
                    elif ((line == file[-1]) and (i != len(aspath)-1)):
                        links += ","
            
                nodes += "{\"prefix\" : \"" + s[5] + "\"}"
                # current line is not the last line
                if (line != file[-1]):
                    nodes += ","

        # current line is the last line and is not an 'Announcement'
        t = line.split("|")
        if ((line == file[-1]) and (t[2] != "A")):
            # remove the last character (which is a comma) from 'nodes' and 'links'
            nodes = nodes[:-1]
            links = links[:-1]

    output = "{\"nodes\":[" + nodes + "], \"links\":[" + links + "]}"
    # intermediate step is needed because of escaped characters
    output = json.loads(output)
    output = json.dumps(output, indent=2)

    # create output file
    f2 = openWriteFile(outputFile)
    f2.write(str(output))
    f2.close()

# call main method
main()
