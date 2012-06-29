# -*- coding: UTF-8 -*-
"""
    Daemons for GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]

    usage:
    >>> import daemon
    >>> d = daemon.DaemonUDP('', 50007, 256)
    >>> d.start()
    Server run :50007
    >>> d.run()

    >>> d1 = daemon.DaemonTCP('127.0.0.1', 50009, 256)
    >>> d1.start()
    >>> d1.run()

"""
import socket
import threading


class DaemonUDP:
    """
        Server UDP
    """
    endfile = 0
    lock = threading.Lock()

    def __init__(self, host, port, buffering):

        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None
        self.running = 1

        self.thread = None


    def start(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind((self.host, self.port))
            print ("Server run %s:%s" % (self.host, self.port))
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket:", message 
            sys.exit(1)

        
    def run(self):
        """ 
            threading 
        """
        while self.running:
            data, address = self.server.recvfrom(self.buffering)
            self.thread = threading.Thread(target=self.threads, args=(data, address, self.__class__.lock, ))
            self.thread.start()


    def threads(self, data, address, lock):
        """
            run thread
        """
        import time, random
        #print "Data: " + data, "ADDR: " + address, "Nombre Hilo: " + self.server.getName(), "Lock: " + lock
        print "Data: " + data, "Nombre Hilo: " + self.thread.getName(), "Lock: " + str(lock)
        print "Hilo actual: ", threading.currentThread()
        print "Hilos presentes:",  threading.enumerate()

        time.sleep(random.randint(1, 10))


class DaemonTCP:
    """
        Server TCP

    """
    def __init__(self, host, port, buffering):
        self.host = host
        self.port = port
        self.buffering = buffering
        self.server = None

    def start(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.server.bind((self.host,self.port)) 
            self.server.listen(5) 
            print ("Server run %s:%s" % (self.host, self.port))
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket:", message 
            sys.exit(1)

        
    def run(self):
        pass
