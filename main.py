import unittest
import os
import threading
import subprocess
import time
import pynput


#global variable used in keyboard listener as callback flag
g_iskeyPressedYet = False
g_keyPressCount= 0

def connectToBTSpeaker(f_deviceID, f_sleepTimeSec) :
    connectResult = subprocess.call(["bluetoothctl", "connect",f_deviceID])
    time.sleep(f_sleepTimeSec)
    return connectResult

def playWakeupFile(f_deviceID, f_fileName, f_sleepTimeSec) :

    deviceString = "--device=bluealsa:DEV="+f_deviceID
    aplayResult = subprocess.call(["aplay",deviceString,f_fileName])
    print(aplayResult)
    time.sleep(f_sleepTimeSec)
    return aplayResult

def disconectBTSpeaker() :
    subprocess.call(["bluetoothctl", "disconnect"])

def wakeup() :
    """Routine to connect to bluetooth speaker, play wakeup file, and disconnect
    The wakeup file is played continously until the user cancel input is received"""

    connectToBTSpeaker("50:DC:E7:4F:F1:A2", 2)

    while (g_keyPressCount < KEY_PRESS_REQUIRED) :
        playWakeupFile("50:DC:E7:4F:F1:A2", "/home/pi/hello.wav", .5)

    disconectBTSpeaker()

def pressReceived(f_key) :
    """keyboard listener callback that sets the global flag so the wakeup routine will
    stop playing the wakeup file
    
    Parameters:
    f_key : the keyboard value pressed by the user

    """

    global g_iskeyPressedYet, g_keyPressCount
    g_keyPressCount += 1
    g_iskeyPressedYet = True
    print(g_keyPressCount)


def isTimeForWakeup():
    """returns true when the current time is equal to to the specified wakeup time
    uses the time elapsed since epoch to calculate current time"""
    timeElpasedSinceEpoch = time.time()
    currentDateTime = time.localtime(timeElpasedSinceEpoch)
    currentHour = currentDateTime.tm_hour
    currentMin = currentDateTime.tm_min
    currentSec = currentDateTime.tm_sec

    if (currentHour == WAKEUP_HOUR and currentMin == WAKEUP_MIN and currentSec == WAKEUP_SEC) :
        return True
    else:
        return False

#hardcoded alarm time
WAKEUP_HOUR = 7
WAKEUP_MIN = 30
WAKEUP_SEC = 0
KEY_PRESS_REQUIRED = 1000

keyListen = pynput.keyboard.Listener(on_press = pressReceived)
keyListen.start()

while (True) :
    if (isTimeForWakeup() == True) :
        g_keyPressCount = 0
        wakeup()
        #reset the flag so the alarm will retrigger next day
        g_iskeyPressedYet = False
    else :
        time.sleep(.25)
        


