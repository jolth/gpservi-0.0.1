# -*- coding: UTF-8 -*-
"""
    Server GPS

    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
import daemon
from Load.loadconfig import load


if __name__ == "__main__":
    server = daemon.DaemonUDP('', 50007, 256)
    server.start()
    server.run()
    
