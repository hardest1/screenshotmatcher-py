import common.utils

APP_NAME = 'Screenshot Matcher'
ICON_PATH = 'gui/icon.png'
HOST = common.utils.getCurrentIPAddress()
PORT = 49049
SERVICE_URL = 'http://{}:{}'.format(HOST, PORT)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}