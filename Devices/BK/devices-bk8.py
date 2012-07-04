# -*- coding: utf-8 -*-
#


from UserDict import UserDict


# Clase que actua como un diccionario
class Device(UserDict):
    """ Store """
    def __init__(self, deviceId=None):
        UserDict.__init__(self)
        self['id'] = deviceId


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
            self.dataFile = StringIO.StringIO(data)

            #
            for tag, (position, bit, seek, parseFunc) in self.tagDataANT.items():
                self[tag] = parseFunc(position, bit, seek)

        except: sys.stderr.write('Error Inesperado:', sys.exc_info())
        finally: self.dataFile.close()


class SKPDevice(Device):
    pass
