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
(content:launch)=
# <span style="font-variant:small-caps;">MoonShine</span>: Launch procedure

This chapter goes over how to launch _<span style="font-variant:small-caps;">MoonShine</span>_ for the moonlight system (using the moon version of the files, i.e., filenames ending with "moon"). The moon version files include: `moonsim_moon.py` and `LED_schedule_moon.csv` located within *Desktop/control_moon*. And the systemd service `moonsim_moon.service`. Apply the same procedures for launching the sunlight/twilight system, using the sun version of the files, namely `moonsim_sun.py` and `LED_schedule_sun.csv` located within *Desktop/control_sun*. And the systemd service `moonsim_sun.service`.
  
The user should follow all other chapters before peforming a launch. Here we pick up from the software setup section {ref}`content:systemd`, in which a `moonsim_moon.service` that link to the `moonsim_moon.py` located in *Desktop/control_moon* was created.

To start _<span style="font-variant:small-caps;">MoonShine</span>_, instead of launching `moonsim_moon.py` directly the user would launch the `moonsim_moon.service` in terminal. Doing so enables the program relaunches itself upon crashing.

## Requirements

Things to check before the launch:

### 1. Generate a working `LED_schedule_moon.csv`

- On a computer, generate a `LED_schedule_moon.csv` using the <span style="font-variant:small-caps;">MoonSim</span> scheduler, with the  desired parameters. Refers to {ref}`content:moonsim_moon` and {ref}`content:moonsim_sun`. Make sure that the time zone was set correctly, and is a time zone without without daylight saving time (DST). Move the `LED_schedule_moon.csv` into the Raspberry Pi's *Desktop/control_moon/*

- For the `moonsim_moon.py` to run, the `LED_schedule_moon.csv` must contain a row matching the time at launch. Meaning that there cannot be a `LED_schedule.csv` where the first row is a time in the future. So, when creating the `LED_schedule.csv`, _do not_ set the beginning date time ahead of launching _<span style="font-variant:small-caps;">MoonShine</span>_.

- For example, lets say that I am launching <span style="font-variant:small-caps;">MoonShine</span> now at noon but do not want the LED arrays to start the light simulation until midnight. I would still generate a `LED_schedule_moon.csv` by specifying noon as the start time in <span style="font-variant:small-caps;">MoonSim: Moonlight led scheduler</span>. Then open the `LED_schedule_moon.csv` in Excel and edit the rows of LED crude and fine value before midnight to zero. Now I can launch this edited `LED_schedule_moon.csv` and expect it to light up starting at midnight. Between noon, the launch time, and midnight, the simulation will run, but because the LEDs rows have been edited to zero, there will be no illumination.

- For the same reason, the user should never delete entire rows with excel in the middle of the  `LED_schedule.csv`. This will cause errors. If dark periods are required, the user must instead replace the LED illumination value with zeros.

- Check that datetime is in the correct format. See {ref}`content:datetime`

### 2. Check the location of files

- Within *Desktop/control_moon*
  
  - `moonsim_moon.py`
  
  - `LED_schedule_moon.csv`

### 3. Make sure that the LED strips are not frozen

- The LED strip should never freeze during operation. However, it may become unresponsive after the service file is stopped, or other accidents such as a loose connection in the GPIO cable.

- To reset the LED array, unplug both the power and the GPIO cable, and reconnect them. It is advisable to turn off the Pi before disconnecting the power and GPIO connections. 

## To run `moonshine_moon.service`

In terminal,

1. Enable the service file:
   
   `sudo systemctl enable moonshine_moon.service`
   
      ```{note}
      The Raspberry Pi does not have a sleep mode or other energy saving modes, so there is no need to worry about these settings.
      ```
2. To see if the service is active:
    `systemctl list-units --type=service --state=active`
    
```{figure} /images/active_service.png
:name: active_service

A list of active systemd service.
```

2. Check CPU usage:
   
   `htop`
   
```{note}
   Starting 8 sec before the start of every minute, one (two if running two service, both moon and sunlight recreation) of the CPU core will increase usage to 100%. Moonshine_moon.service will be listed as the top task in the list. This is normal.The LED will be be updated at the start of the minute, and CPU usage will return to normal.
```
```{figure} /images/htop.png
:name: htop

Two CPUs at 100% usage just before the start of every minute, as the `moonshine_moon.py` and `moonshine_sun.py` are searching for a matching datetime to the current time. 
```

3. A `log.txt` file will be created in *Desktop/control_moon*. This logs allows the user to check what intensities the first 3 LEDs in the array have been instructed to generate. This file be erased upon restarting the systemd service.

4. To stop the service file (this is the only way to stop _<span style="font-variant:small-caps;">MoonShine</span>_):
   
   `sudo systemctl stop moonshine_moon.service`
   
5. The LED strip will maintain it's last instructed intensity. Run the provided `clear_moon.py` or `clear_sun.py` to turn off the corresponding LED arrays.
    - Place both files on the Desktop
    - In terminal, enter:
    `sudo python3 Desktop/clear_moon.py` OR
    `sudo python3 Desktop/clear_sun.py`

   ```{attention}
   Whenever the Pi is rebooted, `moonshine_moon.service` and `moonshine_sun.service` launchs automatically. Even when the user stop the systemd service, it will start itself upon a reboot.
   ```
   
    ```{attention}
    Sometime the LED array can be "stuck" and is unresponsive after systemd service was stopped (This does not happen when MoonShine is up and running). If the LED array is unresponsive, try unplugging the power cord and GPIO connections to reset it.
    ```