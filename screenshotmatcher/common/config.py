import common.utils
import sys
import hashlib
import platform
import random


def createIdentifier(data):
  h = hashlib.new('sha1')
  h.update(data.encode())
  return h.hexdigest()

identifier = ""

try:
  with open('id', 'r') as f:
    identifier = f.read()
except:
  with open('id', 'w') as f:
    data_for_encoding = "{}-{}".format( platform.platform(), random.randrange(1000000, 9999999) )
    identifier = createIdentifier( data_for_encoding )
    f.write(identifier)

class Config():

  IDENTIFIER = identifier

  APP_NAME = 'Screenshot Matcher'
  ICON_PATH = 'gui/icon.png'
  HOST = common.utils.getCurrentIPAddress()
  PORT = 49049
  SERVICE_URL = 'http://{}:{}'.format(HOST, PORT)
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

  DEFAULT_ALGORITHM = 'SURF'
  CURRENT_ALGORITHM = DEFAULT_ALGORITHM

  IS_DIST = getattr(sys, 'frozen', False)