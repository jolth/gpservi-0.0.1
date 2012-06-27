"""
  Module that loads the configuration file
  
  Author: Jorge A. Toro
  Date: 02-02-2012
  
"""

import sys
from ConfigParser import *

_ConfigFile = '../config.cfg'


def load(section, option, archive=_ConfigFile):
  """
    Load variable
  """
  cfg = ConfigParser()
  try:
    cfg.readfp(file(archive))
  except Exception, e:
    sys.stderr.write("%s, %s\n" % (archive, e.strerror))
    return

  try:
    return cfg.get(section, option)
  except:
    sys.stderr.write("Incorrect value for %s or %s parameter\n" % \
    (section, option))
    return

