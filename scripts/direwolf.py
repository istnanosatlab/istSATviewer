# This is a simple wrapper to launch direwolf
# it will simplify the way the user changes the config file to use direwolf to decode the incoming audio
# It will also launch the tnc script with the correct port

import os
import threading
import time


def checkAudioSink():
    """
    Will check if the required audio Sink is available to launch direwolf
    """

    # need to see if the audio Sink is available
    # audio Sink is called DirewolfSink
    if os.system("pactl list sources short | grep -q 'DireWolfSink'") == 0:
        print("DirewolfSink found")
        return True
    else:
        print("DirewolfSink not found")
        return False


def launchDirewolf():
    """
    Will launch direwolf with the correct config file
    """

    # need to launch direwolf with the correct config file
    # config file is called direwolf.conf
    os.system("parec -d DireWolfSink.monitor | direwolf - -n1 -r 88200 -a5 -p -b16 -B 1200")


def checkSerialPort():
    """
    Will check to see if DireWold serial port is available
    """
    
    # need to see if the serial port is available
    # serial port is called /tmp/kisstnc
    if os.path.exists("/tmp/kisstnc"):
        return True
    else:
        return False 
    

def launchTncScript():
    """
    Will launch the tnc script with the correct port
    it is expected to be launched from the istsatviewer repo
    """

    # need to launch the tnc script with the correct port
    # port is /tmp/kisstnc
    os.system("python3 scripts/tnc_proxy.py /tmp/kisstnc")


def run_in_thread(target):
    """
    Run a function in a new thread.
    """
    thread = threading.Thread(target=target)
    thread.start()
    return thread

if __name__ == '__main__':
    if not checkAudioSink():
        print("\033[91m" + "Error: DirewolfSink not found, exiting..." + "\033[0m")
        exit(1)

    print("Launching Direwolf")
    thread_direwolf = run_in_thread(launchDirewolf)

    time.sleep(5)

    if not checkSerialPort():
        print("\033[91m" + "Error: Serial port not found, exiting..." + "\033[0m")
        exit(1)

    print("Launching TNC in a separate thread")
    thread_tnc = run_in_thread(launchTncScript)

    print("Done closing everything")