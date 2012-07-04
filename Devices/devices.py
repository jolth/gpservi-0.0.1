# -*- coding: utf-8 -*-
# Author: Jorge A. Toro
#
import sys
import os
import StringIO
from UserDict import UserDict


def tagData(dFile, position, bit, seek=0):
    """
        Toma un punto de partida (position), cantidad de bit y un punto de 
        referencia para leer los bit(según el método seek() de los fichero).
        Además dataFile el cual es objeto StringIO.
    """
    try:
        dFile.seek(position, seek)
        tagdata =  dFile.read(bit)
    except: sys.stderr.write("Error al obtener el Tag Data")
            
    return tagdata


# Clase que actua como un diccionario
class Device(UserDict):
    """ Store Device"""
    def __init__(self, deviceData=None):
        UserDict.__init__(self)
        self["data"] = deviceData


class ANTDevice(Device):
    """
        Dispositivo Antares
    """
    tagDataANT = {   # (position, bit, seek, function)
                    "id" : ( -7, 6, 2, tagData)
                 }


    def __parse(self, data):
        self.clear()
        try:
            dataFile = StringIO.StringIO(data)
            #
            for tag, (position, bit, seek, parseFunc) in self.tagDataANT.items():
                self[tag] = parseFunc(dataFile, position, bit, seek)

        except: sys.stderr.write('Error Inesperado:', sys.exc_info())
        finally: dataFile.close()


    def __setitem__(self, key, item):
        if key == "data" and item:
            self.__parse(item)
        # Llamamos a __setitem__ de nuestro ancestro
        Device.__setitem__(self, key, item) 

        
    
class SKPDevice(Device):
    """
        Dispositivo Skypatrol
    """
    pass


class HUNTDevice(Device):
    """
        Dispositivo Hunter
    """
    pass



def typeDevice(data):
    """
        Determina que tipo de Dispositivo GPS es dueña de la data.

        Usage:
            >>> import devices
            >>> 
            >>> data='>REV041674684322+0481126-0757378200000012;ID=ANT001<'
            >>> devices.typeDevice(data)
            'ANT'
            >>>
            >>> type(devices.typeDevice(''))
            <type 'NoneType'>
            >>>
            >>> if devices.typeDevice('') is not None: print "Seguir con el programa..."
            ... 
            >>> if devices.typeDevice(data) is not None: print "Seguir con el programa..."
            ... 
            Seguir con el programa...
            >>> 
    """
    # Dispositivos soportados:
    types = ('ANT', 'SKP', 'HUNT')

    typeDev = lambda dat: ("".join(
                            [d for d in types 
                            if dat.find(d) is not -1])
                        )
    return typeDev(data) or None #raise


#
def getTypeClass(data, module=sys.modules[Device.__module__]):
    """
        Determina que clase debe manejar un determinado dispositivo y
        retorna un diccionario con la trama procesada.

        Recibe la data enviada por el dispositivo (data), y opcionalmente 
        el nombre del módulo donde se encuentra la clase que manipula este 
        tipo de dispositivo (module).

        Usage:
            >>> import devices
            >>> 
            >>> data='>REV041674684322+0481126-0757378200000012;ID=ANT001<'
            >>> devices.getTypeClass(data)
            {'data': '>REV041674684322+0481126-0757378200000012;ID=ANT001<', 'id': 'ANT001'}
            >>> 

    """
    # Determinamos la clase manejadora adecuado según el dispositivo
    dev = "%sDevice" % typeDevice(data)

    #return dev
    def getClass(module, dev): 
        """ 
            Retorna una referencia a la clase manejadora. 
            Usage:
            >>> getClass(module, 'ANTDevice')
            <class devices.ANTDevice at 0xb740435c>
            >>> getClass(module, 'SKPDevice')
            <class devices.SKPDevice at 0xb740438c>
            >>> getClass(module, '')
            <class devices.Device at 0xb740426c>
            >>> 
        """
        return hasattr(module, dev) and getattr(module, dev) or Device

    return getClass(module, dev)(data)
     

