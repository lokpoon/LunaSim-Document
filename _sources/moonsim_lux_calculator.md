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
(content:luxcalculator)=
# <span style="font-variant:small-caps;">MoonSim</span>: Lux calculator

_<span style="font-variant:small-caps;">MoonSim</span>: Lux calculator_ predicts ground illuminance of moonlight in lux (lx). A basic prediction of twilight and sunlight illuminance is also included.

It is intended for use for ecological studies where biologists requires moonlight illuminance as a model predictor.

Download _<span style="font-variant:small-caps;">MoonSim</span>: Lux calculator_ here.

## Key features

- Accurate prediction of moonlight illuminance at any geographic location and over any time period.
- Basic prediction of twilight and sunlight illuminance as well.
- Generates .csv table of illuminance over time.
- Plot illuminance over time.

##  Packages required
- `library(suncalc)` Calculate astronomical variables given a time and location, including moon phase, moon altitude, sun altitude, the Moon and Earth distance
- `library(dplyr)` Data wrangling
- `library(rpmodel)` Calculates atmospheric pressure at given elevation
- `library(lubridate)` Makes datetime format easier to work with
- `library(REdaS)` Convert between degree angle and radian
- `library(npreg)` Fit smoothing spline
- `library(ggplot2)` Create plots
- `library(beepr)` Makes a notification sound

    ```{tip}
    This website [R Coder](https://r-coder.com/r-tutorials/r-basics/) is a good resource for learning basic R functions. Start here if you are completely new to R and need instructions on how to install packages.
    ```
##  Workflow
This is a basic run down of the _<span style="font-variant:small-caps;">MoonSim</span>: Lux calculator_ R code, highlighting the important steps. There the code itself is also commented.
1. Set the working directory. This is where the .csv and .png plot will save.

    ```
    setwd("/Users/lokpoon/Desktop")
    ```

2. Set the location.

    ```
    latitude <- -4.21528 # (!) Latitude in decimal degrees (e.g., -4.21528)
    longitude <- -69.94056 # (!) Longitude in decimal degrees (e.g. -69.94056)
    ```

3. Set the site elevation in m above mean sea level.

    ```
    site_elev <- 0 # (!) site elevation in meter (e.g., 0 = sea level)
    ```
    
4. Set the time zone.

    ```
    time_zone <- "EST"
    ```

5. Set the starting date, starting time, and simulation duration in days.

    ```
    date_start <- "2022-07-26" # (!) Starting date of the simulation (YYYY-MM-DD)
    time_start <- "18:00:00" # (!) Starting date of the simulation (hh:mm:ss)
    duration_day <- 29.5 # (!) Duration of simulation in days
    ```

6. Set the simulation time interval (i.e., the temporal resolution).

    ```
    time_interval_minutes <- 1 # (!) The temporal resolution of in minutes.
    ```

7. Decide whether to change the default darksky_value, a constant value that is added to moonlight illuminance for representing starlight and airglow.

    ```
    darksky_value <- 0.002 # (!) Range = 0.0007 to 0.003. Default = 0.002 lx
    ```

8. Specify the type of illumination to plot. i.e., One of the illuminance column name shown in step 10.
    ```
    illuminance_type_plot <- "moon_final_lux" # (!)
    ```
    
9. Run the computation section.
10. Save a lux_prediction.csv, containing the illuminance prediction over time.There are five columns of different illuminance:

    ```
    write.csv(moon_value_table,"lux_caculator_output.csv", row.names = TRUE)
    ```

    The lux_calculator_output.csv contains the following columns. We included the illuminance from the different combinations of moonlight, twilight, and sunlight, because each could be useful according to the user's application.

       ```
    datetime # The datetime in a standard format that R and lightbox.py can read
    phase_angle # the phase angle of the moon
    z_moon # zenith distance of the moon in degree angle
    distance # the moon and Earth distance in km
    sun_altitude # The altitude of the sun. Positive/negative value means the sun is above/below the horizon, respectively.
    moon_final_lux # illuminance of moonlight (plus the darksky_value)
    moon_final_lux_nighttime # illuminance of moonlight only at night (reports NA at daytime, when sun altitude > 0)
    twilight # illuminance of twilight (defined as the light when sun altitude < 0)
    sunlight # illuminance of sunlight (defined as the light when sun altitude > 0)
    total_illuminance_all # sum of moonlight, twilight, and sunlight
    sunlight_twilight # sum of sunlight and twilight
    moonlight_twilight_nighttime # illuminance of moonlight plus twilight only at night (reports NA at daytime, when sun altitude > 0)
       ```

10. Save a plot of the illuminance prediction over time.

    ```
    ggsave("plot_output.png", plot_output, width = 4488, height = 2000, units = "px", scale = 1, dpi = 450)
    ```
    
    
    
    
    ```{figure} /images/one_month.png
    :name: one_month

    Plot example of moonlight ground illuminance over a month in 2022 in Leticia, Colombia.
    ```