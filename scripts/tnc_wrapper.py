# This is a simple wrapper to launch direwolf
# it will simplify the way the user changes the config file to use direwolf to decode the incoming audio
# It will also launch the tnc script with the correct port

import os
import threading
import time
import click 

VERSION = "0.0.2"


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
    If you want to run with a custom audio input, make sure that you change "DireWolfSink.monitor" to the correct audio input
    """

    # need to launch direwolf with the correct config file
    # config file is called direwolf.conf
    os.system("parec -d DireWolfSink.monitor | direwolf - -n1 -r 88200 -a5 -p -b16 -B 1200")


def checkSerialPort(
        serial_port: str
):
    """
    Will check to see if DireWold serial port is available
    """
    
    # need to see if the serial port is available
    # serial port is called /tmp/kisstnc
    if os.path.exists(serial_port):
        return True
    else:
        return False 
    

def launchTncScript(*args, **kwargs):
    """
    Will launch the tnc script with the correct port
    it is expected to be launched from the istsatviewer repo
    """

    # need to launch the tnc script with the correct port
    os.system(f"python3 scripts/tnc_proxy.py --serial-port {args[0]} --baud-rate {args[1]}")


def run_in_thread(target, *args, **kwargs):
    """
    Run a function in a new thread.
    """
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.start()
    return thread


def start(
        serial_port: str,
        baud_rate: int
):
    if not checkAudioSink():
        print("\033[91m" + "Error: DirewolfSink not found, exiting..." + "\033[0m")
        exit(1)

    # only launch direwolf if the serial port is /tmp/kisstnc
    if (serial_port == "/tmp/kisstnc"):
        print("Launching Direwolf")
        thread_direwolf = run_in_thread(launchDirewolf)

    time.sleep(5)

    if not checkSerialPort(serial_port):
        print("\033[91m" + f"Error: Serial port {serial_port} not found, exiting..." + "\033[0m")
        exit(1)

    print("Launching TNC in a separate thread")
    thread_tnc = run_in_thread(launchTncScript, serial_port, baud_rate)

    print("Done closing everything")




@click.command()
@click.option(
    "--serial-port", type=str, default="/dev/ttyACM0", help="Serial port to talk to tnc. for direwolf use /tmp/kisstnc"
)
@click.option(
    "--baud-rate",
    type=int,
    default=9600,
    help="baud rate of the serial port"
)
@click.version_option(version=VERSION)

def main(*args, **kwargs):
    print(args, kwargs)
    start(*args, **kwargs)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\033[91m" + "Exiting..." + "\033[0m")
        exit(1)
    except Exception as e:
        print("\033[91m" + "Error: " + str(e) + "\033[0m")
        exit(1)
    finally:
        print("\033[91m" + "Exiting..." + "\033[0m")
        exit(1)