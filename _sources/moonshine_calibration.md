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
# <span style="font-variant:small-caps;">MoonShine</span>: Calibration

## Moonlight recreation
- To achieve moonlight level illuminance, the LED arrays must be physically dimmed. We use ND filter on the lightbox to reduce the light intensity without modifying the color spectrum ({numref}`box`).

- The user must first decide whether to recreate unobstructed ground illumination (i.e., a simulation in which there is no additional dimming), or a lower intensity to resembles the attenuation level in the desired natural habitat. Of course, the unobstructed ground illumination target varies according to the user's intended location and time as describe in {ref}`content:luxcalculator`


### Which ND filter sheets?
To make an informed decision on what combination of ND filter sheets is need for the user's specific room and setup.

1. In _<span style="font-variant:small-caps;">MoonSim</span>: Lux caculator_, simulate what is the brightest moonlight illuminance expected. Note down all of the eight LED values (the crude and fine values of the RGBW channels) at that moment.
2. Set the lightbox at their permanent locations. Ideally each lightbox on a shelf on both sides of the room, so that the light is directed to the ceiling and diffusely illuminate the entire room.
3. To instruct the LED strips to light up at the intensity during that brightest moment: Generate a `LED_schedule.csv` with a duration of one day. In Excel, replace the eight LED value columns in `LED_schedule.csv` with that set of brightest values.
4. Using a radiometer, measure the illuminance at the position of the animal enclosure. Let's say that it measures 100 lx. 
    - To target a full moon illuminance (e.g.,0.25 lx), based on the transmission of the ND filter:
    - Lee ND filter sheet lineup:
        - Lee 298 (ND 0.15, ½ Stop) = Transmission 69.3%
        - Lee 209 (ND 0.3, 1 Stop) = Transmission 51.2%
        - Lee 210 (ND 0.6, 2 Stop) = Transmission 23.5%
        - Lee 211 (ND 0.9, 3 Stop) = Transmission 13.7%
        - Lee 299 (ND 1.2, 4 Stop) = Transmission 6.6%
    - In theory, using two sheets of 4 Stop ND: 100 lx × 6.6% × 6.6% = 0.44 lx 
    - Adding one sheet of ½ Stop ND: 0.44 lx × 69.3% = 0.30 lx
    - Use ND sheets if further dimming is needed to recreate a lower illuminance.
    - The above calculation is only to get an idea of which ND filter to buy. Next we must calibrate _<span style="font-variant:small-caps;">MoonShine</span>_ by measuring the illuminance.

(content:lightbox:radiometer)=
###  Calibrating <span style="font-variant:small-caps;">MoonShine</span> with a radiometer
- The calibration method depends on whether a low light sensitive radiometer (able to accurately measure 0.01 lx) is available.
    - If available, instruct _<span style="font-variant:small-caps;">MoonShine</span>_ to generate a full moon illuminance, and layer filters on the lightbox until the illuminance (radiometer sensor placed on the ground of animal housing) reads the desire illuminance. If the measured illuminance is slightly higher than the target, and adding an additional filter dims it too much, we would fine tune the illuminance in _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight led scheduler_ by reducing the LED intensity. With this approach, we can slightly dim 0.3 lx to the 0.25 lx target (in the above example).
    - If only a non-low light sensitive radiometer is available:
        1. The user would instead measure the room illuminance with no filter applied. Then repeat the measurement but now with the radiometer pointing directly at the LED light at a close fixed distance.
        2. The ratio between the room illuminance and direct illuminance should remain relatively constant as more filters are applied.
        3. Hence, user can estimate how many layers of filter is required to reduce the illuminance to reach the target.

```{figure} /images/10days.png
:name: 10days

_<span style="font-variant:small-caps;">MoonShine</span>_ performance in recreating moonlight illuminance level after calibration. MoonSim prediction (black line) and measeured recreated illuminance (red line). Both lines mostly overlaps. Test performed in a lab setting, running a simulated LED schedule for 9 nights around a full moon.
```
## Sunlight and twilight recreation

- To achieve sunlight level illuminance, we do not need any dimming.
- The user must first decide what level of sunlight illuminance is required. Direct overhead sunlight can be over 100,000 lx. Therefore it is probably impractical and unnecessary to recreate such level of illuminance.
- We recommend the recreation of sunlight at >200 lx, since 200 lx is approximately the illuminance when the sun is at the horizon. This means that if the light can not achieve 200 lx, _<span style="font-variant:small-caps;">MoonShine</span>_ is not even recreating the full range of twilight illuminance.
- The LED strip can be adhered on the ceiling to illuminate the room like a florescent light fixture, or it could be adhered directly above the animal enclosure to provide a much stronger light intensity. As a reference, illuminance measurement at 50cm from an LED strip is around 1000 lx. 

### Using more LED strips
- Two LED strips may not be enough in recreating the desired illuminance, but more LED strips can be daisy chained together by:
    - Connect additional LED strips by following {numref}`schematic`
    - On the software side, edit the `main.c` as described here in step 11 of {ref}`content:lightbox:lednumber`
    - And edit the `lightbox.py` as described here step 3 of {ref}`content:lightbox:lednumber2`
    - When generating the `LED_schedule.csv` from _<span style="font-variant:small-caps;">MoonSim</span>_ LED schedulers, put in the correct number of LED strips. 