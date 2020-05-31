import socket
import os
import platform
import subprocess

def getCurrentIPAddress():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ipAddr = s.getsockname()[0]
  s.close()
  return ipAddr

def getScriptDir(filename):
  return os.path.dirname(os.path.realpath(filename))
  

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def open_file_or_dir(path):
  if platform.system() == "Windows":
    os.startfile(path)
  elif platform.system() == "Darwin":
    subprocess.Popen(["open", path])
  else:
    subprocess.Popen(["xdg-open", path])