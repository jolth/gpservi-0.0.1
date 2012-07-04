# -*- coding: utf-8 -*-
#
"""

>>> import devices
>>> 
>>> f = devices.DeviceInfo('ANT001', {'lat':'-122344', 'long':'0455636', 'vel':'30'}) 
>>> f
{'id': {'lat': '-122344', 'vel': '30', 'long': '0455636'}}
>>>

"""

#from UserDict import UserDict


# Clase que actua como un diccionario
class DeviceInfo(dict):
    """ Store """
    def __init__(self, data=None, deviceId=None):
        self['id'] = deviceId

