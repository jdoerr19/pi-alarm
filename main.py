import utf
import os
import threading
import subprocess
import time

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
    connectToBTSpeaker("50:DC:E7:4F:F1:A2", 2)
    playWakeupFile("50:DC:E7:4F:F1:A2", "/home/pi/hello.wav", 1)
    disconectBTSpeaker()

#checks if the current time matches the specified wakeup time
#uses the time elapsed since epoch to calculate current time
def isTimeForWakeup():
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
WAKEUP_HOUR = 17
WAKEUP_MIN = 1
WAKEUP_SEC = 20

while (True) :
    if (isTimeForWakeup() == True) :
        wakeup()
        break
    else :
        time.sleep(.25)
        


