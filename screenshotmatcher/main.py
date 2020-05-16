# Import third party modules
import threading
import logging
import time

# Import app config
from common.config import (
    APP_NAME, 
    ICON_PATH,
)

# Import app parts
import gui.tray
import common.utils
from matching.matcher import Matcher
from server.server import Server

# Init Server
server = Server()

# Init Tray
tray = gui.tray.Tray(APP_NAME)

# Start server in different thread
x = threading.Thread(target=server.start, args=(), daemon=True)
x.start()

# Start Tray event loop
tray.run()
