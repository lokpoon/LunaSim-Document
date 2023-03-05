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
# 7. <span style="font-variant:small-caps;">MoonShine</span>: Calibration

## Moonlight re-creation
- To achieve realistic moonlight level illuminance, the LED arrays must be physically dimmed. We use neutral density (ND) filter on the lightbox to reduce the light intensity without modifying the color spectrum ({numref}`box`).

- The user must first decide whether to re-create unobstructed ground illumination (i.e., a simulation in which there is no additional dimming), or to recreate light with a desired attenuation level so as to mimic the illumination levels of a natural habitat.

- For the re-creation of full moon illuminance with no additional dimming, we recommend 0.4 lx as the standard calibration illuminance. The brightest possible full moon does not exceed 0.4 lx. Therefore by calibrating the lightbox to 0.4 lx, we ensure that _<span style="font-variant:small-caps;">MoonShine</span>_ can re-create the entire range of moonlight illuminance.

(content:calibration_schedule)=
## Create a calibration schedule
Use the provided `manual_scheduler.xlsx` (see {ref}`content:excel_scheduler`) to create a `LED_schedule_moon.csv` that turns on the LEDs at full intensity (with spectral control applied).
1. In `manual_scheduler.xlsx`, set theoretical_max to 0.4
2. Fill the entire column of "desired illuminance" with 0.4
3. Set the spectral control as desired (leave it as default for natural moonlight spectrum)
4. Make the schedule to last for 2 hours (or a period sufficient to perform the calibration period) for a time period in the near future, at the time the calibration will be performed.
5. Follow the rest of the instructions in {ref}`content:excel_scheduler` to save the `LED_schedule_moon.csv`
6. This schedule file will instruct _<span style="font-variant:small-caps;">MoonShine</span>_ to generate full intensity light for the purpose of calibration.


### Which ND filter sheets?
To make an informed decision on what combination of ND filter sheets is needed for the user's specific room and setup, perform the following steps:

1. Position the lightboxes at their permanent locations. Ideally the lightboxes should be put on shelves at opposite sides of the room, so that the light is directed to the ceiling and diffusely illuminates the entire room. The room should preferably have a white or light-shaded ceiling so as to minimize the change in the light spectrum.
2. Using the previously created calibration `LED_schedule_moon.csv`, launch _<span style="font-variant:small-caps;">MoonShine</span>_ (see {ref}`content:launch`).
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
        1. Layer filters on the lightbox until the radiometer sensor placed on the ground of the animal housing reads a target illuminance between 0.4 lx to 0.5 lx.
        2. Record this illuminance measurement because this is the calibration point.
        3. Put in this calibration point as the theoretical_max value in _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight led scheduler_ when generating a `LED_schedule_moon.csv`. The _<span style="font-variant:small-caps;">MoonShine</span>_ system is now calibrated.
    - If only a non-low light sensitive radiometer is available:
        1. Instead measure the room illuminance with no filter applied. Then repeat the measurement but now with the radiometer pointing directly at the LED light at a close distance.
        2. The ratio between the room illuminance and direct illuminance should remain relatively constant as more filters are applied.
        3. In this manner estimate how many layers of filter are required to reduce the illuminance to reach the target.
        4. Then follow the above concepts described for calibrating the system with a low light sensitive radiometer.

```{figure} /images/10days.png
:name: 10days

<span style="font-variant:small-caps;">MoonShine</span>'s performance in re-creating moonlight illuminance level after calibration. MoonSim prediction = black line. Radiometer measurements of the re-created illuminance = red line. Note that the lines are very close. This test was performed in a lab setting, running a simulated LED schedule for 9 nights around a full moon.
```

```{note}
If the user intends to heavily modify the color spectrum of the LED arrays, for example to recreate a color-shifted habitat, radiometer measured illuminance (in lx) is not an appropriate unit. This is because photopic illuminance measurements assume a "natural light spectrum" (i.e. light similar to natural sunlight). In these cases the user should instead measure light level and calibrate <span style="font-variant:small-caps;">MoonShine</span> in spectral irradiance (unit photons OR Watts per m2 s nm) using a spectrometer.
```

(content:lightbox:sun_calibration)=
## Sunlight and twilight re-creation

- To achieve sunlight level illuminance, dimming of the LEDs is not required.
- The user must first decide what level of sunlight illuminance they required. Direct overhead sunlight can be over 100,000 lx. It is probably impractical and unnecessary to re-create such high levels of illuminance.
- Nonetheless, we recommend the re-creation of sunlight at well over 200 lx, since 200 lx is approximately the illuminance when the sun is at the horizon. This means that if the light can not achieve 200 lx, _<span style="font-variant:small-caps;">MoonShine</span>_ is not even re-creating the full range of twilight illuminance.
- The LED strip can be adhered to the ceiling, with the LEDs pointing downward, to illuminate the room like a florescent light fixture, or it could be adhered directly above the animal enclosure to provide a much stronger light intensity. As a reference, illuminance measurement at 50cm from a warm white 144-LED SK6812 LED strip is around 1000 lx. 
- Although it is nearly impossible to re-create full intensity sunlight using _<span style="font-variant:small-caps;">MoonShine</span>_ (i.e., the illuminance level would shortly plateau after sunrise), the sunlight LED array still need to be calibrated to ensure correct illuminance level before the plateau occurs (twilight and the short period after sunrise). To calibrate the sunlight LED array, follow these steps:
    1. Instruct the sunlight LED array to produce light at full intensity. See {ref}`calibration_schedule` to create a sunlight version of the calibration schedule (`LED_schedule_sun.csv`).
    2. Measure the illuminance on the level of the animal enclosure with a radiometer. This is the calibration point for the sunlight/twilight LED array.
    3. Use this calibration point as the theoretical_max value in _<span style="font-variant:small-caps;">MoonSim</span>: Sunlight/twilight LED scheduler_.

### Using more LED strips
- Two LED strips may not be enough to re-create the desired illuminance, but more LED strips can be daisy chained together, as follows:
    - Connect additional LED strips by following {numref}`schematic`
    - Add LED strips **in multiple of two**.
    - See {ref}`content:lightbox:lednumber3` for how to update the number of LEDs in the software.