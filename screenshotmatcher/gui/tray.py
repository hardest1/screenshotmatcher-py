from PIL import Image, ImageDraw
from pystray import Icon, Menu as menu, MenuItem as item
import os
import subprocess
import platform
import common.utils
from common.config import Config

class Tray():

  def __init__(self, app_name):
    self.app_name = app_name

    self.ALGORITHM_STATE = Config.CURRENT_ALGORITHM

    self.icon = Icon(
        self.app_name,
        icon=self.get_icon(),
        menu=menu(
            item(
                'Matching Algorithm',
                lambda icon: None,
                enabled=False),
            item(
                'SURF (Precise)',
                self.set_state('SURF'),
                checked=self.get_state('SURF'),
                radio=True),
            item(
                'ORB (Fast)',
                self.set_state('ORB'),
                checked=self.get_state('ORB'),
                radio=True),
            menu.SEPARATOR,
            item(
                'Show QR code',
                lambda icon: self.onclick_qr()),
            item(
                'Open Results Dir',
                lambda icon: self.onclick_results()),
            menu.SEPARATOR,
            item(
                'Quit',
                lambda icon: self.onclick_quit())))
  
  def set_state(self, v):
    def inner(icon, item):
      self.ALGORITHM_STATE = v
      print('Switching Algorithm to %s' % self.ALGORITHM_STATE)
      Config.CURRENT_ALGORITHM = self.ALGORITHM_STATE
    return inner

  def get_state(self, v):
    def inner(item):
      return self.ALGORITHM_STATE == v
    return inner

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

  def onclick_test(self):
    print(Config.CURRENT_ALGORITHM)
    print(self.testvar)

  def onclick_switch_algo(self):
    Config.CURRENT_ALGORITHM = ':-)'
    self.testvar = ':-)'
    self.icon.stop()
    self.icon.run(self.setup)

  def onclick_qr(self):
    if platform.system() == 'Linux':
      os.system('python3 show_qr.py')
    else:
      subprocess.run('show_qr.py', shell=True)
    

  def onclick_results(self):
    common.utils.open_file_or_dir(common.utils.getScriptDir(__file__) + '/../../www/results')

  def setup(self, icon):
    self.icon.visible = True

