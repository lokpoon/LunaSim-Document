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

# <span style="font-variant:small-caps;">MoonShine</span>: Launch procedure

If the user is recreating sunlight and twilight, applies information in this chapter with the sunlight and twilight version of _<span style="font-variant:small-caps;">MoonShine</span>_. Which involves `moonsim_sun.py` and `LED_schedule_sun.csv` located within *Desktop/control_moon*. And `moonsim_sun.service`.
  
By the end of the previous section{ref}`content:lightbox:software`, a `moonsim_moon.service` that link to the `moonsim_moon.py` located in *Desktop/control_moon* was created. Instead of launching `moonsim_moon.py` directly, the user would launch the `moonsim_moon.service` so that the program relaunches itself upon crashing.

## Requirements

Things to check before the launch:

### 1. Generate a working `LED_schedule_moon.csv`

- On a computer, generate a `LED_schedule_moon.csv` with the <span style="font-variant:small-caps;">MoonSim</span> scheduler, with the  desired parameters. Refers to {ref}`content:moonsim_moon` and {ref}`content:moonsim_sun`. Make sure that the time zone was set correctly, and is a time zone without DST. Move the `LED_schedule_moon.csv` into the Pi's *Desktop/control_moon/*

- For the `moonsim_moon.py` to run, the `LED_schedule_moon.csv` must contain a row matching the time at launch. Meaning that there cannot be a `LED_schedule.csv` where the first row is a time in the future. So, when creating the `LED_schedule.csv`, _do not_ set the beginning date time ahead of launching _<span style="font-variant:small-caps;">MoonShine</span>_.

- For example, lets say that I am launching <span style="font-variant:small-caps;">MoonShine</span> now at noon but do not want it to light up until midnight. I would still generate a `LED_schedule_moon.csv` by specifying noon as the start time in <span style="font-variant:small-caps;">MoonSim: Moonlight led scheduler</span>. Then open the `LED_schedule_moon.csv` in Excel and edit the rows of LED crude and fine value before midnight to zero. Now I can launch this edited `LED_schedule_moon.csv` and expect it to light up starting at midnight.

- It also means that the user should never delete entire rows with excel in the middle of the  `LED_schedule.csv`.

### 2. Check the location of files

- Within *Desktop/control_moon*
  
  - `moonsim_moon.py`
  
  - `LED_schedule_moon.csv`

### 3. Make sure that the LED strips are not frozen

- The LED strip should never be frozen during operation. However, it may become unresponsive after the service file is stopped, or other accidents such as lose connection of the GPIO cable.

- We recommend resetting the LED strip before every launch, by unplugging both the power and the GPIO cable, and reconnecting them. It is advisable to turn off the Pi before disconnecting the power and GPIO connections. 

## To run `moonshine_moon.service`

In terminal,

1. Enable the service file:
   
   `sudo systemctl enable moonshine_moon.service`
   
      ```{note}
      The Raspberry Pi does not have sleeping or other enery saving mode, so no need to worry about these settings.
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
   Starting 8 sec before the start of every minutes, one (two if running two service, both moon and sunlight recreation) of the CPU core will increase usage to 100%. moonshine_moon.service would be listed as the top task in the list. The LED will be be updated a the start of the minute, and CPU usage will return to normal.
```
```{figure} /images/htop.png
:name: htop

Two CPU at 100% usage just before the start of every minute, as the `moonshine_moon.py` and `moonshine_sun.py` are serching for a matching datetime to the current time. 
```

3. A `LED_history.log` file will be created in *Desktop/control*. This logs allows the user to check what intensities the first 10 LEDs in the array have been instructed to output.

4. To stop the service file:
   
   `sudo systemctl stop moonshine_moon.service`
   
   ```{note}
   The LED strip will maintain it's last instructed intensity. Unplug the power cord and GPIO connection to reset it.
   ```
   
   ```{note}
   Whenever the Pi is reboot, moonshine_moon.service launchs automatically.
   ```