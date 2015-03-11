'''
Parses config file

@author:    Sascha Holzhauer, CESR, Kassel, Germany
@date:    22.06.2011
'''

import ConfigParser
import os.path

configFile = './config/essanl.config'
config = ConfigParser.ConfigParser()
config.read([configFile])


if not os.path.isfile(configFile):
    print "File " + configFile + " not found!"


workingDir = os.path.expanduser(config.get("basic","destination") + "/")
sourceDir = os.path.expanduser(config.get("basic","sourceDir") + "/")
logDir = os.path.expanduser(config.get("basic","logDir"))

user=config.get("basic","username")

replace_unicode_encode_error = config.get("behaviour","replace_unicode_encode_error")