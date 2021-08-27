from PIL import Image
from ctypes import windll
import time, pyttsx3, win32api, mss, mss.tools

isShooting = False
paused = True
active = True
red = (255, 0, 0)

def run():
    global paused, isShooting, active
    # Voice Settings
    engine = pyttsx3.init()
    engine.setProperty("volume", 0.5)
    engine.setProperty("rate", 350)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    # Voice Welcome
    engine.say("Started")
    engine.runAndWait()

    while active:
        while not paused:
            with mss.mss() as sct:
                monitor = {"top": 1280, "left": 720, "width": 4, "height": 4}
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                color = img.getpixel((2, 2))
            if color == red:
                isShooting = True
                windll.user32.mouse_event(0x0002,0,0,0,0)
            if isShooting == True:
                windll.user32.mouse_event(0x0004,0,0,0,0)
                isShooting = False
            if win32api.GetKeyState(0x13) < 0 and paused == False:
                paused = True
                engine.say("Paused")
                engine.runAndWait()
        if win32api.GetKeyState(0x13) < 0 and paused == True:
                paused = False
                engine.say("Unpaused")
                engine.runAndWait()
        if win32api.GetKeyState(0x23) < 0:
            engine.say("Exiting")
            engine.runAndWait()
            active = False
            quit()

run()