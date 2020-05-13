# Import third party modules
from wx import App
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

# Main App
class MainApp(App):

    def OnInit(self):
        # Initialize tray icon/menu
        self.tray = gui.tray.Tray(self, APP_NAME, ICON_PATH)
        return True

if __name__ == "__main__":

    # Init Server and GUI
    server = Server()
    app = MainApp()
    
    # Start server in different thread
    x = threading.Thread(target=server.start, args=(), daemon=True)
    x.start()

    # Start GUI event loop
    app.MainLoop()
