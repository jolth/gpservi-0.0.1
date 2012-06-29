# -*- coding: UTF-8 -*-
"""
    Server GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
import daemon
from Load.loadconfig import load

#print("El fichero de modulos es: %s" % load('MODULES', 'GpsIP'))


if __name__ == "__main__":
    print ("Host: %s" % load('DAEMON', 'DAEMONHost'))
    server = daemon.DaemonUDP(load('DAEMON', 'DAEMONHost'), 50007, 256)
    server.start()
    server.run()
