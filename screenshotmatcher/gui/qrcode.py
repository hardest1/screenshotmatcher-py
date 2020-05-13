from wx import (  # pylint: disable=no-name-in-module
  BoxSizer, 
  App, 
  Icon, 
  Menu, 
  Frame, 
  CallAfter, 
  Image,
  EmptyImage,
  Bitmap,
  StaticBitmap,
  NullBitmap,
  ID_ANY,
  EVT_MENU, 
  BITMAP_TYPE_PNG, 
  HORIZONTAL, 
)

from wx.adv import TaskBarIcon # pylint: disable=no-name-in-module
import qrcode

import common.config

def static_bitmap_from_pil_image(caller, pil_image):
  wx_image = Image(pil_image.size[0], pil_image.size[1])
  wx_image.SetData(pil_image.convert("RGB").tobytes())
  bitmap = Bitmap(wx_image)
  static_bitmap = StaticBitmap(caller, ID_ANY, NullBitmap)
  static_bitmap.SetBitmap(bitmap)
  return static_bitmap

class QRCodeFrame(Frame):
  def __init__(self, app, parent, id, title):
    Frame.__init__(self, parent, id, title, (-1, -1), (300, 300))

    sizer = BoxSizer(HORIZONTAL)
    
    img = qrcode.make(common.config.SERVICE_URL)

    static_bitmap = static_bitmap_from_pil_image(self, img)
    sizer.Add(static_bitmap)
    self.SetSizer(sizer)
    self.Centre()
    self.Layout()

