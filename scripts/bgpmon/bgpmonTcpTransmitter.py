#!/usr/bin/python

import socket
import sys
import fileinput

BUFFER_SIZE = 1024
TCP_IP = "0.0.0.0"
TCP_PORT = 5001

def main():

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	
	
	while 1:
		conn, addr = s.accept()
		
		for line in fileinput.input():
			#print line
			conn.send(line)
			
		conn.close()



#start main
main()




