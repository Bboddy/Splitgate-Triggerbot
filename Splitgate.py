from PIL import ImageGrab
from ctypes import windll
import time, pyttsx3, win32api

engine = pyttsx3.init()
engine.setProperty("volume", 0.5)
engine.setProperty("rate", 350)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
#Voice welcome
engine.say("Started")
engine.runAndWait()

def GetPixel(x,y):
    image = ImageGrab.grab()
    color = image.getpixel((x, y))
    return color

red = (254, 0, 0)
red2 = (255, 0, 0)

stopShooting = False
paused = True
active = True

def run():
    global paused, stopShooting, active

    #Voice settings
    while active:
        while not paused:
            time.sleep(0.1)
            color = GetPixel(1280 , 720)
            if color == red or color == red2:
                color = GetPixel(1280 , 720)
                stopShooting = True
                #print("Shoot")
                windll.user32.mouse_event(0x0002,0,0,0,0)
            if stopShooting == True:
                windll.user32.mouse_event(0x0004,0,0,0,0)
                stopShooting = False
            if win32api.GetKeyState(0x13) < 0: #Pause
                paused = True
                engine.say("Paused")
                engine.runAndWait()
        if win32api.GetKeyState(0x13) < 0: #Pause
                paused = False
                engine.say("Unpaused")
                engine.runAndWait()
        if win32api.GetKeyState(0x23) < 0: #End 
            engine.say("Exiting")
            engine.runAndWait()
            active = False
            quit()

run()