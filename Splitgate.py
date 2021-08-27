from PIL import Image
from ctypes import windll
import time, pyttsx3, win32api, mss, mss.tools

center_width = int((win32api.GetSystemMetrics(0) / 2) - 2) # Grab monitor width
center_height = int((win32api.GetSystemMetrics(1) / 2) - 2) # Grab monitor height

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
            with mss.mss() as sct: # Mss image grab
                monitor = {"top": center_height, "left": center_width, "width": 4, "height": 4} # Grab 4x4 in center of screen
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX") # Grab image data
                color = img.getpixel((2, 2)) # Grab center pixel's color
            if color == red and not isShooting and not win32api.GetAsyncKeyState(0x01):
                isShooting = True 
                windll.user32.mouse_event(0x0002,0,0,0,0) # Left mouse down
            if isShooting and color != red:
                windll.user32.mouse_event(0x0004,0,0,0,0) # Left mouse Up
                isShooting = False
            if win32api.GetKeyState(0x13) < 0 and paused == False: #0x13 is pause
                paused = True
                engine.say("Paused")
                engine.runAndWait()
        if win32api.GetKeyState(0x13) < 0 and paused == True: #0x13 is pause
                paused = False
                engine.say("Unpaused")
                engine.runAndWait()
        if win32api.GetKeyState(0x23) < 0: #End 
            engine.say("Exiting")
            engine.runAndWait()
            active = False
            quit()

run()