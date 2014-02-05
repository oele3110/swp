#!/usr/bin/python
import fileinput
import threading
import re
import time


class MyFileinputReader(threading.Thread):

	def __init__(self, asn):
		threading.Thread.__init__(self)
		self.asn = "6500" + str(asn)


	def run(self):

		regexUpdate = "\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} BGP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) rcvd UPDATE w/ attr: nexthop (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}), origin i(, metric \d{1,5})?, path ((\d{1,5}\s?)+)\s"
		regexUpdatePrefix = "\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} BGP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) rcvd (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})"

		regexWithdrawn = "\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} BGP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) rcvd UPDATE about (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}) -- withdrawn"

		logfile = open("/usr/local/quagga/AS" + self.asn + ".log","r")
		loglines = follow(logfile)

		prefixA = None
		pathA = None

		prefixW = None

		for line in loglines:

			print line

			resultUpdate = re.match(regexUpdate, line)
			resultUpdatePrefix = re.match(regexUpdatePrefix, line)

			resultWithdrawn = re.match(regexWithdrawn, line)

			if resultUpdate:
				pathA = "\"" + self.asn + "\",\"" + resultUpdate.group(4).replace(" ", "\",\"") + "\""

			if resultUpdatePrefix:
				prefixA = resultUpdatePrefix.group(2)

			# print json announcement output after prefix and path is read
			if prefixA and pathA:
				output = "{ \"nodes\": [ { \"asn\": \""+self.asn+"\", \"prefix\": [\""+prefixA+"\"], \"type\": \"announcement\", \"path\": [ "+pathA+" ] } ] }\r\n"
				print output
				prefixA = None
				pathA = None

			# print json withdraw output
			if resultWithdrawn:
				prefixW = resultWithdrawn.group(2)
				output = "{ \"nodes\": [ { \"asn\": \""+self.asn+"\", \"prefix\": [\""+prefixW+"\"], \"type\": \"withdraw\", \"path\": [  ] } ] }\r\n"
				print output
				prefixW = None



def follow(thefile):
	thefile.seek(0,2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		yield line




if __name__ == '__main__':
	
	thread1 = MyFileinputReader(1)
	thread2 = MyFileinputReader(2)
	thread3 = MyFileinputReader(3)
	thread4 = MyFileinputReader(4)
	thread5 = MyFileinputReader(5)
	thread6 = MyFileinputReader(6)
	thread7 = MyFileinputReader(7)
	


	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	thread5.start()
	thread6.start()
	thread7.start()



