---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# LS-lightbox: Software setup

## Setting up a new Raspberry Pi

1. On a computer go to Raspberry Pi’s website https://www.raspberrypi.com/software/ to download and install the Raspberry Pi Imager.

2. In Raspberry Pi Imager, install **Raspberry Pi OS (Legacy)** on the micro SD card.

3. Connect the monitor, keyboard, and mouse to the PI.

4. Insert the micro SD card into the Pi.

5. Connect power to the Pi to boot it up.

6. Follow the setup pages instructions. Connect to the internet, and the perform prompted update on first launch. Note down the username and password you have set.

7. Install Python 3.9.9. 
   
   Reference: [How to Update Python on Raspberry Pi](https://linuxhint.com/update-python-raspberry-pi/)
   
   Enter the following sequence of commands in terminal:
   
   - `wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz`
   
   - `tar -zxvf Python-3.9.9.tgz`
   
   - `cd Python-3.9.9`
   
   - `./configure --enable-optimizations`
   
   - `sudo make altinstall`
   
   - `cd /usr/bin`
   
   - `sudo rm python`
   
   - `sudo ln -s /usr/local/bin/python3.9 python`

8. Check Python version (3.9.9):
   
   `python --version`

9. Modify Pi to run the *ws2811* library. 
   
   Reference: [Connect and Control WS2812 RGB LED Strips via Raspberry Pi](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/)
   
   In terminal:
   
   - `sudo apt-get update`
   
   - `sudo apt-get install gcc make build-essential python-dev git scons swig` (confirm with Y)
   
   - To deactivate audio output, we edit the `.conf` file by:
     
     `sudo nano /etc/modprobe.d/snd-blacklist.conf`
     
     And add this line:
     
     ```
     blacklist snd_bcm2835
     ```
     
     Then save file with CTRL + O.
     
     And close the editor with CTRL + X.
   
   - Edit another `.conf` file:
     
     `sudo nano /boot/config.txt`
     
     Comment out the line
     
     ```
     dtparam=audio=on
     ```
     
     by adding a # in front of it.
     
     Then save file with CTRL + O.
     
     And close the editor with CTRL + X.
   
   - Reboot Pi:
     
     `sudo reboot`

10. Download *rpi_ws281x* library
    
    - `cd`
    
    - `git clone https://github.com/jgarff/rpi_ws281x`

11. We need to modify some lines to specify using SK6812: 
    
    - Using the file explorer, open the `main.c` file found in */home/pi/rpi_ws281x/*
    
    - Line 63 is turned on by default for LED ws2811, so turn it off by adding // at the front.
    
    - Instead, turn on line 64 for SK6812 by deleting the // at the front.
    
    - On line 66, edit it to the number of total numbers of LEDs connected.
    
    - On line 67, edit number to 1.
    
    - Save file.
    
    - Then we compile the library for Python.
      
      In terminal:
      
      `cd rpi_ws281x/`
    
    - `sudo scons`
    
    ```{note}
    Everytime you edit main.c, for example changing the number LED connected, it requires a recompile.
    ```

12. Now the Pi should be ready to control the SK6812 LED strips using our `lightbox.py`

## Create Desktop folder "control"

1. Create a folder in Desktop named _control_

2. Download `lightbox.py` from our Github site(link), and paste it in _Desktop/control_

## Setting up the `lightbox.py` as a systemd service

1. Create a new service file.
   
   In terminal:
   
   `sudo nano /etc/systemd/system/lightbox_failsafe.service`

2. In the editor, paste in the following lines:
   
   ```
   [Unit]
   Description=relaunch lightbox.py when crashed`
   
   [Service]
   User=root
   Group=root
   Type=simple
   ExecStart=sudo /usr/bin/python3 /home/pi/Desktop/control/lightbox.py
   Restart=always
   RestartSec=3
   
   [Install]
   WantedBy=default.target
   ```

3. CTRL + X to close the editor.
   
   When prompted the file name, confirm that it is `lightbox_failsafe.service` and enter Y to save.

4. Refresh the system service files. It may ask for the username and password.
   
   `sudo systemctl daemon-reload`
   
   ```{note}
   Everytime you edit lightbox_failsafe.service, it requires a refresh.
   ```
