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

2. In the Raspberry Pi Imager, install **Raspberry Pi OS (Legacy)** on the micro SD card.

3. Connect the monitor, keyboard, and mouse to the PI.

4. Insert the micro SD card into the Pi.

5. Connect power to the Pi to boot it up.

6. Follow the instructions in the setup pages. Connect to the internet, and perform the prompted update on first launch. Note down the username and password that are utilized.

7. Install Python 3.9.9.
   
   OTHER PYTHON IS NOT SUPPORTED
   Reference: [How to Update Python on Raspberry Pi](https://linuxhint.com/update-python-raspberry-pi/)
   
   Enter the following sequence of commands in the terminal:
   
   - `wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz`
   
   - `tar -zxvf Python-3.9.9.tgz`
   
   - `cd Python-3.9.9`
   
   - `./configure --enable-optimizations`
   
   - `sudo make altinstall`
   
   - `cd /usr/bin`
   
   - `sudo rm python`
   
   - `sudo ln -s /usr/local/bin/python3.9 python`

8. Check Python is version (3.9.9):
   
   `python --version`

   ```{attention}
   It must be python 3.9.9
   ```
9. Modify Pi to run the *ws2811* library. 
   
   Reference: [Connect and Control WS2812 RGB LED Strips via Raspberry Pi](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/)
   
   In terminal, enter the following sequence of commands:
   
   - `sudo apt-get update`
   
   - `sudo apt-get install gcc make build-essential python-dev git scons swig` (confirm with Y)
   
   - This command line will open a file editor. To deactivate audio output, edit the `.conf` file by entering the following command:
     
     `sudo nano /etc/modprobe.d/snd-blacklist.conf`
     
     And add this line:
     
     ```
     blacklist snd_bcm2835
     ```
     
     Then save file with CTRL + O.
     
     And close the editor with CTRL + X.
   
   - We also need to edit another `.conf` file:
     
     `sudo nano /boot/config.txt`
     
     When the editor is opened, comment out the following line with a # at the beginning:
     
     ```
     dtparam=audio=on
     ```
     
     i.e.,
     
     ```
     #dtparam=audio=on
     ```
     
     Then save file with CTRL + O.
     
     And close the editor with CTRL + X.
   
   - Reboot Pi by entering the following command:
     
     `sudo reboot`

10. Download *rpi_ws281x* library
    
    - `cd`
    
    - `git clone https://github.com/jgarff/rpi_ws281x`

11. Next, modify some lines to specify using the SK6812 protocol: 
    
    - Using the file explorer, open the `main.c` file found in */home/pi/rpi_ws281x/*
    
    - The line of "STRIP_TYPE  WS2811_STRIP_RGB" is turned on by default for LED ws2811 (should be Line 63), so turn it off by adding // at the front.
    
    - Instead, turn on the line of "STRIP_TYPE  WS6812_STRIP_RGBW" (should be line 64) for SK6812 by deleting the // at the front.
    

    - On the line of "HEIGHT" (should be line 67) edit the number to 1.
    - The value of the line of "WIDTH" is unimportant (should be line 66). Since it is expected that the user will use a different number of LED strips for the moonlight array (two LED strip should suffice) and sunlight/twilight array (likely need more than two LED strips). The different number of LEDs being used for the two arrays are specified in the python file `moonsim_moon.py` and `moonsim_sun.py`, detailed later.
    
    
    - Save file.


    ```{figure} /images/mainc.png
    :name: mainc

    The configuration of the main.c file.
    ```
    
12. Next, compile the library for Python.
      
      In terminal, enter the following commands:
      
      `cd rpi_ws281x/`
    
    - `sudo scons`
   

13. Now the Pi should be ready to control the SK6812 LED strips.

## Setup RTC and time

A real time clock module is optional but recommended. We recommend that the user runs the Pi offline, and instead uses the RTC to keep time. This is because when the Pi is online it will automatically update to the local time. This may use daylight saving time, DST, which can be troublesome. The RTC is also essential if the Pi is used in a location with no internet connection.

1. Install RTC module DS3231 as described in {ref}`content:hardware:assemble`

2. On the Pi, go to the Start menu (top left button) and select > Preferences > Raspberry Pi Configuration > Interfaces > I2C **Enable** > OK

3. Install RTC configurations (Reference: [Real Time Clock Script for Raspberry Pi](https://www.youtube.com/watch?v=MxUbqotDBnM), [Adding a Real Rime Clock to your Raspberry Pi](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi))
    - In terminal enter:
    `wget https://raw.githubusercontent.com/km4ack/pi-scripts/master/rtc && bash rtc'
    - When the terminal returns: "Is the time above correct?", respond accordingly (Y/N).
    - When the terminal returns: "Do you see 68 in the info listed above?", respond accordingly (Y/N). (Note to user: you may see UU instead of 68)
    ```{note}
    This rtc installation works for both DS 1307 or DS 3231 variants RTC chips
    ```
4. Turn off DST by setting the time zone to UTC. In terminal:
    - `sudo raspi-config`
    - Select option 5 **Internationalization Options**
    - Select 12 **Change Time Zone**
    - At the bottom select **None of the above**
    - Select **UTC** and OK

5. To change Pi clock to the user's current time (without DST, even if the user is currently experiencing DST), in terminal:
    - `sudo date -s 'YYYY-MM-DD hh:mm:ss'`
    - Change the above to the user's current time in Year-Month-Day hour:minute:second. Keep the digits format, meaning four digits for the year and two digits for the rest.

6. Copy the time from the Raspberry Pi system to the Hardware RTC:
    - `sudo hwclock -w`
8. To check if RTC is working, enter:
    - `sudo hwclock -rv`
    - The RTC time will be reported.


(content:lightbox:lednumber2)=    
## Desktop folders

1. Download from our Github the _control_moon_ and _control_sun_ folders.
    - _control_moon_ contains `moonsim_moon.py`
    - _control_sun_ contains `moonsim_sunn.py`

2. Move the two folders to the Pi Desktop.

```{note}
In _/control_moon/moonsim_moon.py_, the line LED_PIN = 18 specify the communication with the moonlight LED strip through the **GPIO 18**. _/control_sun/moonsim_sun.py_ controls the sunlight/twilight LED strip through **GPIO 21** instead.
```
(content:systemd)=   
## Setting up systemd service

1. Create a new service file.
   
   In terminal, enter:
   
   `sudo nano /etc/systemd/system/moonsim_moon.service`

2. The file editor will open up a blank file, paste in the following lines:
   
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
```{note}
The line "ExecStart=..." specify the action. Here it is launching the `moonsim_moon.py` with python3 with admin permission. `Restart=always` and `RestartSec=3` are configured to restart moonsim_moon.py within 3 seconds upon closing (i.e., the script crashing).
```

3. Then save file with CTRL + O. CTRL + X to close the editor.
   
   When prompted for the file name, confirm that it is `moonsim_moon.service` and enter Y to save.

4. Refresh the system service files. It may ask for the username and password.
   
   - `sudo systemctl daemon-reload`

5. (Optional) If the user is recreating sunlight and twilight as well, repeat the above steps, from 1 to4, to make another service for _control_sun/moonsim_sun.py_
    
    - For step 1, use a different file name:
    
        ```
       /etc/systemd/system/moonsim_sun.service
        ```
        
    - For step 2, replace the line of `ExecStart=...`  with 
        ```
        ExecStart=sudo /usr/bin/python3 /home/pi/Desktop/control_sun/moonsim.py
        ```

    - For step 3, save the file with name `moonsim_sun.service`
    
   ```{note}
   Everytime a .service file is edited, it requires a refresh (see Step 4).
   ```
(content:lightbox:lednumber3)=    
## Setting LED numbers in `moonsim_moon.py` and `moonsim_sun.py`

- Recall that in {ref}`content:moonsim_moon` and {ref}`content:moonsim_sun`, to generate the `LED_schedule .csv` the specification of the LED array (diode_per_strip and strip_count was specified.
- The total number of LEDs is diode_per_strip multiplied by strip_count. E.g., 144 x 4 = 576

    ```{figure} /images/led_count.png
    :name: led_count

    Specify the line of "LED_COUNT" in `moonsim_sun.py` to 576 when using four daisy-chained 144 LED strips.
    ```
- Edit the line of "LED_COUNT" in `moonsim_moon.py` and `moonsim_sun.py` with the respective total number of LEDs for each array.
- Save the file.


    
    ```{note}
    When changing the number of LEDs number in an array, simply change the corresponding settings in MoonSim schedulers and the moonsim python file. Of course, it will also require a recalibration of the illuminance.
    ```