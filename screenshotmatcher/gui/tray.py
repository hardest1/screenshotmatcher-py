from wx import App, Icon, Menu, Frame, BITMAP_TYPE_PNG, CallAfter, EVT_MENU # pylint: disable=no-name-in-module
from wx.adv import TaskBarIcon # pylint: disable=no-name-in-module

import gui.qrcode
import common.utils

class Tray(TaskBarIcon):

    def __init__(self, app, app_name, icon_path):
        TaskBarIcon.__init__(self)
        self.app = app
        self.app_name = app_name
        self.SetIcon(Icon(icon_path, BITMAP_TYPE_PNG), app_name)
        self.Bind(EVT_MENU, self.OnTaskbarQR, id=1)
        self.Bind(EVT_MENU, self.OnTaskbarResults, id=2)
        self.Bind(EVT_MENU, self.OnTaskbarClose, id=3)
       

    def CreatePopupMenu(self):
        menu = Menu()
        menu.Append(1, 'Show QR Code')
        menu.Append(2, 'Show Results')
        menu.Append(3, 'Close')
        return menu

    def OnTaskbarQR(self, event):
        # Initialize QR code window
        self.qr_frame = gui.qrcode.QRCodeFrame(self, None, -1, self.app_name)
        self.qr_frame.Show(True)

    def OnTaskbarResults(self, event):
        common.utils.open_file_or_dir(common.utils.getScriptDir(__file__) + '/../../www/results')

    def OnTaskbarClose(self, event):
        if hasattr(self, 'qr_frame') and self.qr_frame:
            CallAfter(self.qr_frame.Destroy)
        self.Destroy()