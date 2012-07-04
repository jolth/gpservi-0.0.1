# -*- coding: utf-8 -*-
#


import StringIO
from UserDict import UserDict


def tagData():
    """
        Toma un punto de partida, cantidad de bit y un punto de 
        referencia para leer los bit( según el método seek() de los fichero).
    """
    return  



# Clase que actua como un diccionario
class Devices(UserDict):
    """ Store """
    def __init__(self, data=None, deviceId=None, dict=None):
        if dict is not None: UserDict.__init__(self, dict)
        else: UserDict.__init__(self)
        if data is not None: self.__parse(data) 
        else: continue()
        self['id'] = deviceId


    def __parse(self, data):


    def deviceANT(self):
        """
            Dispositivo Antares
        """
        data = {    # (position, bit, seek, function)
                    "id" : ( -7, 6, 2, tagData)
                }
            
    def deviceSKP(self):
        """
            Dispositivo SkyPatrol
        """
        pass
