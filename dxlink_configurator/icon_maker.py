import base64
import os
from Tkinter import *
##The Base64 icon version as a string
icon = \
""" REPLACE THIS WITH YOUR BASE64 VERSION OF THE ICON
"""
icondata= base64.b64decode(icon)
## The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()
root = Tk()
root.wm_iconbitmap(tempFile)
## Delete the tempfile
os.remove(tempFile)