import subprocess, sys
import time
from PIL import ImageGrab
import wmi


with subprocess.Popen(["powershell.exe","C:\\Users\\kbalaraman\\Desktop\\windows\\rdp.ps1"]) as f:
    time.sleep(0)
    print (f.pid)
    image = ImageGrab.grab(bbox = None)
    image.save('sc.png')
    subprocess.Popen.kill(f)

