#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jorge A. Toro
#

import socket
import threading
import time

class Device(threading.Thread):
	""" """

	endfile = 0

	def __init__(self, data, address, lock):
        threading.Thread.__init__(self)
        self.data, self.address = data, address
        self.lock = lock


	def run(self):
		self.lock.acquire(True)
		with open('/tmp/gps.log', 'w') as f:
			f.seek(self.__class__.endfile)
			print >> f, time.asctime() + ': ' + repr(self.address)
			print >> f, self.data
			self.__class__.endfile = f.tell() 
			f.close()
		self.lock.release()



if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((socket.gethostbyname(socket.gethostname()), 59000))

	lock = threading.Lock()
	while True:
		try:
			data, address = sock.recvfrom(4096)
			d = Device(data, address, lock)
			d.start()
		except KeyboardInterrupt: 
			break

