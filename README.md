# istSatViewer
Simple program that will provide the capability for any user with an SDR to receive and decode messages sent from ISTSat-1. There are two versions, one lighter for Linux users mainly and another using a VM for Windows and Mac OS X users.

For Linux it is  distributed as two docker images that will be run using docker-compose. One image is responsible for running GNURADIO and the other image is responsible for running the software that will decode the messages and print the data to the terminal. Docker was chosen in order to facilitate the development process and make it accessible to anyone. After installing Docker and Docker Compose, with just one command you should be receiving messages from the Satellite.


# Instructions for Windows and Mac OS
In Windows and Mac OS, docker does not support easily sharing the host USB device with the containers. To facilitate installation and guarantee future compatibility, we created a virtual machine (VM) that will contain everything you need to receive and decode messages from the satellite.

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Download the ova file from [here](https://drive.google.com/drive/folders/1FTXfsTDHjU9etDDFKRuVthNt_m1gdBOq?usp=sharing)
3. Open VirtualBox
4. Click on File -> Import Appliance
5. Select the ova file you downloaded (this might take a while to complete, please be patient)
6. Please check that you are sharing the USB device with the virtual machine (this can be done by clicking on the virtual machine -> settings -> USB -> add the SDR device)
6. Start the virtual machine (better to choose Scalled Mode, View -> Host+C) 
8. login with the default username and password (username: isat password: isat)
9. Go to settings and adjust the keyboard layout to match your own

Now you should have everything you need to start receiving messages from the satellite. To start the program, simply open the terminal and run the following command:
```bash
./launcher.sh
```

This will automatically launch the gnuradio script, the decoder, and the server. The default script is configured to work with RTL-SDR. To use PlutoSDR, you need to change the script name in the config file

The config file contains the default values that will be used to launch the gnu radio script and the decoder. If you want to change any of the default values, you can edit this file to suit your needs.

# Instructions Ubuntu

1. Install docker in your system,
    - [Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
2. Install docker compose
    - [Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
3. Clone this repository
4. Open a terminal inside this repository
6. Connect the SDR to your computer
5. run ```docker compose up```
    - if you installed docker compose via apt, it probably installed V1, meaning that you have to run ```docker-compose up``` instead

After this you should any received messages will be shown in your terminal



## Currently Supported Radios

The current supported list of SDRs is:
- PlutoSDR
- RTL-SDR

It is also possible to use a conventional HAM Radio through:
- TNC

the default script is configured to work with RTL-SDR. To use with PlutoSDR, you jaust have to change the docker-compose.yaml to use the correct script
the line is commented, so all you have to do is comment the rtl line and uncomment the pluto line

## TNC support

We have just added TNC support. There is a script called tnc_proxy.py. Which will be the script responsible to communicate with the TNC and send the data to the decoder. Please, make sure that your tnc supports KISS mode.

Also make sure that you change in the config file that you desire to use the TNC script and change the gr-port to 6970. 

The last thing that you should check is that in the tnc_proxy.py script you  have the correct serial port selected and the correct baud rate.

Due to the lack of dependencies, if you are running with docker you will need to run the tnc_proxy.py script locally. You just need to make sure that you have python3 installed and run the following commands: (it is recommended that you comment out the gnuradio service in the docker-compose file to avoid conflicts)

```bash
pip install pyserial
pip install kiss
pip install kiss2
python3 scripts/tnc_proxy.py
```

If you are running in the virtual machine. Please make sure that you change the port and the script in the config file. Make sure that you have passed the usb device to the virtual machine. And make sure that you update the script with the correct serial port and baud rate. After that it should run automatically when you run the launcher.sh script.

After this everything should run smoothly.

ps: when the tnc_proxy.py script starts, you should see the lights on the tnc blink three times

## Operational parameters

**Downlink Frequency**: 145.895 MHz \
**CallSign**: CT6IST 

# Common Errors

```console
gnuradio_nui_1  | Traceback (most recent call last):
gnuradio_nui_1  |   File "istsat_radio_v2/AFSK.py", line 971, in <module>
gnuradio_nui_1  |     main()
gnuradio_nui_1  |   File "istsat_radio_v2/AFSK.py", line 959, in main
gnuradio_nui_1  |     tb = top_block_cls(rx_offset=options.rx_offset, tx_offset=options.tx_offset, uri=options.uri)
gnuradio_nui_1  |   File "istsat_radio_v2/AFSK.py", line 716, in __init__
gnuradio_nui_1  |     self.pluto_source_0 = iio.pluto_source(uri, 145895000-sample_rate/4+rx_offset, 32*sample_rate, 32*sample_rate, 0x8000, True, True, True, "slow_attack", 55, '', True)
gnuradio_nui_1  |   File "/usr/lib/python2.7/dist-packages/gnuradio/iio/iio_pluto_source_swig.py", line 126, in make
gnuradio_nui_1  |     return _iio_pluto_source_swig.pluto_source_make(*args, **kwargs)
gnuradio_nui_1  | RuntimeError: Unable to create context
```

If you see something similar to this means that the container is not able to access the SDR. There could be many issues that could be causing this. Please check that you have the SDR correctly connected and configured for your computer, make sure that you are using the correct ip or correct port.



<details>
For the virtual machine: <br />
    _ install script to launch things; <br />
    _ install configuration fi.e; <br />
    _ install a cool background scene; <br />
    _ check network setup from Pluto; <br />
    _ check port forwarding in network setup; <br />
    _ checl USB forwarding configuration; <br /> 
    _ Review all instructions; <br />
    _ Create a new image; <br />
    _ Upload new image to website.
</details>
