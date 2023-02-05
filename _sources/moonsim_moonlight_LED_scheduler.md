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
(content:moonsim_moon)=
# <span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler

_<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_ is designed to be used in conjunction with _<span style="font-variant:small-caps;">MoonShine</span>_ to recreate moonlight cycle in the lab.

_<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_ runs the same set of calculations as _<span style="font-variant:small-caps;">MoonSim</span>: Lux calculator_ to predict moonlight illuminance. What's different is that the output table  `LED_schedule_moon.csv` contains lists of LED intensity values over time.


## Key features

- Recreate a realistic moonlight cycle in the lab
- Option to simulate the obstruction of moonlight by surrounding obstructions (e.g., mountain ranges)
- Option to simulate the dimming effects of moving cloud cover
- Option to change the LED color spectrum by controlling the intensity fraction of each RGBW channels. Can be useful in approximating the color shift in certain habitats (e.g., blue shiftiness of ocean at depth or the red shiftiness of sodium vapor street lamp).

- **IN PROGRESS**
