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

# LS-lightbox: Launch procedure

In the previous software setup section, we have created a `lightbox_failsafe.service` that link to the `lightbox.py` located in *Desktop/control*. Instead of launching `lightbox.py` directly, we would launch the `lightbox_failsafe.service` so that the program will relaunch itself upon crashing.


## Requirements

Things to check before the launch:

### 1. Generate a working `LED_schedule.csv`

- On a computer, generate a `LED_schedule.csv` with the LunaSim scheduler, with your desired parameters. Move the `LED_schedule.csv` into your Pi's *Desktop/control*

- For the `lightbox.py` to run, the `LED_schedule.csv` must contain a row matching the time at launch. Meaning you cannot have a `LED_schedule.csv` where the first row is a time in the future. So, when creating the `LED_schedule.csv`, set the beginning date time ahead of when you will run the script.

- It also means that you should not delete entire rows with excel in the middle of the  `LED_schedule.csv`.

### 2. Check the location of files

- Within *Desktop/control*
  
  - `lightbox.py`
  
  - `LED_schedule.csv`

### 3. Make sure that the LED strips are not frozen

- The LED strip should never be frozen during operation. However, it may become unresponsive after the service file is stopped, or other accidents such as lose connection of the GPIO cable.

- We recommend resetting the LED strip before every launch, by unplugging both the power and the GPIO cable, and reconnecting them.

## To run `lightbox_failsafe.service`

In terminal,

1. Enable the service file:
   
   `sudo systemctl enable lightbox_failsafe.service`
   
      ```{note}
      The Raspberry Pi does not have sleeping or other enery saving mode, so no need to worry about these settings.
      ```

2. Check task running and the CPU usage:
   
   `htop`
   
   ```{note}
   Starting 8 sec before the start of every minutes, one of the CPU core will increase usage to 100%. lightbox_failsafe.service would be listed as the top task in the list. The LED will be be updated a the start of the minute, and CPU usage will return to normal.
   ```

3. A `LED_history.log` file will be created in *Desktop/control*. This logs allows the user to check what intensities the first 10 LEDs in the array have been instructed to output.

4. To stop the service file:
   
   `systemctl stop lightbox_failsafe.service`
   
   ```{note}
   The LED strip will maintain it's last instructed intensity. Unplug the power cord and GPIO connection to reset it.
   ```
   
   ```{note}
   Whenever the Pi is reboot, lightbox_failsafe.service launchs automatically.
   ```