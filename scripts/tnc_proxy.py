#!/usr/bin/env python3

from serial import Serial
import base64
import time
import sys
import kiss2 as kiss
import socket
import threading

import click

VERSION = "0.0.1"


#TNC PACCOMM  0.77
# BAUDRATE = 38200

# Add 'D' or 'I' to LOG to change log level
LOG = 'I'

# KISS Special Characters
# http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
# http://k4kpk.com/content/notes-aprs-kiss-and-setting-tnc-x-igate-and-digipeater
# Frames begin and end with a FEND/Frame End/0xC0 byte
KISS_FEND = b'\xC0'  # Marks START and END of a Frame
KISS_FESC = b'\xDB'  # Escapes FEND and FESC bytes within a frame

# Transpose Bytes: Used within a frame-
# "Transpose FEND": An FEND after an FESC (within a frame)-
# Sent as FESC TFEND
KISS_TFEND = b'\xDC'
# "Transpose FESC": An FESC after an FESC (within a frame)-
# Sent as FESC TFESC
KISS_TFESC = b'\xDD'

# "FEND is sent as FESC, TFEND"
# 0xC0 is sent as 0xDB 0xDC
KISS_FESC_TFEND = b''.join([KISS_FESC, KISS_TFEND])

# "FESC is sent as FESC, TFESC"
# 0xDB is sent as 0xDB 0xDD
KISS_FESC_TFESC = b''.join([KISS_FESC, KISS_TFESC])

# KISS Command Codes
# http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
KISS_DATA_FRAME = b'\x00'
KISS_TX_DELAY = b'\x01'
KISS_PERSISTENCE = b'\x02'
KISS_SLOT_TIME = b'\x03'
KISS_TX_TAIL = b'\x04'
KISS_FULL_DUPLEX = b'\x05'
KISS_SET_HARDWARE = b'\x06'
KISS_RETURN = b'\xFF'




def printi(*args, **kwargs):
    if 'I' in LOG:
        return print(*args, **kwargs)


def printd(*args, **kwargs):
    if 'D' in LOG:
        return print(*args, **kwargs)


def tnc_config(sl: Serial):
    sl.write(b'\x03')  # CTRL-C
    sl.write(b'\r')
    sl.write(b'mcon on\r')
    sl.write(b'mcom on\r')
    sl.write(b'monitor on\r')
    sl.write(b'mrpt on\r')
    sl.write(b'trflow on\r')
    sl.write(b'kiss on\r')
    sl.write(b'restart \r')
    sl.flush()
    sl.reset_input_buffer()
    time.sleep(0.250)
    sl.reset_input_buffer()


sockcli = None


def sock_rx(sock: socket.socket, ki: kiss.SerialKISS):
    global sockcli
    buff = bytearray(1024)
    buff_len = len(buff)

    printi('Waiting for clients')

    while True:
        sockcli, addr = sock.accept()
        printi(f'Client connected from {addr}')

        raw = b''
        try:
            while True:
                idx = raw.find(0)
                if idx == -1:
                    raw2 = sockcli.recv(512)
                    if len(raw2) == 0:
                        break

                    raw = raw + raw2
                    continue

                frame_raw = raw[:idx]
                raw = raw[idx + 1:]
                frame = base64.b64decode(frame_raw)

                printi(f'TX frame: {frame.hex()}')
                ki.write(frame)

        finally:
            printi(f'Client disconnected')
            sockcli.close()
            sockcli = None


def on_recv_frame(frame):
    printi(f'RX frame: {frame.hex()}')
    if sockcli is not None:
        frame = frame[1:]
        frame = base64.b64encode(frame) + b'\x00'
        sockcli.send(frame)



def rx(sl: Serial):
    read_buffer = bytes()

    while 1:
        bytes2read = sl.in_waiting if sl.in_waiting > 0 else 1
        data = sl.read(bytes2read)

        if len(data) == 0:
            continue

        printd(f'read_data({len(data)})="data"')

        frames = []

        split_data = data.split(KISS_FEND)
        fends = len(split_data)

        printd(f'split_data(fends={fends})="{split_data}"', fends, split_data)

        # No FEND in frame
        if fends == 1:
            read_buffer += split_data[0]

        # Single FEND in frame
        elif fends == 2:
            # Closing FEND found
            if split_data[0] is not None:
                # Partial frame continued, otherwise drop
                frames.append(b''.join([read_buffer, split_data[0]]))
                read_buffer = bytes()

            # Opening FEND found
            else:
                frames.append(read_buffer)
                read_buffer = split_data[1]

        # At least one complete frame received: [FEND, xxx, FEND]
        elif fends >= 3:

            # Iterate through split_data and extract just the frames.
            for i in range(0, fends - 1):
                buf = bytearray(b''.join([read_buffer, split_data[i]]))
                if buf:
                    printd(f'Frame Found: "{buf}"')
                    frames.append(buf)
                    read_buffer = bytearray()

            # TODO: What do I do?
            if split_data[fends - 1]:
                printd('Mystery Conditional')
                read_buffer = bytearray(split_data[fends - 1])

        # Fixup T3-Micro NMEA Sentences
        frames = list(map(kiss.strip_nmea, frames))
        # Remove None frames.
        frames = [_f for _f in frames if _f]

        # Maybe.
        frames = list(map(kiss.recover_special_codes, frames))

        should_strip_df_start = False
        if should_strip_df_start:
            frames = list(map(kiss.strip_df_start, frames))

        for f in frames:
            yield f


def start(
        serial_port: str,
        baud_rate: int
):
    ki = kiss.SerialKISS(port=serial_port, speed=baud_rate)
    ki.start()

    sl: Serial = ki.interface
    sl.rtscts = True
    sl.timeout = None  # TODO confirm

    tnc_config(sl)
    ki.write_setting('FULL_DUPLEX', b'\0x01')
    printi('Config done')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 6970))
    sock.listen()

    thread = threading.Thread(target=sock_rx, args=(sock, ki), name='sock rx', daemon = True)
    thread.start()

    try:
        while True:
            for frame in rx(sl):
                on_recv_frame(frame)

            # frames = ki.read(32, readmode=False)
            # for f in frames:
            #     on_recv_frame(f)

    finally:
        ki.kiss_off()
        ki.stop()



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
        print('Exiting')
