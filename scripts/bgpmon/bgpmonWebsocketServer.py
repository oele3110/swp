#!/usr/bin/env python

###############################################################################
##
##  Copyright (C) 2011-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

from socket import *
import re
import xml
import xml.dom.minidom as dom
import string
import signal
import sys
from pprint import pprint

startReceive = False

class MyServerProtocol(WebSocketServerProtocol):

   def onConnect(self, request):
      print("Client connecting: {0}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")
      global startReceive
      startReceive = True
      print str(startReceive)

      cli = socket( AF_INET,SOCK_STREAM)
      cli.connect(("livebgp.netsec.colostate.edu", 50001))
      data =""
      msg = ""
      signal.signal(signal.SIGPIPE, signal.SIG_DFL)
      signal.signal(signal.SIGINT, signal.SIG_IGN)
      """
      while startReceive:
         data = cli.recv(1024) #14= </BGP_MESSAGE>
         
         if(re.search('</BGP_MESSAGE>', msg)):
            l = msg.split('</BGP_MESSAGE>', 1)
            bgp_update = l[0] + "</BGP_MESSAGE>"
            bgp_update = string.replace(bgp_update, "<xml>", "")
            d = parse(bgp_update, update, withdrawal)
            msg = ''.join(l[1:])
            for i in d:
               for j in i["prefix"]:
                  path = []
                  for k in i["as_path"]:
                     path.append(str(k.childNodes[0].data))
                  #print j["address"] + " " + j["len"] + " " + i["origin_as"]# + " " + str(i["update"]) + " " + str(i["withdrawal"]) + " " + str(i["count"])# +"\t" + string.join(path, ",")
                  # example output
                  # BGP4MP|03/15/12 11:45:28|A|198.32.124.146|25152|2.92.137.0/24|25152 6939 3216 8402|IGP
                  
                  # update
                  if i["count"] == 0:
                     path = ""
                     
                     counter = 0
                     for node in i["as_path"]:
                        #if str(node.childNodes[0].data) != i["origin_as"]:
                        path = str(node.childNodes[0].data) + path
                        if counter != (len(i["as_path"])-1):
                           path = " " + path
                        counter += 1
                     
                     #print j["address"] + " " + j["len"] + " " + i["origin_as"] + " update " + path
                     print "BGP4MP|01/01/01 00:00:00|A|0.0.0.0|" + i["origin_as"] + "|" + j["address"] + "/" + j["len"] + "|" + path + "|IGP\r"
                     
                  # withdrawn
                  if i["count"] > 0:
                     path = ""
                     counter = 0
                     for node in i["as_path"]:
                        #if str(node.childNodes[0].data) != i["origin_as"]:
                        path = str(node.childNodes[0].data) + path
                        if counter != (len(i["as_path"])-1):
                           path = " " + path
                        counter += 1
                     #print j["address"] + " " + j["len"] + " " + i["origin_as"] + " withdrawn " + path
                     print "BGP4MP|01/01/01 00:00:00|W|0.0.0.0|" + i["origin_as"] + "|" + j["address"] + "/" + j["len"] + "|" + path + "|IGP\r"
               
         msg += str(data)
         """

      self.sendMessage("test".encode('utf-8'))
      
   """
   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))

      ## echo back message verbatim
      self.sendMessage(payload, isBinary)
   """

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))
      global startReceive
      startReceive = False
      print str(startReceive)

def parse(xml, update, withdrawal): 
   l = [] 
   try:
      tree = dom.parseString(xml)
   except xml.parsers.expat.ExpatError:
      print >> sys.stderr, xml
      return []

   d = {}
   for i in tree.firstChild.childNodes: 
      if i.nodeName == "ASCII_MSG": 
         schluessel = wert = None
         for elems in i.childNodes: 
            if elems.nodeName == "UPDATE": 
               if elems.firstChild.nodeName == "WITHDRAWN":
                  count = int(elems.firstChild.getAttribute("count"))
                  if ((update and withdrawal) or ((count == 0) and not withdrawal and update) or ((count > 0) and not update and withdrawal)):
                     #print "count: " + str(count) + "\tupdate: " + str(update) + "\twithdrawal: " + str(withdrawal)
                     d["update"] = update
                     d["withdrawal"] = withdrawal
                     d["count"] = int(elems.firstChild.getAttribute("count"))
                     for update in elems.childNodes: 
                        if(update.nodeName == "NLRI"):
                           for nlri in update.childNodes:
                              if(nlri.nodeName == "PREFIX"):
                                 for prefix in nlri.childNodes:
                                    if(prefix.nodeName == "ADDRESS"):
                                       for txt in prefix.childNodes:
                                          s = txt.data.split("/")
                                          if not "prefix" in d:
                                             d["prefix"] = []
                                          p = {}
                                          p["address"] =  s[0]
                                          p["len"] = s[1]
                                          d["prefix"].append(p)
                        if(update.nodeName == "PATH_ATTRIBUTES"):
                           for pattr in update.childNodes:
                              if(pattr.nodeName == "ATTRIBUTE"):
                                 for pattr in pattr.childNodes:
                                    if(pattr.nodeName == "AS_PATH"):
                                       for asPath in pattr.childNodes:
                                          if(asPath.nodeName == "AS_SEG"):
                                             length =  int(asPath.getAttribute("length"))
                                             origin_as = asPath.childNodes[length-1]
                                             d['as_path'] = asPath.childNodes
                                             d["origin_as"] = str(origin_as.childNodes[0].data)
         break;
   if("prefix" in d):
      l.append(d)
   return l

if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:5002", debug = False)
   factory.protocol = MyServerProtocol

   reactor.listenTCP(5002, factory)
   reactor.run()
