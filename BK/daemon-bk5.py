# -*- coding: UTF-8 -*-
"""
    Daemons for GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]

    Usage:
    >>> import daemon
    >>> d = daemon.DaemonUDP('', 50007, 256)
    >>> d.start()
    Server run :50007
    >>> d.run()

    >>> d1 = daemon.DaemonTCP('127.0.0.1', 50009, 256)
    >>> d1.start()
    >>> d1.run()

"""
import sys
import socket
import threading
from Log.logFile import createLogFile, logFile
from Load.loadconfig import load

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
        self.server = None # Servidor UDP activo 
        self.running = 1 
        self.thread = None # Hilo actual de la instacia del objeto daemon


    def start(self):
        """
            Prepara el servidor 
        """

        if createLogFile(str(load('FILELOG', 'FILE'))): # Creamos el fichero de Log
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creamos el Socket Server 
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
        # Bucle Principal
        while self.running:
            try:
                data, address = self.server.recvfrom(self.buffering) # Esperamos por un cliente UDP
                self.thread = threading.Thread(target=self.threads, args=(data, address, self.__class__.lock, ))
                self.thread.start()
            except KeyboardInterrupt: 
                sys.stderr.write("\rExit, KeyboardInterrupt\n")
                try:
                    sys.stdout.write("Exit App... \n")
                    self.server.close()
                    self.thread.join() # Esperamos hasta que se termine la ejecución de los hilos
                                       # activos, para terminar la ejecución del programa.
                    raise SystemExit("Se terminaron de ejecutar todos los dispositivos activos en el servidor")
                except AttributeError, NameError: pass

                break # Salimos del bucle principal



    def threads(self, data, address, lock):
        """
            run thread
        """
        import time, random
            
        # Fichero de Log
        lock.acquire(True)
        self.__class__.endfile = logFile(str(load('FILELOG', 'FILE')),
                                         self.__class__.endfile,
                                         address=address, data=data, 
                                        )
        lock.release()
        # End Fichero de Log

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
