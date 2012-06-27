#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Jorge A. Toro
"""
import socket
import threading
import time

class Device(threading.Thread):
    """
        Devices
    """

    endfile = 0

    def __init__(self, data, address, lock):
        threading.Thread.__init__(self)
        self.data, self.address = data, address
        self.lock = lock

    def run(self):
       pass 

    def __logFile(self):
        """
            Fichero de Log
        """
        self.lock.acquire(True)
        with open('/tmp/gps.log', 'w') as arch:
            arch.seek(self.__class__.endfile)
            print >> arch, time.asctime() + ': ' + repr(self.address)
            print >> arch, self.data
            self.__class__.endfile = arch.tell() 
            arch.close()
        self.lock.release()



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((socket.gethostbyname(socket.gethostname()), 59000))

    lock = threading.Lock()
    while True:
        try:
            data, address = sock.recvfrom(1024)
            d = Device(data, address, lock)
            d.start()
        except KeyboardInterrupt: 
            break

