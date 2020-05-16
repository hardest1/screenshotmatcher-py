from PIL import Image, ImageDraw
from pystray import Icon, Menu as menu, MenuItem as item
import os

import common.utils

class Tray():

  def __init__(self, app_name):
    self.app_name = app_name
    self.icon = Icon(
        self.app_name,
        icon=self.get_icon(),
        menu=menu(
            item(
                'Show QR code',
                lambda icon: self.onclick_qr()),
            item(
                'Show Results',
                lambda icon: self.onclick_results()),
            menu.SEPARATOR,
            item(
                'Quit',
                lambda icon: self.onclick_quit())))

  def get_icon(self):
    width = 64
    height = 64
    color1 = 'white'
    color2 = 'black'
    result = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(result)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return result
  
  def run(self):
    self.icon.run(self.setup)

  def onclick_quit(self):
    self.icon.stop()

  def onclick_qr(self):
    os.system('python show_qr.py')

  def onclick_results(self):
    common.utils.open_file_or_dir(common.utils.getScriptDir(__file__) + '/../../www/results')

  def setup(self, icon):
    self.icon.visible = True

