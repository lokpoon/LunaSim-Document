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
- Option to simulate light attenuation of cloud cover with the ability fine tune the cloud behavior.
- Option to adjust the LED light spectrum by controlling the relative intensity of each RGBW channels. Can be useful in approximating the color shift in certain habitats (e.g., blue shiftiness of ocean at depth or the red shiftiness of sodium vapor street lamp).

##  Workflow

1. Refer to {ref}`content:luxcalculator2` to repeat the process of packages loading and steps (1-7) to set the user definable settings (location, time period, etc.) The time_interval_minutes is fixed to 1 and should not be changed. The following instructions will cover the settings and function specific to _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_.

2. Set the calibration illuminance point. See {ref}`content:lightbox:calibration`.
   
   ```
   theoretical_max <- 0.4 # (!) Define a intensity upper limit (in lux)
   ```
   
3. Specify the number of LEDs per strip and the number of strips daisy-chained.

   ```
    diode_per_strip <- 144 # (!) Number of LEDs per strip
    strip_count <- 2 # (!) Number of daisy-chained LED strips
   ```


4. Determine the LED color spectrum by specifying the intensity output (0-1) of each RGBW channels. Leave this setting at the default value if the user wish to approximate natural moonlight spectrum. Note that these default values are intended for the warm white SK6812 LED strips made by BTF lightning. 

   ```
    white_fraction <- 1.0 # (!) White. Default = 1.0
    red_fraction <- 0.08 # (!) Red. Default = 0.08
    green_fraction <- 0.36 # (!) Green. Default = 0.36
    blue_fraction <- 0.19 # (!) Blue. Default = 0.19
   ```
    ```{figure} /images/moon_spectrum.jpg
    :name: moon_spectrum
    :width: 500px

    A comparison of the moonlight and LED lightbox spectral irradiance. RGBW intensity fraction set to the default values. R = 0.08, G = 0.36, B = 0.19, W = 1.0.
    ```
   Got to {ref}`content:rgbw` for details on how to adjust the RGBW intensity output for approximating the spectral-shift characteristics of certain habitats.
   
5. Specify whether to recreate the effect of surround tall objects blocking moonlight. We refer to this phenomenon as the **'horizon obstruction'**, for example when distant tree canopy or mountain range obscure a rising/setting moon near the horizon. Recreating this phenomenon might recreate a more realistic light scenario for the captive animal. See {ref}`content:horizon` for more details.
   
   ```
   horizon_option <- FALSE # (!) TRUE to enable
   ```
   
6. Specify whether to recreate the light attenuation by a changing cloud cover regime. See {ref}`content:cloud` for more details.

   ```
   cloud_option <- FALSE # (!) TRUE to enable cloud simulator
   ```

(content:rgbw)=
### RGBW spectral control

- _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_ does not recreate the rather insignificant spectral change according to the moon altitude. Meaning that moonlight is recreated with a consistent spectrum.
- Certain habitats are characterized by unique wavelength dependent attenuation, in which researchers might consider attempt  to recreate. _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_ gives users the option to adjust the relative intensity of the RGBW channels.
- Adjusting the RGBW spectrum require the user to have profound understandings of the spectral quality of their habitat target, and their studied animal's visual sensitivity. This is due to the limitations of the RGBW channels, which has very specific and limited peak and spectral range. And yet there are an endless range of light spectrum that occur in all kinds of habitat. Consequently, some habitat light spectrum approximations would be more realistic (e.g. when the spectral peak correspond to one of the RGBW peak), while other approximations would be unsatisfactory.
- Knowing the animal's spectral sensitivity can provide insights for assessing the validity of the recreated LED spectrum. For example mammals do not see UV light, so it is not a problem to use our UV deficient LED on them. However, many invertebrates and some vertebrates do see UV light and therefore must be consider.
- If user have a spectrometer, one would specify the RGBW intensity fraction in _<span style="font-variant:small-caps;">MoonSim</span>: Moonlight scheduler_ and measure the resulting overall LED spectral irradiance.
- If user do not have a spectrometer, one would use the provided excel spreadsheet `RGBW_LED_spectrum.xlsx` to predict the resulting overall LED spectral irradiance.
```{figure} /images/excel_predict.jpg
:name: excel_predict
:width: 500px

Using the provided excel spreadsheet RGBW_LED_spectrum.xlsx to visualize how the overall LED light spectrum will be based on the specified intensity fraction.
```
```{figure} /images/habitat.jpg
:name: habitat

The spectral irradiance of the RGBW channels at the same intensity level. Notice that at the same intensity level, the RGBW each produce a different absolute irradiance level (e.g. blue is the strongest at its peak wavelength). The dotted line indicates the spectral peaks of four distinctive habitats (clear ocean [Jerlov 1976], forest understory [Veilleus and Cummings 2012], relativly clear river, heavily tannined black/white water river [Costa et al. 2013]). The spectral peak of the clear ocean and blue channel are close, while the far red peak of the tannined river can neither be recreated by the red or white channels. This is a oversimplified representation of the habitats' spectrum, the user should always refer to the complete spectral irradiance plot. Ideally, researchers should make their own spectral irradiance measurment at their study site since even spectral property of the same type of habitats (e.g. "clear river") can vary greatly.
```

(content:horizon)=
### Horizon obstruction

```{attention}
Horizon obstruction automatically applies to all nights, since it is a topographical feature that is constantly present at the location.
```

- There are three settings that modify the behavior of horizon obstruction:

```{note}
(*) The angular altitude refers to the angle above the horizon, from 0 degrees at the horizon to 90 degrees at the zenith.)
```

```
horizon_transition_end <- 57 # (!) angular altitude* ABOVE which there is a zone of unobstructed illumination.
# We define this as Zone A.
```

```
horizon_elev <- 55 # (!) angular altitude* BELOW which there is maximum light attenuation (e.g. due to a mountain or tree line).
# We DEFINE THIS AS ZONE C.
```

```
horiz_transmission <- 0.15 # (!) the proportional transmission of light in Zone A relative to Zone C.
```

```{figure} /images/horizon.jpg
:name: horizon

An example of the horizon obstruction effect on illuminance, if horizon_option is enabled with the above three settings. Illuminance when the moon is below 55 degree (zone C) will be 15% of the light level above 57 degree (zone A), when the moon rise above the obstruction. In the transition zone B between 55 amd 57 degree, A linear transition of illuminance is applied. This makes light level transitions less abrupt when the simulated moon rises above simulated obstacles. MoonSim will read the LED_schedule_moon.csv and recreate the same illuminance behavior as visualized by the plot.
```

(content:cloud)=
### Cloud cover simulation
- There are six variables that need to be configured for cloud cover simulation. Cloud cover works by creating a random list of numbers (represent transmission) using a normal distribution, and fitting a spline function through them, creating a varying but smoothed modulation of the illuminance over time. The values of the six variables have some mutual effect on each other. The only way to assess the cloud cover effect is to visualize the spline function as a plot to get an idea of how will the simulated cloud modulate the existing moonlight.

#### Cloud period
- The first three defines the periods when cloud simulation is applied. Period outside of this period will not have cloud.
```
date_start_cloud <- "2022-07-26" # (!) starting date of cloud effect (YYYY-MM-DD)
time_start_cloud <- "18:00:00" # (!) starting time of cloud effect (hh:mm:ss)
duration_day_cloud <- 29.5 # (!) duration of the cloud effect
```
```{note}
If the user wants to apply cloud cover to the entire simulation period, simply uses the same values as the simulation inputted earlier for variables date_start,  time_start, and duration_day
```
```{note}
If the user wants to a more complicated cloud cover schedule that is not limited to a single period (e.g., only cloud in the second and eighth day of the simulation), generate multiple LED_schedule_moon.csv versions with the respective settings and merge them together in Excel. See {ref}`content:edit`
```

#### Cloud change frequency
- Specify the frequency of the change in cloud density.
```
cloud_change_freq <- 5 # (!) Sets how quickly the clouds are transitioning (in minutes). 
```
```{attention}
Setting cloud_change_freq smaller than 5 may crash R session.
```

**Example of cloud_change_freq = 5**
```{figure} /images/freq5smooth.jpg
:name: freq5smooth
:width: 500px
The smoothing spline with cloud_change_freq = 5
```
```{figure} /images/freq5output.jpg
:name: freq5output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. A value of 5 simulates rapid movement of clouds across the moon’s disk, due to high-speed winds at cloud altitude.
```

**Example of cloud_change_freq = 30**
```{figure} /images/freq30smooth.jpg
:name: freq30smooth
:width: 500px
The smoothing spline with cloud_change_freq = 30
```
```{figure} /images/freq30output.jpg
:name: freq30output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. A value of 60 represents very slow cloud movement.
```

#### Transmission mean
- Transmission here is defined as the fraction of light that passes through the cloud. Here specify the mean of transmission, with 1 being almost full transmission (little attenuation) and 0 being almost no transmission (near total attenuation). transmission_mean defines the mean of the normal distribution. A value of 1 means cloud simulator is using only the ‘left’ half of the normal distribution. This simulates an occasional cloud passing across the moon.
```
transmission_mean <- 1 # (!) Set the mean of the normal distribution.
```
```{important}
The user can set transmission_mean to exceed 1 or below 0. Setting it to exceed 1 "shifts" the normal distribution further to the "right", and will reduce the frequency and extremity of cloud cover (we recommend not exceeding 2). Zero or a negative value will use the right side of the normal distribution – simulating denser cloud cover with occasional periods of no cloud cover (we recommend values no lower than -1). Avoid using a value between 0 and 1.
```
**Example of transmission_mean = 1.2**
```{figure} /images/mean12smooth.jpg
:name: mean12smooth
:width: 500px
The smoothing spline with transmission_mean = 1.2
```
```{figure} /images/mean12output.jpg
:name: mean12output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. By increasing the transmission_mean slightly above 1, it decreases the overall "thickness" of the cloud. It simulate the occational passing of a thin cloud.
```

**Example of transmission_mean = -0.2**

```{figure} /images/mean02smooth.jpg
:name: mean02smooth
:width: 500px
The smoothing spline with transmission_mean = -0.2
```
```{figure} /images/mean02output.jpg
:name: mean02output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. By reducing the transmission_mean slightly below 0, it increases the overall "thickness" of the cloud. The behaviour of transmission_mean at around 0 is the complete opposite of 1. Instead of using the "left" side of the normal distribution, it uses the "right" side. Meaning that instead of the occational passing of cloud, it simulate the occational windows of clear sky in a cloudy scenerio. 
```

#### Transmission standard deviation (SD)
- Specify the SD of transmission, with 0.5 being a good value to start with. All the above plots have transmission_sd = 0.5. Increasing the transmission_sd increases the range of transmission variation, making the cloud effect more unpredictable (i.e., patchy clouds. Reducing the transmission_sd limits the range of transmission variation, which suits for simulating a evenly overcast sky.

**transmission_sd = 1**

```{figure} /images/sd1smooth.jpg
:name: sd1smooth
:width: 500px
The smoothing spline with transmission_sd = 1
```

```{figure} /images/sd1output.jpg
:name: sd1output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. The illuminance switches drastically from one moment to the next with a higher transmission_sd = 1. This resembles thick but patchy clouds with many windows of opening.
```

**transmission_sd = 0.1**

```{figure} /images/sd01smooth.jpg
:name: sd01smooth
:width: 500px
The smoothing spline with transmission_sd = 1 (and lower transmission_mean = 0.5 )
```

```{figure} /images/sd01output.jpg
:name: sd01output
:width: 500px
The final moonlight illuminance with the same smoothing spline of the previous plot applied. This simulate a thin overcast sky with a overall reduction but small variation in illuminace.
```
```{tip}
Selecting the best suited cloud settings should be based on the smoothing spline preview.  Users are encourage to try out different combinations of cloud settings. The user will see a preview of the smoothing spline by "END OF PARAMETER SETTINGS" line. If the paticular smoothing spline looks undesirable, runing the section of code again will generate another smoothing spline that looks different because it is a random number generator.
```

```{attention}
Beware that the cloud effect is generated randomly every time the script is run. The user can save the specific cloud_table with a line of code just before "END OF PARAMETER SETTINGS"
```