import common.utils
import sys

class Config():
    
  APP_NAME = 'Screenshot Matcher'
  ICON_PATH = 'gui/icon.png'
  HOST = common.utils.getCurrentIPAddress()
  PORT = 49049
  SERVICE_URL = 'http://{}:{}'.format(HOST, PORT)
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

  DEFAULT_ALGORITHM = 'SURF'
  CURRENT_ALGORITHM = DEFAULT_ALGORITHM

  IS_DIST = getattr(sys, 'frozen', False)