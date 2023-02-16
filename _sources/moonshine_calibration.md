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

## Moonlight re-creation
- To achieve realistic moonlight level illuminance, the LED arrays must be physically dimmed. We use neutral density (ND) filter on the lightbox to reduce the light intensity without modifying the color spectrum ({numref}`box`).

- The user must first decide whether to re-create unobstructed ground illumination (i.e., a simulation in which there is no additional dimming), or a lower intensity to resembles the attenuation level in the desired natural habitat.

- For the re-creation of full moon illuminance with no additional dimming, we recommend 0.4 lx as the standard calibration illuminance. Even the brightest full moon in the tropics does not exceed 0.4 lx. Therefore by calibrating the lightbox to 0.4 lx, we ensure that _<span style="font-variant:small-caps;">MoonShine</span>_ can re-create the entire range of moonlight illuminance.

## Create a calibration schedule
Use the provided `manual_scheduler.xlsx` (see {ref}`content:excel_scheduler`) to create a `LED_schedule_moon.csv` that turn on the LED at full intensity (with spectral control applied).
1. In `manual_scheduler.xlsx`, set theoretical_max to 0.4
2. Fill the entire column of "desired illuminance" with 0.4
3. Set the spectral control as desired (leave it as default for natural moonlight spectrum)
4. Make the schedule to lasts for 2 hours (or a period sufficient to perform the calibration period) and starts in the near future, at the time the calibration will be performed.
5. Follow the rest of the instructions in {ref}`content:excel_scheduler` to save the `LED_schedule_moon.csv`
6. This schedule file will instruct _<span style="font-variant:small-caps;">MoonShine</span>_ to generate full light intensity for the purpose of calibration.
### Which ND filter sheets?
To make an informed decision on what combination of ND filter sheets is need for the user's specific room and setup.

2. Set the lightbox at their permanent locations. Ideally each lightbox should be positioned on a shelf on both sides of the room, so that the light is directed to the ceiling and diffusely illuminate the entire room. The room should preferably have a white or light-shaded ceiling for optimal reflectance of the LED light into the room.
3. Using a radiometer, measure the illuminance at the position of the animal enclosure. Let us say that it measures 100 lx. 
    - To target a full moon illuminance (0.4 lx), based on the transmission of the ND filter:
    - Lee ND filter sheet lineup:
        - Lee 298 (ND 0.15, ½ Stop) = Transmission 69.3%
        - Lee 209 (ND 0.3, 1 Stop) = Transmission 51.2%
        - Lee 210 (ND 0.6, 2 Stop) = Transmission 23.5%
        - Lee 211 (ND 0.9, 3 Stop) = Transmission 13.7%
        - Lee 299 (ND 1.2, 4 Stop) = Transmission 6.6%
    - In theory, using two sheets of 4 Stop ND: 100 lx × 6.6% × 6.6% = 0.44 lx 
    - Use more ND sheets if further dimming is needed to re-create a lower illuminance.
    - The above calculation is only to get an idea of which ND filter to buy. Next we must calibrate _<span style="font-variant:small-caps;">MoonShine</span>_ by measuring the illuminance.

(content:lightbox:radiometer)=
###  Calibrating <span style="font-variant:small-caps;">MoonShine</span> with a radiometer
- Using the previously created calibration `LED_schedule_moon.csv`, launch _<span style="font-variant:small-caps;">MoonShine</span>_ (see {ref}`content:launch`).
- Next, the calibration method depends on whether a low light sensitive radiometer (able to accurately measure 0.01 lx) is available.
    - If available,
        1. layer filters on the lightbox until the illuminance (radiometer sensor placed on the ground of animal housing) reads the desire illuminance.
        2. If the measured illuminance is slightly higher than the target, and adding an additional filter dims it too much, we would simply change the **theoretical_max** value to the measured illuminance in _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight led scheduler_. Continuing the above example, the user would input 0.44 lx as the theoretical_max and use it as the calibration point.The _<span style="font-variant:small-caps;">MoonShine</span>_  system is now calibrated.
    - If only a non-low light sensitive radiometer is available:
        1. The user would instead measure the room illuminance with no filter applied. Then repeat the measurement but now with the radiometer pointing directly at the LED light at a close fixed distance.
        2. The ratio between the room illuminance and direct illuminance should remain relatively constant as more filters are applied.
        3. Hence, user can estimate how many layers of filter is required to reduce the illuminance to reach the target.

```{figure} /images/10days.png
:name: 10days

_<span style="font-variant:small-caps;">MoonShine</span>_ performance in re-creating moonlight illuminance level after calibration. MoonSim prediction (black line) and measeured re-created illuminance (red line). Both lines mostly overlaps. Test performed in a lab setting, running a simulated LED schedule for 9 nights around a full moon.
```
## Sunlight and twilight re-creation

- To achieve sunlight level illuminance, we do not need any dimming.
- The user must first decide what level of sunlight illuminance is required. Direct overhead sunlight can be over 100,000 lx. It is probably impractical and unnecessary to re-create such high levels of illuminance.
- We recommend the re-creation of sunlight at well over 200 lx, since 200 lx is approximately the illuminance when the sun is at the horizon. This means that if the light can not achieve 200 lx, _<span style="font-variant:small-caps;">MoonShine</span>_ is not even re-creating the full range of twilight illuminance.
- The LED strip can be adhered on the ceiling, with the LEDS pointing downward, to illuminate the room like a florescent light fixture, or it could be adhered directly above the animal enclosure to provide a much stronger light intensity. As a reference, illuminance measurement at 50cm from an LED strip is around 1000 lx. 

### Using more LED strips
- Two LED strips may not be enough in re-creating the desired illuminance, but more LED strips can be daisy chained together by:
    - Connect additional LED strips by following {numref}`schematic`
    - See {ref}`content:lightbox:lednumber3` for how to update the LEDs number in the software.