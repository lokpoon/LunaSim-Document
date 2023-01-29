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

(content:lightbox:calibration)=
# LS-lightbox: Calibration

## Moonlight recreation
- To achieve moonlight level illuminance, the LED arrays must be physically dimmed. We use ND filter on the lightbox to reduce the light intensity without modifying the color spectrum.

- The user must first decide whether to recreate unobstructed ground illumination (i.e., a simulation in which there is no additional dimming), or a lower intensity to resembles the attenuation level in the desired natural habitat.

- To make an informed decision on what combination of ND filter sheets you would need for your specific room and setup, put the lightboxs at their permanent locations. Ideally on two top shelves on both sides of the room, so that light is directed to the ceiling and diffusely illuminate the entire room. Then measure the illuminance at the position of the animal enclosure. Let's say that it measures 100 lx. 
    - To target a full moon illuminance of 0.25 lx, based on the transmission of the ND filter:
    - Lee ND filter sheet lineup:
        - Lee 298 (ND 0.15, ½ Stop) = Transmission 69.3%
        - Lee 209 (ND 0.3, 1 Stop) = Transmission 51.2%
        - Lee 210 (ND 0.6, 2 Stop) = Transmission 23.5%
        - Lee 211 (ND 0.9, 3 Stop) = Transmission 13.7%
        - Lee 299 (ND 1.2, 4 Stop) = Transmission 6.6%
    - In theory, using two sheets of 4 Stop ND: 100 lx :x: 6.6% :x: 6.6% = 0.44 lx
    - Adding one sheet of ½ Stop ND: 0.44 lx :x: 69.3% = 0.30 lx
    - To further reduce 0.30 lx to 0.25, we could do it through LunaSim-Moonlight LED scheduler.
    - The above calculation is only to get an idea of which ND filter to buy. Next we must calibrate the lightbox by measuring the illuminance.
- The calibration method depends on whether a low light sensitive spectrometer or radiometer (able to measure 0.01 lx) is available.
    - If available, instruct the lightbox to generate a full moon illuminance, and layer filters on the lightbox until your room illuminance (radiometer sensor placed at your animal keeping area) reads the desire illuminance.
    - If only a non-low light sensitive radiometer is available:
        1. The user would instead measure the room illuminance with no filter applied. Then repeat the measurement but now with the radiometer pointing directly at the LED light at a close fixed distance.
        2. The ratio between the room illuminance and direct illuminance should remain relatively constant as more filters are applied.
        3. Hence, user can estimate how many layers of filter is required to reduce the illuminance to reach the target.

```{figure} /images/10days.png
:name: 10days

LS-lightbox performance in recreating moonlight illuminance level after calibration. LunaSim prediction (black line) and measeured recreated illuminance (red line). Both lines mostly overlaps. Test performed in a lab setting, running a simulated LED schedule for 9 nights around a full moon.
```
## Sunlight and twilight recreation

- To achieve sunlight level illuminance, we do not need any dimming.
- The user must first decide what sunlight illuminance is required. Direct overhead sunlight can be >100,000 lx, and is probably impractical and unnecessary to recreate such level of illuminance.
- You would probably want to recreate sunlight at least 200 lx though, because 200 lx is approximatly the illuminance when the sun is on the horizon. Meaning that if you can not recreate 200 lx, you are not even recreating the full range of twilight illuminance.
- The LED strip can be adhered on the ceiling to create illuminate the room like a normal light fixture, or fixed directly on your animal enclosure to provide a much stronger light intensity.

### Using more LED strips
- Two LED strips may not be enough in recreating the desired illuminance, but more LED strips can be daisy chained.
    - Connect additional LED strips according to {numref}`schematic`
    - On the software side, edit the `main.c` as described here in step 11 of {ref}`content:lightbox:lednumber`
    - And edit the `lightbox.py` as described here step 3 of {ref}`content:lightbox:lednumber2`
    - When generating the `LED_schedule.csv` from LunaSim LED schedulers, put in the correct number of LED strips. 