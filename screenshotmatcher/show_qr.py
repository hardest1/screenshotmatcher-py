#!/usr/bin/env python

import PySimpleGUI as sg

from common.config import Config
import qrcode
import sys
import io
    
img = qrcode.make(Config.SERVICE_URL)

bio = io.BytesIO()
img.save(bio, format="PNG")
del img

# All the stuff inside your window.
layout = [[sg.Image(data=bio.getvalue())]]
# Create the Window
window = sg.Window(Config.APP_NAME, layout)


event, values = window.read()

if event in (None, 'Cancel'):   # ifbreak user closes window or clicks cancel
    window.close()

window.close()