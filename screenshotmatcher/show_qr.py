#!/usr/bin/env python

import PySimpleGUI as sg

import common.config
import qrcode
import sys
import io
    
img = qrcode.make(common.config.SERVICE_URL)

bio = io.BytesIO()
img.save(bio, format="PNG")
del img

# All the stuff inside your window.
layout = [[sg.Image(data=bio.getvalue())]]
# Create the Window
window = sg.Window(common.config.APP_NAME, layout)


event, values = window.read()

if event in (None, 'Cancel'):   # ifbreak user closes window or clicks cancel
    window.close()

window.close()