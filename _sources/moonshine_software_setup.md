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

(content:lightbox:software)=
# <span style="font-variant:small-caps;">MoonShine</span>: Software setup
(content:lightbox:lednumber)=
## Setting up a new Raspberry Pi

1. On a computer go to Raspberry Pi’s website https://www.raspberrypi.com/software/ to download and install the Raspberry Pi Imager.

2. In Raspberry Pi Imager, install **Raspberry Pi OS (Legacy)** on the micro SD card.

3. Connect the monitor, keyboard, and mouse to the PI.

4. Insert the micro SD card into the Pi.

5. Connect power to the Pi to boot it up.

6. Follow the setup pages instructions. Connect to the internet, and the perform prompted update on first launch. Note down the username and password being set.

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
   
   - This command line will open a file editor. To deactivate audio output, we edit the `.conf` file by:
     
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
    Everytime main.c is edited, for example changing the number LED connected, it requires a recompile.
    ```

12. Now the Pi should be ready to control the SK6812 LED strips using our `lightbox.py`

## Setup RTC and time

A real time clock module is optional but recommended. We recommend the user to run the Pi offline, and instead use the RTC to keep time. This is because having the Pi connected to the internet may not be possible, and when the Pi is online it will automatically update to the local time (including the troublesome DST).

1. Install RTC module DS3231 as described in {ref}`content:hardware:assemble`

2. On Pi, go to Start menu (top left button) > Preferences > Raspberry Pi Configuration > Interfaces > I2C **Enable** > OK

3. Install RTC configurations (Reference: [Real Time Clock Script for Raspberry Pi](https://www.youtube.com/watch?v=MxUbqotDBnM), [Adding a Real Rime Clock to your Raspberry Pi](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi))
    - In terminal:
    `wget https://raw.githubusercontent.com/km4ack/pi-scripts/master/rtc && bash rtc'
    - Is the time above correct?
    - Do you see 68 in the info listed above? (It may also appear as UU instead of 68, either is fine)
    ```{note}
    This rtc installation works for both DS 1307 or DS 3231 variants RTC chips
    ```
4. Turn off DST by setting the time zone to UTC. In terminal:
    - `sudo raspi-config`
    - Select option 5 **Internationalization Options**
    - Select 12 **Change Time Zone**
    - At the bottom select **None of the above**
    - Select **UTC** and OK

5. To change Pi clock to the user's current time (without DST if the user is currently experiencing DST), in terminal:
    - `sudo date -s 'YYYY-MM-DD hh:mm:ss'`
    - Change the above to the user's current time in Year-Month-Day hour:minute:second. Keep the digits format, meaning four digits for the year and two digits for the rest.

6. Copy the time from the Raspberry Pi system to the Hardware RTC:
    - `sudo hwclock -w`
8. To check if RTC is working:
    - `sudo hwclock -rv`
    - It should report the RTC time.


(content:lightbox:lednumber2)=    
## Desktop folders

1. Download from our Github. the _control_moon_ and _control_sun_ folders.

2. Move them to the Pi Desktop.

```{note}
In _/control_moon/moonsim_moon.py_, the line LED_PIN = 18 specify the communication with the LED strip through the **GPIO 18**. _/controlmoonsim_moonhtbox.py_ controls controls through **GPIO 21** instead.
```

## Setting up systemd service

1. Create a new service file.
   
   In terminal:
   
   `sudo nano /etc/systemd/system/moonsim_moon.service`

2. In the editor, paste in the following lines:
   
   ```
   [Unit]
   Description=relaunch moonsim_moon.py when crashed
   
   [Service]
   User=root
   Group=root
   Type=simple
   ExecStart=sudo /usr/bin/python3 /home/pi/Desktop/control_moon/moonsim_moon.py
   Restart=always
   RestartSec=3
   
   [Install]
   WantedBy=default.target
   ```

3. Then save file with CTRL + O. CTRL + X to close the editor.
   
   When prompted the file name, confirm that it is `moonsim_moon.service` and enter Y to save.

4. Refresh the system service files. It may ask for the username and password.
   
   - `sudo systemctl daemon-reload`

5. (Optional) If the user is recreating sunlight and twilight as well, repeat the above steps to make another service for _control_sun/moonsim_sun.py_
    
    - For step 1, use a different file name:
    
        ```
       /etc/systemd/system/moonsim_sun.service
        ```
        
    - For step 2, replace the line of ExecStart=...  with 
        ```
        ExecStart=sudo /usr/bin/python3 /home/pi/Desktop/control_sun/moonsim.py
        ```

    - For step 3, save the file with name `moonsim_sun.service`
    
   ```{note}
   Everytime a .service file is edited, it requires a refresh.
   ```
