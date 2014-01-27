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
import fileinput
import threading
import Queue

class MyServerProtocol(WebSocketServerProtocol):

   running = True

   def onConnect(self, request):
      print("Client connecting: {0}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")

      while not MyFileinputReader.queue.empty():
         self.sendMessage(MyFileinputReader.queue.get().encode('utf-8'))



   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))

      ## echo back message verbatim
      self.sendMessage(payload, isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {0}".format(reason))
      self.running = False
      print str(self.running)

class MyFileinputReader(threading.Thread):

   queue = Queue.Queue()

   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
      for line in fileinput.input():
         MyFileinputReader.queue.put(line)



if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor

   thread = MyFileinputReader()
   thread.start()

   log.startLogging(sys.stdout)

   factory = WebSocketServerFactory("ws://localhost:5002", debug = False)
   factory.protocol = MyServerProtocol

   reactor.listenTCP(5002, factory)
   reactor.run()

   thread.join()