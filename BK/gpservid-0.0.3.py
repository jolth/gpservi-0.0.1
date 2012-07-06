#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: Jorge A. Toro [jolthgs@gmail.com]
"""

import sys 
#import os
import socket
import threading
import time


FILE = '/tmp/gps.log'
#FILE = 'gps.log'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 59000
SIZE = 256


def createFile(arch):
    """ 
        Create file of Log 
    """
    with open(arch, 'w') as  f:
        if f.tell() == 0: 
            print >> f, 'ID'.center(8), 'IP,Port'.center(24), \
            'Date'.center(12), 'Time'.center(10), \
            'Event'.center(9), 'Latitude'.center(10), \
            'Longitude'.center(12), 'Geocoding'.center(36)
            print >> f, ('-'*6).ljust(8), ('-'*22).ljust(24), \
            ('-'*10).ljust(14), ('-'*8).ljust(10), \
            ('-'*6).ljust(6), ('-'*10).ljust(11), \
            ('-'*10).ljust(12), ('-'*34).ljust(36) 
    return True


class Device(threading.Thread):
    """ 
        Dispositivos GPS 
    """

    endfile = 0

    def __init__(self, data, address, lock):
        threading.Thread.__init__(self)
        self.data, self.address = data, address
        self.lock = lock

    def run(self):
        """
            run
        """
        self.logFile()


    def logFile(self):
        """
           Fichero de Log
        """
        self.lock.acquire(True)
        with open(FILE, 'a+') as f:
            f.seek(self.__class__.endfile)
            #print >> f, f.tell()
            #print >> f, time.asctime() + ': ' + repr(self.address)
            print >> f, ('None').ljust(8), \
            (repr(self.address)).ljust(26), \
            (time.strftime('%D')).ljust(12), \
            (time.strftime("%H:%M:%S")).ljust(10), \
            ('None').ljust(6), ('None').ljust(11), \
            ('None').ljust(12), ('None').ljust(36) 
            #print >> f, self.data
            self.__class__.endfile = f.tell() 
            #f.close()
        self.lock.release()



if __name__ == "__main__":
    #if os.path.exists(FILE) or createFile(FILE):
    if createFile(FILE):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((HOST, PORT))

        lock = threading.Lock()

        print("Servidor %s:%s" % (HOST, PORT)) 

        while 1:
            try:
                data, address = sock.recvfrom(SIZE)
                device = Device(data, address, lock)
                device.start()

            except KeyboardInterrupt: 
                sys.stderr.write("Exit, KeyboardInterrupt\n")
                try:
                    sock.close()
                    device.join() # Esperamos hasta que termine la ejecución del hilo
                                  # para terminar la ejecución del programa.
                except NameError: pass

                break # salimos del bucle principal

            #else:
                #device.join() 
                #sock.close()
                #break
        
