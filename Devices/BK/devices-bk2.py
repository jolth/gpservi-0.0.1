# -*- coding: utf-8 -*-
#


from UserDict import UserDict


# Clase que actua como un diccionario
class DeviceInfo(UserDict):
    """ Store """
    def __init__(self, deviceId=None, dict=None):
        if dict is not None: UserDict.__init__(self, dict)
        else: UserDict.__init__(self)
        self['id'] = deviceId

