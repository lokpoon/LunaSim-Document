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

(content:codes)=
# Code

- The code provided below is available on GitHub at: [https://github.com/Crampton-Lab/MoonShine](https://github.com/Crampton-Lab/MoonShine)

### <span style="font-variant:small-caps;">MoonShineR</span>: Lux calculator

```r
# MoonShineR - Lux calculator
# An R program by C. Lok Poon, Crampton Electric Fish Lab, University of Central Florida, Copyright 2023
# A detailed guide about this program: https://lokpoon.github.io/moonshine_manual/lux_calculator.html

# Description:
# This script predicts accurate moonlight illuminance at a given geographical location and time period. It generate a lux_calculator_output.csv and .png plot.

# Load libraries ---------------------------

library(suncalc)
library(rpmodel)
library(dplyr)
library(lubridate)
library(REdaS)
library(npreg)
library(ggplot2)
library(beepr)
library(progress)

#---------------------------START OF PARAMETER SETTINGS---------------------------

# (!) indicates a user specified setting

# Set working directory:
setwd("/Users/lokpoon/Desktop") # (!) .csv and .png files will be saved to this directory

# Set the location and time ---------------------------
latitude <- -4.21528 # (!) Latitude in decimal degrees (e.g., -4.21528)
longitude <- -69.94056 # (!) Longitude in decimal degrees (e.g., -69.94056)
site_elev <- 0 # (!) Site elevation in meters (e.g., 0 = sea level). Elevation correction only applies to moonlight but not sunlight and twilight.
# The user can determine the site elevation of a coordinate location using https://www.dcode.fr/earth-elevation

time_zone <- "EST" # (!) Set the time zone for the location set (e.g., “EST”). REMEMBER TO CHANGE THE TIME ZONE WHEN THE LOCATION IS CHANGED.
# For a list of time zone names, enter OlsonNames(tzdir = NULL) in R console
# Use a time zone without DST. E.g., use "EST" instead of "America/New_York"
date_start <- "2023-03-01" # (!) Starting date of the simulation (YYYY-MM-DD)
time_start <- "18:00:00" # (!) Starting time of the simulation (hh:mm:ss)
duration_day <- 1 # (!) Duration of simulation in days
time_interval_minutes <- 1 # (!) The temporal resolution of the simulation in minutes. E.g., 5 = calculates the illuminance every 5 minutes.
# User may increase time_interval_minutes for a shorter run time when simulating over many days.

# Set nominal dark sky value ---------------------------
# Adding a baseline illumination to the model to represent other nocturnal light sources (e.g., starlight and airglow) (Hänel et al. 2017) 
darksky_value <- 0.0008 # (!) Default = 0.0008
# change it to zero if a completely dark sky is preferred.

# Set what type of illuminance to plot ---------------------------
illuminance_type_plot <- "moon_final_lux_nighttime" # (!) Enter one of the below illuminance column names.
# This only affect the plot, the .csv output will include all of the various illuminance columns.

# Illuminance columns name:
# moon_final_lux = illuminance of moonlight (plus the darksky_value)
# moon_final_lux_nighttime = illuminance of moonlight only at night (reports NA at daytime, when sun altitude > 0 degrees)
# twilight = illuminance of twilight (defined as the light when sun altitude < 0 degrees)
# sunlight = illuminance of sunlight (defined as the light when sun altitude > 0 degrees)
# total_illuminance_all = sum of moonlight, twilight, and sunlight
# sunlight_twilight = sum of sunlight and twilight
# moonlight_twilight_nighttime = illuminance of moonlight plus twilight only at night (reports NA at daytime, when sun altitude > 0 degrees)

# To generate a good-looking plot, the user will typically need to modify the y-axis range. See the plotting section near the end.
  
#---------------------------END OF PARAMETER SETTINGS---------------------------

#---------------------------START OF ILLUMINATION COMPUTATION-------------------

# Start time formatting
date_time_start <- as_datetime(paste(date_start, time_start, sep = " ", collapse = NULL), tz = time_zone)
number_of_interval <- as.numeric(ddays(duration_day)) / as.numeric(dminutes(time_interval_minutes))

# Create an empty dataframe, to be filled during for loop
moon_value_table <- data.frame(matrix(ncol = 1, nrow = number_of_interval))
x <- c("x")
colnames(moon_value_table) <- x

# Create for loop [i] time interval list
time_interval_list <- seq(1, number_of_interval, by = 1) 

# Create a progress bar object
pb <- progress_bar$new(total = length(time_interval_list))

# Fill in empty data frame with suncalc data
for (i in time_interval_list) {
  moon_value_table[i, "datetime"] <- getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes * 60)[1, "date"]
  moon_value_table[i, "phase_angle"] <- (getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes * 60)[1, "phase"]) * (-360) + 180 # phase_angle = angular separation of the sun and Earth, as seen on the moon
  moon_value_table[i, "fraction"] <- (getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes*60)[1, "fraction"]) # Moon illuminated fraction, not used in calculation. This is calculated only for user to learn about the moon phase.
  moon_value_table[i, "Z_moon"] <- 90 - (rad2deg(getMoonPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude)[1, "altitude"])) # Z_moon = Zenith distance in degree of the moon = 90 - moon altitude
  moon_value_table[i, "distance"] <- getMoonPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude)[1, "distance"] # distance = moon/Earth distance in km
  moon_value_table[i, "sun_altitude"] <- rad2deg(getSunlightPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude, keep = c("altitude"))[1, "altitude"]) # sun_altitude = altitude of the sun in degree
  pb$tick() # Update the progress bar
}
moon_value_table <- subset(moon_value_table, select = -c(x))

# Replace moon altitude that are lower than horizon_elev with NA (moon below horizon)
moon_value_table <- transform(moon_value_table, Z_moon = ifelse(Z_moon > 90, NA, Z_moon)) 

# Calculate atmospheric extinction
moon_value_table$atm_ext <- (-0.140194 * moon_value_table$Z_moon) / (-91.674385 + moon_value_table$Z_moon) - 0.03 # A Michaelis-Menten that fits Table 2 in Austin et al. (1976)
moon_value_table$atm_ext <- ifelse(moon_value_table$atm_ext < 0, 0, moon_value_table$atm_ext)

# Moon magnitude calculated from phase angle (unit in relative magnitude) (see Allen 1976, p. 144)
moon_value_table$m <- (-12.73) + 0.026 * abs(moon_value_table$phase_angle) + 4 * (10 ^ -9) * (abs(moon_value_table$phase_angle) ^ 4)

# Initial illuminance of moonlight (see eq. (16) of Schaefer 1990a)
illuminance_temp <- 10 ^ ((-0.4) * (moon_value_table$m + moon_value_table$atm_ext + 16.57)) # In unit foot candle
moon_value_table$illuminance_temp_lux <- illuminance_temp * 10.7639 # Convert to lux

# Correct for the effect of site elevation
atm_pressure_relative_to_sea <- patm(site_elev, patm0 = 101325) / 101325 # The atmospheric pressure at the site elevation relative to sea level
sea_555nm <- 18.964 * exp(-0.229 * 1) # Sea level irradiance at 555nm. Function extracted from figure 1 of Laue (1970)
elevated_555nm <- 18.964 * exp(-0.229 * atm_pressure_relative_to_sea) # Sea level irradiance at 555nm. Function extracted from figure 1 of Laue (1970)
increase_factor_elev <- elevated_555nm / sea_555nm # relative increase in illuminance due to elevation
moon_value_table$illuminance_temp_lux <- moon_value_table$illuminance_temp_lux * increase_factor_elev

# Apply lunar opposition surge when p < 6 (Buratti et al. 1996, figure 5)
moon_value_table <- transform(moon_value_table, illuminance_temp_lux = ifelse(abs(phase_angle) < 6, illuminance_temp_lux + ((0.4 * (6 - abs(phase_angle)) / 6) * illuminance_temp_lux), illuminance_temp_lux))
## A linear increase in moon brightness as phase angle decreases below 6

# Apply spreading out effect (angle of incidence) of light when illuminating at an angle (Austin et al. 1976)
moon_value_table$moon_final_lux <- moon_value_table$illuminance_temp_lux * sin(deg2rad(90 - moon_value_table$Z_moon))

# The moon/Earth distance effect (inverse square law) (Austin et al. 1976)
moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux * (1 / ((moon_value_table$distance / 384400) ^ 2))

# Waxing Waning asymmetric effect (simplified function derived from Austin et al. 1976 Table 1)
moon_value_table$moon_final_lux <- ifelse(moon_value_table$phase_angle < 0,
                                          moon_value_table$moon_final_lux * (-0.00026 * moon_value_table$phase_angle + 1),
                                          moon_value_table$moon_final_lux)

# Final moonlight illuminance (with a slight adjustment factor, calibrated from Leticia, Colombia, Aug 11, 2022 field full moon measurement)
moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux * 0.863 + darksky_value
moon_value_table$moon_final_lux <- replace(moon_value_table$moon_final_lux, is.na(moon_value_table$moon_final_lux), darksky_value) # Replace NA with darksky_value

moon_value_table <- transform(moon_value_table, moon_final_lux_nighttime = ifelse(sun_altitude > 0, NA, moon_final_lux)) # Create moon_final_lux_nighttime column

#---------------------------TWILIGHT CALCULATION---------------------------

# Calculation of sunlight and twilight follows Seidelmann (1992)
moon_value_table$twilight <- 0
moon_value_table$twilight <- ifelse(moon_value_table$sun_altitude < 0 & moon_value_table$sun_altitude > -0.8,
                                    10 ^ (2.88 + (22.26 * (moon_value_table$sun_altitude / 90)) - 207.64 * ((moon_value_table$sun_altitude / 90) ^ 2) + 1034.3 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$twilight)
moon_value_table$twilight <- ifelse(moon_value_table$sun_altitude < -0.8 & moon_value_table$sun_altitude > -5,
                                    10 ^ (2.88 + (21.81 * (moon_value_table$sun_altitude / 90)) - 258.11 * ((moon_value_table$sun_altitude / 90) ^ 2) - 858.36 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$twilight)
moon_value_table$twilight <- ifelse(moon_value_table$sun_altitude < -5 & moon_value_table$sun_altitude > -12,
                                    10 ^ (2.7 + (12.17 * (moon_value_table$sun_altitude / 90)) - 431.69 * ((moon_value_table$sun_altitude / 90) ^ 2) - 1899.83 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$twilight)
moon_value_table$twilight <- ifelse(moon_value_table$sun_altitude < -12 & moon_value_table$sun_altitude > -18,
                                    10 ^ (13.84 + (262.72 * (moon_value_table$sun_altitude / 90)) + 1447.42 * ((moon_value_table$sun_altitude / 90) ^ 2) + 2797.93 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$twilight)

#---------------------------SUNLIGHT (SUN > 0 DEGREE) CALCULATION---------------------------

moon_value_table$sunlight <- 0
moon_value_table$sunlight <- ifelse(moon_value_table$sun_altitude > 20,
                                    10 ^ (3.74 + (3.97 * (moon_value_table$sun_altitude / 90)) - 4.07 * ((moon_value_table$sun_altitude / 90) ^ 2) + 1.47 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$sunlight)
moon_value_table$sunlight <- ifelse(moon_value_table$sun_altitude < 20 & moon_value_table$sun_altitude > 5,
                                    10 ^ (3.05 + (13.28 * (moon_value_table$sun_altitude / 90)) - 45.98 * ((moon_value_table$sun_altitude / 90) ^ 2) + 64.33 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$sunlight)
moon_value_table$sunlight <- ifelse(moon_value_table$sun_altitude < 5 & moon_value_table$sun_altitude > 0,
                                    10 ^ (2.88 + (22.26 * (moon_value_table$sun_altitude / 90)) - 207.64 * ((moon_value_table$sun_altitude / 90) ^ 2) + 1034.3 * ((moon_value_table$sun_altitude / 90) ^ 3)), moon_value_table$sunlight)

#---------------------------ADD MOON, SUNLIGHT AND TWILIGHT TOGETHER---------------------------

moon_value_table$total_illuminance_all <- moon_value_table$moon_final_lux + moon_value_table$twilight + moon_value_table$sunlight
moon_value_table$sunlight_twilight <- moon_value_table$twilight + moon_value_table$sunlight
moon_value_table$moonlight_twilight_nighttime <- moon_value_table$twilight + moon_value_table$moon_final_lux_nighttime

#---------------------------REMOVE UNNECESSARY COLUMNS---------------------------

moon_value_table <- subset(moon_value_table, select = -c(atm_ext, m, illuminance_temp_lux))

#---------------------------END OF ILLUMINATION COMPUTATION--------------------

#---------------------------GENERATE lux_calculator_output.csv---------------------------

# Save moon table csv file
write.csv(moon_value_table,"lux_calculator_output.csv", row.names = TRUE)

# Explanation for the columns found in lux_calculator_output.csv:
# Use whichever illuminance prediction is appropriate for desired use. 

## datetime = The datetime in a standard format that R and moonshine_moon.py can read
## phase_angle = the phase angle of the moon
## fraction = the illuminated fraction of the moon
## Z_moon = zenith distance of the moon in degree angle
## distance = the moon and Earth distance in km
## sun_altitude = The altitude of the sun. Positive/negative value means the sun is above/below the horizon, respectively.
## moon_final_lux = illuminance of moonlight (plus the darksky_value)
## moon_final_lux_nighttime = illuminance of moonlight only at night (reports NA at daytime, when sun altitude > 0 degree)
## twilight = illuminance of twilight (defined as the light when sun altitude < 0 degree
## sunlight = illuminance of sunlight (defined as the light when sun altitude > 0 degree)
## total_illuminance_all = sum of moonlight, twilight, and sunlight
## sunlight_twilight = sum of sunlight and twilight
## moonlight_twilight_nighttime = illuminance of moonlight plus twilight only at night (reports NA at daytime, when sun altitude > 0 degree)

#---------------------------Plotting Section---------------------------

# Dark gray area depicts dark periods (true night after astronomical twilight ended).
# Light gray area indicate the periods of astronomical twilight.

# Create a clean ggplot theme
theme_rectangular_clean <-
  theme(axis.line = element_line(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank()) +
  theme(axis.text = element_text(size = 12, colour = 'black'),
        axis.title = element_text(size = 12, colour = 'black')) +
  theme(plot.title = element_text(size = 12)) +
  theme(plot.margin = unit(c(0.25,0.25,0.25,0.25),"cm"))

# Specify the time of night period and twilight period for shading
night_time <- filter(moon_value_table, sun_altitude < 0) %>% dplyr::select(datetime)
night_time <- as_datetime(night_time$datetime, tz = time_zone)

after_twilight_time <- filter(moon_value_table, sun_altitude < (-18)) %>% dplyr::select(datetime)
after_twilight_time <- as_datetime(after_twilight_time$datetime, tz =  time_zone)

day_time <- filter(moon_value_table, sun_altitude > 0) %>% dplyr::select(datetime)
day_time <- as_datetime(day_time$datetime, tz = time_zone)

# Plotting:
plot_output <- ggplot() + theme_rectangular_clean +
  geom_rect(aes(xmin = night_time, # night period
                xmax = night_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey88", alpha = 1, na.rm = TRUE) +
  geom_rect(aes(xmin = after_twilight_time, # after twilight
                xmax = after_twilight_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey80", alpha = 1, na.rm = TRUE) +
  geom_line(data = moon_value_table, aes(x = datetime, y = eval(as.symbol(illuminance_type_plot))), colour = 'black', linewidth = 0.75) +
  geom_rect(aes(xmin = day_time, # day time mask moonlight regression to gray color
                xmax = day_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "white", alpha = 0.85, na.rm = TRUE) +
  scale_y_continuous(limits = c(0, 0.3), # change the y-axis range here
                     breaks = c(seq(from = 0, to = 0.3, by = 0.1))) + # change the y-axis breaks here
  scale_x_datetime(date_breaks = "1 day") + # change the date break here for different x-axis label. A more specific format can be specified.
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) + # rotate date label 90 degree.
  labs(x = "", y = "predicted ground illuminance (lx)") 

plot_output

beep()

# Save plot:
ggsave("plot_output.png", plot_output, width = 4488, height = 2000, units = "px", scale = 1, dpi = 450)

## .png can be changed to .pdf to save as a vector file.
## However when exporting as .pdf, the shading transparency (alpha setting) might not look right. This is a limitation of R.

#---------------------------Lunar eclipse warning---------------------------

# MoonShineR warns the user if an eclipse occurs during a simulation, and it reports the start and end time of the simulation.
# However, MoonShineR does not simulate the reduction in moon ground illuminance associated with the eclipse.

if (any(abs(moon_value_table$phase_angle) < 1.5 & moon_value_table$sun_altitude < 0)) { # eclipse defined as a moon with phase angle < 1.5 during nighttime
  print("ECLIPSE IN SIMULATION!!!")
  eclipse_list <- (abs(moon_value_table$phase_angle) < 1.5 & moon_value_table$sun_altitude < 0)
  moon_value_table[which(eclipse_list == TRUE),]
} else {
  print("no eclipse in simulation")
}

#---------------------------END OF SCRIPT---------------------------

# References ---------------------------  

# Allen, C. W. (1976). Astrophysical quantities (3rd ed. 1973, Repr. with corrections 1976). Athelone Press.; [Distributor for] U.S.A. and Canada, Humanities Press.
# Austin, R. H., Phillips, B. F., & Webb, D. J. (1976). A method for calculating moonlight illuminance at the earth’s surface. The Journal of Applied Ecology, 13(3), 741. https://doi.org/10.2307/2402251
# Buratti, B. J., Hillier, J. K., & Wang, M. (1996). The lunar opposition surge: Observations by clementine. Icarus, 124(2), 490–499. https://doi.org/10.1006/icar.1996.0225
# Hänel, A., Posch, T., Ribas, S. J., Aubé, M., Duriscoe, D., Jechow, A., Kollath, Z., Lolkema, D. E., Moore, C., Schmidt, N., Spoelstra, H., Wuchterl, G., & Kyba, C. C. M. (2018). Measuring night sky brightness: Methods and challenges. Journal of Quantitative Spectroscopy and Radiative Transfer, 205, 278–290. https://doi.org/10.1016/j.jqsrt.2017.09.008
# Krisciunas, K., & Schaefer, B. E. (1991). A model of the brightness of moonlight. Publications of the Astronomical Society of the Pacific, 103, 1033. https://doi.org/10.1086/132921
# Laue, E. G. (1970). The measurement of solar spectral irradiance at different terrestrial elevations. Solar Energy, 13(1), 43–57. https://doi.org/10.1016/0038-092X(70)90006-X
# Schaefer, B. E. (1990). Telescopic limiting magnitudes. Publications of the Astronomical Society of the Pacific, 102, 212. https://doi.org/10.1086/132629
# Seidelmann, P. K., United States Naval Observatory, & Great Britain (Eds.). (1992). Explanatory supplement to the Astronomical almanac (Rev. ed.). University Science Books.

# Notes ---------------------------  

## Be careful with radian and degree angle
### Calculations in Krisciunas & Scaefer 1991 model uses degree angle
### suncalc functions gives radian. R trigonometry function takes radian.

## Zenith distance of the moon = 90 degree angle - moon altitude

## Phase output from suncalc::getMoonIllumination:
### 0 = new moon
### 0.25 = first quarter (waxing)
### 0.5 = full
### 0.75 = third/last quarter (waning)

## To convert phase to phase angle (following the sign convention of Krisciunas & Schaefer 1991):
### phase_angle <- phase*(-360)+180
#### positive = waxing 
#### negative = waning 
#### 180 = new moon
#### 90 = 1st quarter (waxing)
#### 0 = full
#### -90 = 2nd quarter (waning)
```
### <span style="font-variant:small-caps;">MoonShineR</span>: Moonlight scheduler

```r
# MoonShineR - Moonlight scheduler
# An R program by C. Lok Poon, Crampton Electric Fish Lab, University of Central Florida, Copyright 2023
# A detailed guide about this program: https://lokpoon.github.io/moonshine_manual/moonlight_LED_scheduler.html

# Description:
# This script generates an LED_schedule_moon.csv schedule file for MoonShineP to re-create a moonlight regime.

# Load libraries ---------------------------

library(suncalc)
library(rpmodel)
library(dplyr)
library(lubridate)
library(REdaS)
library(npreg)
library(ggplot2)
library(beepr)
library(progress)

#---------------------------START OF PARAMETER SETTINGS---------------------------

# (!) indicates a user specified setting

# Set working directory:
setwd("/Users/lokpoon/Desktop") # (!) .csv and .png files will be saved to this directory

# Set the location and time ---------------------------
latitude <- -4.21528 # (!) Latitude in decimal degrees (e.g., -4.21528)
longitude <- -69.94056 # (!) Longitude in decimal degrees (e.g., -69.94056)
site_elev <- 0 # (!) Site elevation in meters (e.g., 0 = sea level).
# Elevation correction applies to moonlight but not sunlight and twilight.
# The user can determine the site elevation of a coordinate location using https://www.dcode.fr/earth-elevation

time_zone <- "EST" # (!) Set the time zone for the location set (e.g., “EST”). REMEMBER TO CHANGE THE TIME ZONE WHEN THE LOCATION IS CHANGED.
# For a list of time zone names, enter OlsonNames(tzdir = NULL) in R console
# Use a time zone without DST. E.g., use "EST" instead of "America/New_York"
date_start <- "2023-03-01" # (!) Starting date of the simulation (YYYY-MM-DD)
time_start <- "18:00:00" # (!) Starting time of the simulation (hh:mm:ss)
duration_day <- 1 # (!) Duration of simulation in days

# Set nominal dark sky value ---------------------------
# Adding a baseline illumination to the model to represent other nocturnal light sources (e.g., starlight and airglow) (Hänel et al. 2017) 
darksky_value <- 0.0008 # (!) Default = 0.0008
# change it to zero if a complete darkness (during moonless night) is preferred (i.e., no starlight or skyglow)

# LED strip configuration---------------------------

theoretical_max <- 0.4 # (!) Define an intensity upper limit (in lx) so that the LED system is not instructed to exceed 100% output intensity.
## Refer to online MoonShine Manual part 7.
## Increasing theoretical_max will reduce the illuminance to the LED.

diode_per_strip <- 144 # (!) Number of LEDs per strip
strip_count <- 2 # (!) Number of daisy-chained LED strips

# LED spectral control---------------------------
# Input the intensity fraction (0-1) each LED color is outputting. Each is independent. 
white_fraction <- 1.0 # (!) White. Default = 1.0
red_fraction <- 0.08 # (!) Red. Default = 0.08
green_fraction <- 0.36 # (!) Green. Default = 0.36
blue_fraction <- 0.19 # (!) Blue. Default = 0.19
# These default RGBW fractions approximate the spectrum of moonlight when used with the intended SK6812 RGBW LED strip, with 'warm white' specification.
# To change color balance from white to, for example, a red-shifted light, the user can increase the red_fraction, incrementally, until the color generated by lightbox reaches the desired parameters on a spectrometer.
# See manual for citations of papers that describe the color properties of different natural habitats. 

# Horizon obstruction---------------------------
# Recreate potential obstructions of moonlight from the horizon (anywhere except sea level). E.g., tall mountain range or trees around a forest gap.
horizon_option <- FALSE # (!) TRUE to enable
horizon_transition_end <- 57 # (!) angular altitude* ABOVE which there is a zone of unobstructed illumination. We define this as Zone A.
horizon_elev <- 55 # (!) angular altitude* BELOW which there is maximum light attenuation (e.g., due to a mountain or tree line). We DEFINE THIS AS ZONE C.
# * The angular altitude refers to the angle above the horizon, from 0 degrees at the horizon to 90 degrees at the zenith.
horiz_transmission <- 0.15 # (!) the proportional transmission of light in Zone A relative to Zone C. For example, if a value of 0.15 is chosen, and horizon_elev is set to 55, light level in the zone below 55 degrees will be 15% of the light level above the angle of “horizon_transition_end”.
# Zones A and C delimit a third, intervening zone B (e.g., between 55 and 60 degrees above the horizon). A linear transition of light level is applied between horizon_elev and horizon_transition_end. This makes light level transitions less abrupt when the simulated moon rises above simulated obstacles. 

# Cloud cover settings ---------------------------
cloud_option <- FALSE # (!) TRUE to enable cloud simulator
# User should review graphical output of simulation in the next section, and adjust parameters accordingly, before deployment of the simulation with MoonShineP.
date_start_cloud <- date_start # (!) starting date of cloud effect (YYYY-MM-DD)
time_start_cloud <- time_start # (!) starting time of cloud effect (hh:mm:ss)
duration_day_cloud <- duration_day # (!) duration of the cloud effect
cloud_change_freq <- 30 # (!) Sets how quickly the clouds are transitioning (in minutes). Set this value to > or = 5. A value of <5 may crash R session.
# A value of 5 simulates rapid movement of clouds across the moon’s disk due to high-speed winds at cloud altitude. A value of 30 represents very slow cloud movement.
transmission_mean <- 1 # (!) Set the mean of the normal distribution. A value of 1 means cloud simulator is using only the ‘left’ half of the normal distribution. This simulates an occasional cloud passing across the moon.
# A value over 1 will reduce the frequency and extremity of cloud cover (we recommend values not exceeding 2).
# Zero or a negative value will use the right side of the normal distribution – simulating denser cloud cover with occasional periods of no cloud cover (we recommend values no lower than -1). Avoid using a value between 0 and 1.

transmission_sd <- 0.5 # (!) Set the SD of the of the normal distribution. We recommend starting at 0.5, and increasing or decreasing this value slightly (e.g. change to 1.5) to thicken or thin the simulated passing clouds.
# The user can create ‘tailored’ weather changes by running MoonShineR moonlight scheduler for a defined start and end period, using one set of cloud simulator parameters, and then running the entire simulation for a subsequent period of time, this time using a new set of cloud simulator parameters. The user can then manually concatenate the data in the .csv files.
# This procedure can be repeated for as many major transitions in weather are required during a simulation. 

# The cloud simulator works by applying a cloud_table dataframe that contains the proportional moonlight transmission value for each minute (recalling that lightbox operations are constrained to changes in light every minute as defined by time_interval_minutes).
# The cloud_table dataframe is generated in two stages. First, it create a set of random data points (each representing simulated light transmission values for a given time), with the value of these data points constrained within a normal distribution.
# The user is able to control the following parameters of this normal distribution: 1) the mean; 2) the standard deviation; 3) the number of values per unit time, with 1 value per minute being the minimum. The cloud simulator then applies a smoothing spline to this distribution to create a smooth transition in light transmission.
# Finally values from this spline are interpolated at one minute intervals to provide the required values for light generation by the LED array.

#--------------------------- START OF CLOUD EFFECT GENERATOR ---------------------------

time_interval_minutes <- 1 # The temporal resolution of the simulation in minutes. Locked at 1 for MoonShineP to operate correctly.
bit8 <- 255 # Controllable light intensity level of the LEDs is 255 (8 bit).

# Prepare a table for cloud stochastic values and plot
# Beware that the cloud effect is generated randomly, within the desired parameters, every time if “set.seed(1)” is commented out. 
#enabling “set.seed(1)” by uncommenting this line  will replicate the exact same cloud settings #every time the script is run (assuming all settings remain identical)

if (cloud_option == TRUE) {
  date_time_start_cloud <- as_datetime(paste(date_start_cloud, time_start_cloud, sep = " ", collapse = NULL), tz = time_zone)
  number_of_interval_cloud <- as.numeric(days(duration_day_cloud)) / as.numeric(dminutes(time_interval_minutes))
  cloud_table <- data.frame(matrix(ncol = 1, nrow = number_of_interval_cloud / cloud_change_freq))
  colnames(cloud_table) <- c("x")
  
  # set.seed(1) # (!) enable this line if desired (see commenting above)
  cloud_table$cloud_transmission <- rnorm(n = number_of_interval_cloud / cloud_change_freq, mean = transmission_mean, sd = transmission_sd)
  
  time_interval_cloud_list <- seq(1, number_of_interval_cloud / cloud_change_freq, by = 1) 
  for (i in time_interval_cloud_list) {
    cloud_table[i, "datetime"] <- getMoonIllumination(date = date_time_start_cloud + ((i - 1) * (time_interval_minutes * cloud_change_freq) * 60))[1, "date"]
  }
  cloud_table <- subset(cloud_table, select = -c(x))
  
  par(mfrow = c(1,1))
  
  # Plot the spline fit to visualize cloud transmission that will be applied:
  mod.ss0 <- ss(cloud_table$datetime, cloud_table$cloud_transmission, all.knots = TRUE, lambda = (1 / number_of_interval_cloud) * 1e-12) 
  # The lambda multiplied constant can be reduced to create less abrupt transitions.
  # However, in most cases, the default 1e-12 can be left unchanged as it closely resembles the abrupt change of light caused by passing cloud.
  # An increase in the lambda value (e.g., to 1e-8) will make the transition slightly smoother but at the expense of narrowing the range of used values. 
  
  plot(mod.ss0, ylim = c(0, 1), xlab = "duration of cloud effect", ylab = "fraction of light that passes through cloud")
  points(cloud_table$datetime, cloud_table$cloud_transmission)
}

# Calculate the cloud effect on each minute
if (cloud_option == TRUE) {
  smoothing_cloud <- mod.ss0 # (!) select smoothing model from above
  
  time_interval_cloud_list_full <- seq(1, number_of_interval_cloud, by = 1)
  cloud_table_full <- data.frame(matrix(ncol = 1, nrow = number_of_interval_cloud))
  colnames(cloud_table_full) <- c("x")
  
  for (i in time_interval_cloud_list_full) {
    cloud_table_full[i, "datetime"] <- getMoonIllumination(date = date_time_start_cloud + (i - 1) * time_interval_minutes * 60)[1, "date"]
    cloud_table_full[i, "cloud_transmission"] <- predict(smoothing_cloud, cloud_table_full[i, "datetime"] , deriv = 0)[1, 2]
    if (cloud_table_full[i, "cloud_transmission"] > 1) {cloud_table_full[i, "cloud_transmission"] <- 1}
    if (cloud_table_full[i, "cloud_transmission"] < 0) {cloud_table_full[i, "cloud_transmission"] <- 0}
  }
  cloud_table_full <- subset(cloud_table_full, select = -c(x))
}

#--------------------------- END OF CLOUD EFFECT GENERATOR---------------------------
#--------------------------- END OF PARAMETER SETTINGS---------------------------

#---------------------------START OF ILLUMINATION COMPUTATION-------------------

# Start time formatting
date_time_start <- as_datetime(paste(date_start, time_start, sep = " ", collapse = NULL), tz = time_zone)
number_of_interval <- as.numeric(ddays(duration_day)) / as.numeric(dminutes(time_interval_minutes))

# Create an empty dataframe (to be filled during the for loop)
moon_value_table <- data.frame(matrix(ncol = 1, nrow = number_of_interval))
x <- c("x")
colnames(moon_value_table) <- x

# Create for loop [i] time interval list
time_interval_list <- seq(1, number_of_interval, by = 1) 

# Create a progress bar object
pb <- progress_bar$new(total = length(time_interval_list))

# Fill in empty data frame with suncalc data
for (i in time_interval_list) {
  moon_value_table[i, "datetime"] <- getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes * 60)[1, "date"]
  moon_value_table[i, "phase_angle"] <- (getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes * 60)[1, "phase"]) * (-360) + 180 #phase_angle = angular separation of the sun and Earth, as seen on the moon
  moon_value_table[i, "fraction"] <- (getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes*60)[1, "fraction"]) # moon illuminated fraction, not used in calculation. This is calculated only for user to learn about the moon phase.
  moon_value_table[i, "Z_moon"] <- 90 - (rad2deg(getMoonPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude)[1, "altitude"])) #Z_moon = Zenith distance in degree of the moon = 90 - moon altitude
  moon_value_table[i, "distance"] <- getMoonPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude)[1, "distance"] #distance = moon/Earth distance in km
  moon_value_table[i, "sun_altitude"] <- rad2deg(getSunlightPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude, keep = c("altitude"))[1, "altitude"]) #sun_altitude = altitude in degree of the sun
  pb$tick() # Update the progress bar
}
moon_value_table <- subset(moon_value_table, select = -c(x))

# Replace moon altitude that are lower than horizon_elev with NA (moon below horizon)
moon_value_table <- transform(moon_value_table, Z_moon = ifelse(Z_moon > 90, NA, Z_moon)) 

# Calculate atmospheric extinction
moon_value_table$atm_ext <- (-0.140194 * moon_value_table$Z_moon) / (-91.674385 + moon_value_table$Z_moon) - 0.03 # A Michaelis-Menten that fits Table 2 in Austin et al. (1976)
moon_value_table$atm_ext <- ifelse(moon_value_table$atm_ext < 0, 0, moon_value_table$atm_ext)

# Moon magnitude calculated from phase angle (unit in relative magnitude) (Allen 1976, p. 144)
moon_value_table$m <- (-12.73) + 0.026 * abs(moon_value_table$phase_angle) + 4 * (10 ^ -9) * (abs(moon_value_table$phase_angle) ^ 4)

# Temporary illuminance of moonlight (in unit foot candle) (see eq. (16) of Schaefer 1990a)
illuminance_temp <- 10 ^ ((-0.4) * (moon_value_table$m + moon_value_table$atm_ext + 16.57)) 
moon_value_table$illuminance_temp_lux <- illuminance_temp * 10.7639 #convert to lux

# Correct for the effect of site altitude (i.e., elevation)
atm_pressure_relative_to_sea <- patm(site_elev, patm0 = 101325) / 101325 # the atmospheric pressure at the site elevation relative to sea level
sea_555nm <- 18.964 * exp(-0.229 * 1) # Sea level irradiance at 555nm. Function extracted from figure 1 of Laue (1970)
elevated_555nm <- 18.964 * exp(-0.229 * atm_pressure_relative_to_sea) # Sea level irradiance at 555nm. Function extracted from figure 1 of Laue (1970)
increase_factor_elev <- elevated_555nm / sea_555nm 
moon_value_table$illuminance_temp_lux <- moon_value_table$illuminance_temp_lux * increase_factor_elev

# Apply lunar opposition surge when p < 6 (Buratti et al. 1996, figure 5)
moon_value_table <- transform(moon_value_table, illuminance_temp_lux = ifelse(abs(phase_angle) < 6, illuminance_temp_lux + ((0.4 * (6 - abs(phase_angle)) / 6) * illuminance_temp_lux), illuminance_temp_lux)) 
## A linear increase in moon brightness as phase angle decreases below 6

# Apply spreading out effect (angle of incidence) of light when illuminating at an angle (Austin et al. 1976)
moon_value_table$moon_final_lux <- moon_value_table$illuminance_temp_lux * sin(deg2rad(90 - moon_value_table$Z_moon))

# The moon/Earth distance effect (inverse square law) (Austin et al. 1976)
moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux * (1 / ((moon_value_table$distance / 384400) ^ 2))

# Waxing - waning asymmetric effect (simplified function derived from Austin et al. 1976 Table 1)
moon_value_table$moon_final_lux <- ifelse(moon_value_table$phase_angle < 0,
                                          moon_value_table$moon_final_lux * (-0.00026 * moon_value_table$phase_angle + 1),
                                          moon_value_table$moon_final_lux)

# Final moonlight illuminance (with a slight adjustment factor, calibrated from Leticia, Colombia, Aug 11, 2022 field full moon measurement)

moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux * 0.863
moon_value_table$moon_final_lux <- replace(moon_value_table$moon_final_lux, is.na(moon_value_table$moon_final_lux), 0)


#---------------------------APPLY CLOUD AND HORIZON ELEVATION EFFECT---------------------------

# Horizon elevation effect
if (horizon_option == TRUE) {
  moon_value_table <- transform(moon_value_table, moon_final_lux = ifelse((90 - Z_moon) > horizon_elev & (90 - Z_moon) < horizon_transition_end, 
                                                                          moon_final_lux - (moon_final_lux * (1 - horiz_transmission) * (abs(90 - Z_moon - horizon_transition_end) / (horizon_transition_end - horizon_elev))), moon_final_lux)) 
  moon_value_table <- transform(moon_value_table, moon_final_lux = ifelse((90 - Z_moon) < horizon_elev, moon_final_lux * horiz_transmission, moon_final_lux)) 
}

# Add baseline dark sky illuminance (Note: darsky_value is not affected by the horizon obstruction, but is subjected to the cloud effect)
moon_value_table$moon_final_lux[is.na(moon_value_table$moon_final_lux)] <- 0
moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux + darksky_value 

# Cloud effect
if (cloud_option == TRUE) {
  moon_value_table <- left_join(moon_value_table, cloud_table_full, by = "datetime")
  moon_value_table <- moon_value_table %>%
    mutate(cloud_transmission = if_else(is.na(cloud_transmission), 1, cloud_transmission))
  moon_value_table$moon_final_lux <- moon_value_table$moon_final_lux * moon_value_table$cloud_transmission
}

#---------------------------END OF ILLUMINATION COMPUTATION--------------------

#---------------------------GENERATE LED_schedule_moon.csv---------------------------

#Scale the model illumination to an intensity fraction by dividing it by theoretical_max
recreate_intensity_fraction <- moon_value_table$moon_final_lux / theoretical_max

#Calculate the RGBW crude and fine values for moonlight recreation
temp_white_intensity <- recreate_intensity_fraction * bit8 * white_fraction
crudewhite <- floor(temp_white_intensity)
wfine <- floor((temp_white_intensity - crudewhite) * diode_per_strip * strip_count)

temp_red_intensity <- recreate_intensity_fraction * bit8 * red_fraction
crudered <- floor(temp_red_intensity)
rfine <- floor((temp_red_intensity - crudered) * diode_per_strip * strip_count)

temp_green_intensity <- recreate_intensity_fraction * bit8 * green_fraction
crudegreen <- floor(temp_green_intensity)
gfine <- floor((temp_green_intensity - crudegreen) * diode_per_strip * strip_count)

temp_blue_intensity <- recreate_intensity_fraction * bit8 * blue_fraction
crudeblue <- floor(temp_blue_intensity)
bfine <- floor((temp_blue_intensity - crudeblue) * diode_per_strip * strip_count)

#Fill moon_value_table with LED color crude and fine values. NA converted to 0.
moon_value_table$crudewhite <- crudewhite
moon_value_table <- transform(moon_value_table, crudewhite = ifelse(is.na(crudewhite), 0, crudewhite)) 

moon_value_table$wfine <- wfine
moon_value_table <- transform(moon_value_table, wfine = ifelse(is.na(wfine), 0, wfine)) 

moon_value_table$crudered <- crudered
moon_value_table <- transform(moon_value_table, crudered = ifelse(is.na(crudered), 0, crudered)) 

moon_value_table$rfine <- rfine
moon_value_table <- transform(moon_value_table, rfine = ifelse(is.na(rfine), 0, rfine))

moon_value_table$crudegreen <- crudegreen
moon_value_table <- transform(moon_value_table, crudegreen = ifelse(is.na(crudegreen), 0, crudegreen)) 

moon_value_table$gfine <- gfine
moon_value_table <- transform(moon_value_table, gfine = ifelse(is.na(gfine), 0, gfine))

moon_value_table$crudeblue <- crudeblue
moon_value_table <- transform(moon_value_table, crudeblue = ifelse(is.na(crudeblue), 0, crudeblue)) 

moon_value_table$bfine <- bfine
moon_value_table <- transform(moon_value_table, bfine = ifelse(is.na(bfine), 0, bfine)) 

moon_value_table <- subset(moon_value_table, select = -c(atm_ext, m, illuminance_temp_lux)) # remove extra columns


# Save moon table csv file
write.csv(moon_value_table,"LED_schedule_moon.csv", row.names = TRUE)

# Explanation for the columns found in LED_schedule_moon.csv:
# Use whichever illuminance prediction is appropriate for desired use. 

## datetime = The datetime in a standard format that R and moonshine_moon.py can read
## phase_angle = the phase angle of the moon
## fraction = the illuminated fraction of the moon
## Z_moon = zenith distance of the moon in degree angle
## distance = the moon and Earth distance in km
## sun_altitude = The altitude of the sun. Positive/negative value means the sun is above/below the horizon, respectively.
## moon_final_lux = illuminance of moonlight (plus the darksky_value)
## crude and fine LED values for each RGBW = the LED values that moonshine_moon.py will use instruct the LED at the given time.

#---------------------------Plotting Section---------------------------

# Plotting the moonlight illuminance that will be re-created.
# Dark gray areas depict dark periods (true night after astronomical twilight ended).
# Light gray areas indicate periods of astronomical twilight.

# Create a clean ggplot theme
theme_rectangular_clean <-
  theme(axis.line = element_line(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank()) +
  theme(axis.text = element_text(size = 12, colour = 'black'),
        axis.title = element_text(size = 12, colour = 'black')) +
  theme(plot.title = element_text(size = 12)) +
  theme(plot.margin = unit(c(0.25,0.25,0.25,0.25),"cm"))

# Specify the time of night period and twilight period for shading
night_time <- filter(moon_value_table, sun_altitude < 0) %>% dplyr::select(datetime)
night_time <- as_datetime(night_time$datetime, tz = time_zone)

after_twilight_time <- filter(moon_value_table, sun_altitude < (-18)) %>% dplyr::select(datetime)
after_twilight_time <- as_datetime(after_twilight_time$datetime, tz =  time_zone)

day_time <- filter(moon_value_table, sun_altitude > 0) %>% dplyr::select(datetime)
day_time <- as_datetime(day_time$datetime, tz = time_zone)

# Plotting:
plot_output <- ggplot() + theme_rectangular_clean +
  geom_rect(aes(xmin = night_time, # night period
                xmax = night_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey88", alpha = 1, na.rm = TRUE) +
  geom_rect(aes(xmin = after_twilight_time, # after twilight
                xmax = after_twilight_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey80", alpha = 1, na.rm = TRUE) +
  geom_line(data = moon_value_table, aes(x = datetime, y = moon_final_lux), colour = 'black', linewidth = 0.75) +
  geom_rect(aes(xmin = day_time, # day time mask moonlight regression to gray color
                xmax = day_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "white", alpha = 0.85, na.rm = TRUE) +
  scale_y_continuous(limits = c(0, 0.3), # change the y-axis range here
                     breaks = c(seq(from = 0, to = 0.3, by = 0.1))) + # change the y-axis breaks here
  scale_x_datetime(date_breaks = "1 day") + # change the date break here for different x-axis label. More specific format can be specified.
  labs(x = "", y = "predicted ground illuminance (lx)") 


plot_output

beep()

# Save plot:
ggsave("moon_plot_output.png", plot_output, width = 4488, height = 2000, units = "px", scale = 1, dpi = 450)
## .png can be changed to .pdf to save as a vector file.
## However when exporting as .pdf, the shading transparency (alpha setting) might not look right. This is a limitation of R.

#---------------------------Lunar eclipse warning---------------------------

# MoonShineR warns the user if an eclipse occurs during a simulation, and it reports the start and end time of the simulation.
# However, MoonShineR does not simulate the reduction in moon ground illuminance associated with the eclipse.

if (any(abs(moon_value_table$phase_angle) < 1.5 & moon_value_table$sun_altitude < 0)) { # eclipse defined as a moon with phase angle < 1.5 during nighttime
  print("ECLIPSE IN SIMULATION!!!")
  eclipse_list <- (abs(moon_value_table$phase_angle) < 1.5 & moon_value_table$sun_altitude < 0)
  moon_value_table[which(eclipse_list == TRUE),]
} else {
  print("no eclipse in simulation")
}

#---------------------------END OF SCRIPT---------------------------

# References ---------------------------  

# Allen, C. W. (1976). Astrophysical quantities (3rd ed. 1973, Repr. with corrections 1976). Athelone Press.; [Distributor for] U.S.A. and Canada, Humanities Press.
# Austin, R. H., Phillips, B. F., & Webb, D. J. (1976). A method for calculating moonlight illuminance at the earth’s surface. The Journal of Applied Ecology, 13(3), 741. https://doi.org/10.2307/2402251
# Buratti, B. J., Hillier, J. K., & Wang, M. (1996). The lunar opposition surge: Observations by clementine. Icarus, 124(2), 490–499. https://doi.org/10.1006/icar.1996.0225
# Hänel, A., Posch, T., Ribas, S. J., Aubé, M., Duriscoe, D., Jechow, A., Kollath, Z., Lolkema, D. E., Moore, C., Schmidt, N., Spoelstra, H., Wuchterl, G., & Kyba, C. C. M. (2018). Measuring night sky brightness: Methods and challenges. Journal of Quantitative Spectroscopy and Radiative Transfer, 205, 278–290. https://doi.org/10.1016/j.jqsrt.2017.09.008
# Krisciunas, K., & Schaefer, B. E. (1991). A model of the brightness of moonlight. Publications of the Astronomical Society of the Pacific, 103, 1033. https://doi.org/10.1086/132921
# Laue, E. G. (1970). The measurement of solar spectral irradiance at different terrestrial elevations. Solar Energy, 13(1), 43–57. https://doi.org/10.1016/0038-092X(70)90006-X
# Schaefer, B. E. (1990). Telescopic limiting magnitudes. Publications of the Astronomical Society of the Pacific, 102, 212. https://doi.org/10.1086/132629
# Seidelmann, P. K., United States Naval Observatory, & Great Britain (Eds.). (1992). Explanatory supplement to the Astronomical almanac (Rev. ed.). University Science Books.

# Notes ---------------------------  

## Be careful with radian and degree angle
### Calculations in Krisciunas & Scaefer 1991 model uses degree angle
### suncalc functions gives radian. R trigonometry function takes radian.

## Zenith distance of the moon = 90 degree angle - moon altitude

## Phase output from suncalc::getMoonIllumination:
### 0 = new moon
### 0.25 = first quarter (waxing)
### 0.5 = full
### 0.75 = third/last quarter (waning)

## To convert phase to phase angle (following the sign convention of Krisciunas & Schaefer 1991):
### phase_angle <- phase*(-360)+180
#### positive = waxing 
#### negative = waning 
#### 180 = new moon
#### 90 = 1st quarter (waxing)
#### 0 = full
#### -90 = 2nd quarter (waning)
```

### <span style="font-variant:small-caps;">MoonShineR</span>: Sunlight/twilight scheduler

```r
# MoonShineR - Sunlight/twilight LED scheduler
# An R program by C. Lok Poon, Crampton Electric Fish Lab, University of Central Florida, Copyright 2023
# A detailed guide about this program: https://lokpoon.github.io/moonshine_manual/sunlight_twilight_LED_scheduler.html

# Description:
# This script generates an LED_schedule_sun.csv schedule file for MoonShineP to re-create a sunlight/twilight regime.

# Load libraries ----------------------------

library(dplyr)
library(suncalc)
library(lubridate)
library(REdaS)
library(ggplot2)
library(beepr)
library(stats)
library(npreg)
library(progress)

#---------------------------START OF PARAMETER SETTINGS---------------------------

# (!) indicates a user specified setting

# Set working directory
setwd("/Users/lokpoon/Desktop") # (!) Set working directory. Place R program here. .csv and .jpg files will be saved to this directory

# Set the location and time ---------------------------
latitude <- -4.21528 # (!) Latitude in decimal degrees (e.g., -4.21528)
longitude <- -69.94056 # (!) Longitude in decimal degrees (e.g., -69.94056)

time_zone <- "EST" # (!) Set the time zone for the location set (e.g., “EST”). REMEMBER TO CHANGE THE TIME ZONE WHEN THE LOCATION IS CHANGED.
# For a list of time zone names, enter OlsonNames(tzdir = NULL) in R console
# Highly recommend using a time zone without DST. E.g., use "EST" instead of "America/New_York"
date_start <- "2023-03-01" # (!) Starting date of the simulation (YYYY-MM-DD)
time_start <- "18:00:00" # (!) Starting time of the simulation (hh:mm:ss)
duration_day <- 1 # (!) Duration of simulation in days

# LED strip configuration ---------------------------

theoretical_max <- 600 # (!) Define an intensity upper limit (in lx) so that the LED system is not instructed to exceed 100% output intensity.
## Refer to online MoonShineP Manual part 7.
## Increasing theoretical_max will reduce the illuminance to the LED.

diode_per_strip <- 144 # (!) Number of LEDs per strip
strip_count <- 4 # (!) Number of daisy-chained LED strips

# Apply color shift  ---------------------------
# Pick either to use realistic_sunlight or a manual spectral shift.
# If realistic_sunlight is TRUE, an automatic spectral shift is applied, and the manual spectral shift is ignored.
# If realistic_sunlight is FALSE, the manual spectral shift is applied.

# LED spectral control---------------------------
# A) Default realistic twilight and sunlight spectral change. 
realistic_sunlight <- TRUE # (!) TRUE to enable
# This automatically sets the color spectrum to a realistic color of sunlight and twilight. It simulates the color change during sunrise/set and twilight periods (Palmer & Johnsen 2015) according to the sun's altitude.
# If realistic_sunlight is enabled, it will override and ignore the manual spectral shift settings in the next section.

# B) Manual spectral shift (a constant shift, does not change with sun's altitude)
# This can be used to approximate a specific light spectrum of habitat or anthropogenic light.
# Input the intensity fraction (0-1) each LED color is outputting. Each is independent. 
white_fraction <- 1.0 # (!) White. Default = 1.0
red_fraction <- 0.08 # (!) Red. Default = 0.08
green_fraction <- 0.36 # (!) Green. Default = 0.36
blue_fraction <- 0.19 # (!) Blue. Default = 0.19
# The default values approximate the sunlight spectrum.
# To change color balance from white to, for example, a blue-shifted light, the user can decrease other color fractions except for blue_fraction, incrementally, until the color generated by lightbox reaches desired parameters on a spectrometer.
# Please recognize the narrow band nature of the RGB LED and utilize it accordingly.

#---------------------------END OF PARAMETER SETTINGS---------------------------

#---------------------------START OF ILLUMINATION COMPUTATION---------------------------

time_interval_minutes <- 1 # The temporal resolution of the simulation in minutes. Locked at 1 for MoonShineP to operate correctly.
bit8 <- 255 # Controllable light intensity level of the LEDs is 255 (8 bit).

# Start time formatting
date_time_start <- as_datetime(paste(date_start, time_start, sep = " ", collapse = NULL), tz = time_zone)
number_of_interval <- as.numeric(ddays(duration_day)) / as.numeric(dminutes(time_interval_minutes))

# Create an empty dataframe (to be filled during the for loop)
sun_value_table <- data.frame(matrix(ncol = 1, nrow = number_of_interval))
x <- c("x")
colnames(sun_value_table) <- x

# Create for loop [i] time interval list
time_interval_list <- seq(1, number_of_interval, by = 1) 

# Create a progress bar object
pb <- progress_bar$new(total = length(time_interval_list))

# Fill in empty data frame with suncalc data
for (i in time_interval_list) {
  sun_value_table[i, "datetime"] <- getMoonIllumination(date = date_time_start + (i - 1) * time_interval_minutes * 60)[1, "date"]
  sun_value_table[i, "sun_altitude"] <- rad2deg(getSunlightPosition(date = date_time_start + (i - 1) * time_interval_minutes * 60, lat = latitude, lon = longitude, keep = c("altitude"))[1, "altitude"]) #sun_altitude = altitude of the sun in degree
  pb$tick() # Update the progress bar
}
sun_value_table <- subset(sun_value_table, select = -c(x))

# Calculate twilight illuminance
# Following the polynomial function in Seidelmann (1992) p. 491
sun_value_table$twilight <- 0
sun_value_table$twilight <- ifelse(sun_value_table$sun_altitude < 0 & sun_value_table$sun_altitude > -0.8,
                                    10 ^ (2.88 + (22.26 * (sun_value_table$sun_altitude / 90)) - 207.64 * ((sun_value_table$sun_altitude / 90) ^ 2) + 1034.3 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$twilight)
sun_value_table$twilight <- ifelse(sun_value_table$sun_altitude < -0.8 & sun_value_table$sun_altitude > -5,
                                    10 ^ (2.88 + (21.81 * (sun_value_table$sun_altitude / 90)) - 258.11 * ((sun_value_table$sun_altitude / 90) ^ 2) - 858.36 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$twilight)
sun_value_table$twilight <- ifelse(sun_value_table$sun_altitude < -5 & sun_value_table$sun_altitude > -12,
                                    10 ^ (2.7 + (12.17 * (sun_value_table$sun_altitude / 90)) - 431.69 * ((sun_value_table$sun_altitude / 90) ^ 2) - 1899.83 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$twilight)
sun_value_table$twilight <- ifelse(sun_value_table$sun_altitude < -12 & sun_value_table$sun_altitude > -18,
                                    10 ^ (13.84 + (262.72 * (sun_value_table$sun_altitude / 90)) + 1447.42 * ((sun_value_table$sun_altitude / 90) ^ 2) + 2797.93 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$twilight)

# Calculate sunlight (SUN > 0 degree) illuminance---------------------------
# Following the polynomial function in Seidelmann (1992) p. 491
sun_value_table$sunlight <- 0
sun_value_table$sunlight <- ifelse(sun_value_table$sun_altitude > 20,
                                    10 ^ (3.74 + (3.97 * (sun_value_table$sun_altitude / 90)) - 4.07 * ((sun_value_table$sun_altitude / 90) ^ 2) + 1.47 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$sunlight)
sun_value_table$sunlight <- ifelse(sun_value_table$sun_altitude < 20 & sun_value_table$sun_altitude > 5,
                                    10 ^ (3.05 + (13.28 * (sun_value_table$sun_altitude / 90)) - 45.98 * ((sun_value_table$sun_altitude / 90) ^ 2) + 64.33 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$sunlight)
sun_value_table$sunlight <- ifelse(sun_value_table$sun_altitude < 5 & sun_value_table$sun_altitude > 0,
                                    10 ^ (2.88 + (22.26 * (sun_value_table$sun_altitude / 90)) - 207.64 * ((sun_value_table$sun_altitude / 90) ^ 2) + 1034.3 * ((sun_value_table$sun_altitude / 90) ^ 3)), sun_value_table$sunlight)

# Add sunlight and twilight together
sun_value_table$raw_twilight_sun <- sun_value_table$twilight + sun_value_table$sunlight # add twilight and sunlight illuminance together
sun_value_table$raw_twilight_sun <- illuminance_fraction * sun_value_table$raw_twilight_sun # apply illuminance_fraction
sun_value_table <- transform(sun_value_table, adjusted_twilight_sun = ifelse(raw_twilight_sun > theoretical_max, theoretical_max, raw_twilight_sun)) # apply the ceiling for sunlight recreation

#---------------------------END OF ILLUMINATION COMPUTATION---------------------------

#---------------------------GENERATE LED_schedule_sun.csv---------------------------

# scale the predicted illuminance to an intensity fraction by dividing it by the theoretical_max
recreate_intensity_fraction <- sun_value_table$adjusted_twilight_sun / theoretical_max

# To simulate realistic color change according to the sun altitude, create curve functions for each RGBW:
# Make a table of sun's altitude ~ LED intensity fraction for each RGBW
color_change_matrix <- matrix(c(90, 1, 0.08, 0.6, 0.4,
                                42, 1, 0.08, 0.6, 0.4,
                                12, 1, 0.08, 0.46, 0.26,
                                6, 1, 0.1, 0.4, 0.2,
                                0, 1, 0.16, 0.34, 0.12,
                                -2, 0.99, 0.3, 0.34, 0.13,
                                -4, 0.95, 0.4, 0.38, 0.18,
                                -6.5, 0.7, 0.15, 0.7, 0.9,
                                -18, 0.6, 0.08, 0.8, 1), ncol = 5, byrow = TRUE)

colnames(color_change_matrix) <- c("sun_altitude","white","red", "green", "blue")
color_change_matrix <- as.data.frame(color_change_matrix)

time_interval <- seq(1, nrow(sun_value_table), by = 1)
color_table <- data.frame(matrix(ncol = 1, nrow = nrow(sun_value_table)))
colnames(color_table) <- c("x")

# Fit a smooth spline curve to the table values
# (!) Remove commenting in the next 15 lines (plot & points) if you want to see how the LED color changes according to sun altitude:
white_curve <- ss(color_change_matrix$sun_altitude, color_change_matrix$white, df = 8, m = 1)
#plot(white_curve, ylim = c(0, 1), xlab = "sun_altitude", ylab = "led intensity", main = "color curve for white")
#points(color_change_matrix$sun_altitude, color_change_matrix$white)

red_curve <- ss(color_change_matrix$sun_altitude, color_change_matrix$red, df = 8, m = 1)
#plot(red_curve, ylim = c(0, 1), xlab = "sun_altitude", ylab = "led intensity", main = "color curve for red")
#points(color_change_matrix$sun_altitude, color_change_matrix$red)

green_curve <- ss(color_change_matrix$sun_altitude, color_change_matrix$green, df = 8, m = 1)
#plot(green_curve, ylim = c(0, 1), xlab = "sun_altitude", ylab = "led intensity", main = "color curve for green")
#points(color_change_matrix$sun_altitude, color_change_matrix$green)

blue_curve <- ss(color_change_matrix$sun_altitude, color_change_matrix$blue, df = 8, m = 1)
#plot(blue_curve, ylim = c(0, 1), xlab = "sun_altitude", ylab = "led intensity", main = "color curve for blue")
#points(color_change_matrix$sun_altitude, color_change_matrix$blue)

# Create a progress bar object
pb2 <- progress_bar$new(total = length(time_interval_list))

if (realistic_sunlight == TRUE) {
  for (i in time_interval) {
    color_table$datetime <- sun_value_table$datetime
    color_table$sun_altitude <- sun_value_table$sun_altitude
    
    color_table[i, "white"] <- predict(white_curve , color_table[i, "sun_altitude"] , deriv = 0)[1, 2]
    if (color_table[i, "white"] > 1) {color_table[i, "white"] <- 1}
    if (color_table[i, "white"] < 0) {color_table[i, "white"] <- 0}
    color_table$white <- round(color_table$white, digits = 2)
    
    color_table[i, "red"] <- predict(red_curve , color_table[i, "sun_altitude"] , deriv = 0)[1, 2]
    if (color_table[i, "red"] > 1) {color_table[i, "red"] <- 1}
    if (color_table[i, "red"] < 0) {color_table[i, "red"] <- 0}
    color_table$red <- round(color_table$red, digits = 2)
    
    color_table[i, "green"] <- predict(green_curve , color_table[i, "sun_altitude"] , deriv = 0)[1, 2]
    if (color_table[i, "green"] > 1) {color_table[i, "green"] <- 1}
    if (color_table[i, "green"] < 0) {color_table[i, "green"] <- 0}
    color_table$green <- round(color_table$green, digits = 2)
    
    color_table[i, "blue"] <- predict(blue_curve , color_table[i, "sun_altitude"] , deriv = 0)[1, 2]
    if (color_table[i, "blue"] > 1) {color_table[i, "blue"] <- 1}
    if (color_table[i, "blue"] < 0) {color_table[i, "blue"] <- 0}
    color_table$blue <- round(color_table$blue, digits = 2)
    pb2$tick() # Update the progress bar
    
    white_fraction <- 1.0 
    red_fraction <- 1.0 
    green_fraction <- 1.0 
    blue_fraction <- 1.0
  }
  }else {
    color_table$datetime <- sun_value_table$datetime
    color_table$sun_altitude <- sun_value_table$sun_altitude
    
    color_table$white <- 1
    color_table$red <- 1
    color_table$green <- 1
    color_table$blue <- 1
  }
color_table <- subset(color_table, select = -c(x))


#Calculate the RGBW crude and fine values for the light recreation
color_table$temp_white_intensity <- recreate_intensity_fraction * bit8 * white_fraction * color_table$white
color_table$crudewhite <- floor(color_table$temp_white_intensity)
color_table$wfine <- floor((color_table$temp_white_intensity - color_table$crudewhite) * diode_per_strip * strip_count)

color_table$temp_red_intensity <- recreate_intensity_fraction * bit8 * red_fraction * color_table$red
color_table$crudered <- floor(color_table$temp_red_intensity)
color_table$rfine <- floor((color_table$temp_red_intensity - color_table$crudered) * diode_per_strip * strip_count)

color_table$temp_green_intensity <- recreate_intensity_fraction * bit8 * green_fraction * color_table$green
color_table$crudegreen <- floor(color_table$temp_green_intensity)
color_table$gfine <- floor((color_table$temp_green_intensity - color_table$crudegreen) * diode_per_strip * strip_count)

color_table$temp_blue_intensity <- recreate_intensity_fraction * bit8 * blue_fraction * color_table$blue
color_table$crudeblue <- floor(color_table$temp_blue_intensity)
color_table$bfine <- floor((color_table$temp_blue_intensity - color_table$crudeblue) * diode_per_strip * strip_count)

#Fill sun_value_table with LED color crude and fine values. NA converted to 0.
sun_value_table$crudewhite <- color_table$crudewhite
sun_value_table <- transform(sun_value_table, crudewhite = ifelse(is.na(crudewhite), 0, crudewhite)) 

sun_value_table$wfine <- color_table$wfine
sun_value_table <- transform(sun_value_table, wfine = ifelse(is.na(wfine), 0, wfine)) 

sun_value_table$crudered <- color_table$crudered
sun_value_table <- transform(sun_value_table, crudered = ifelse(is.na(crudered), 0, crudered)) 

sun_value_table$rfine <- color_table$rfine
sun_value_table <- transform(sun_value_table, rfine = ifelse(is.na(rfine), 0, rfine))

sun_value_table$crudegreen <- color_table$crudegreen
sun_value_table <- transform(sun_value_table, crudegreen = ifelse(is.na(crudegreen), 0, crudegreen)) 

sun_value_table$gfine <- color_table$gfine
sun_value_table <- transform(sun_value_table, gfine = ifelse(is.na(gfine), 0, gfine))

sun_value_table$crudeblue <- color_table$crudeblue
sun_value_table <- transform(sun_value_table, crudeblue = ifelse(is.na(crudeblue), 0, crudeblue)) 

sun_value_table$bfine <- color_table$bfine
sun_value_table <- transform(sun_value_table, bfine = ifelse(is.na(bfine), 0, bfine))

sun_value_table <- subset(sun_value_table, select = -c(twilight, sunlight, raw_twilight_sun))

# Save twilight_sun_table csv file
write.csv(sun_value_table,"LED_schedule_sun.csv", row.names = TRUE)

# Explanation for the columns found in LED_schedule_sunlight_twilight).csv:
## datetime = The datetime in a standard format that R and moonshine_sun.py can read
## sun_altitude = The altitude of the sun. Positive/negative value means the sun is above/below the horizon, respectively.
## adjusted_twilight_sun = the combined illuminance of the sunlight and twilight, capped at the theoretical_max
## crude and fine LED values for each RGBW = the LED values that moonshine_sun.py will use instruct the LED at the given time

#---------------------------Plotting Section---------------------------

# Plot the sunlight and twilight illuminance that will be re-created.
# Dark gray areas depict dark periods (true night after astronomical twilight ended).
# Light gray areas indicate the periods of astronomical twilight.

# Create a clean ggplot theme
theme_rectangular_clean <-
  theme(axis.line = element_line(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank()) +
  theme(axis.text = element_text(size = 12, colour = 'black'),
        axis.title = element_text(size = 12, colour = 'black')) +
  theme(plot.title = element_text(size = 12)) +
  theme(plot.margin = unit(c(0.25,0.25,0.25,0.25),"cm"))

# Specify the time of night period and twilight period for shading
night_time <- filter(sun_value_table, sun_altitude < 0) %>% dplyr::select(datetime)
night_time <- as_datetime(night_time$datetime, tz = time_zone)

after_twilight_time <- filter(sun_value_table, sun_altitude < (-18)) %>% dplyr::select(datetime)
after_twilight_time <- as_datetime(after_twilight_time$datetime, tz =  time_zone)

day_time <- filter(sun_value_table, sun_altitude > 0) %>% dplyr::select(datetime)
day_time <- as_datetime(day_time$datetime, tz = time_zone)

#Plotting
plot_output <- ggplot() + theme_rectangular_clean +
  geom_rect(aes(xmin = night_time, # night period
                xmax = night_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey88", alpha = 1, na.rm = TRUE) +
  geom_rect(aes(xmin = after_twilight_time, # after twilight
                xmax = after_twilight_time + dminutes(time_interval_minutes),
                ymin = 0, ymax = Inf), fill = "grey80", alpha = 1, na.rm = TRUE) +
  geom_line(data = sun_value_table, aes(x = datetime, y = adjusted_twilight_sun), colour = 'black', linewidth = 0.75) +
  scale_y_continuous(limits = c(0, 600), # change the y-axis range here
    breaks = c(seq(from = 0, to = 600, by = 50))) + # change the y-axis breaks here
  scale_x_datetime(date_breaks = "1 day") + # change the date break here for different x-axis label.
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) + # rotate date label 90 degree.
  labs(x = "", y = "predicted ground illuminance (lx)") 

plot_output

beep()

# To save plot, remove commenting in the next line:
ggsave("sunlight_twilight_output.png", plot_output, width = 4488, height = 2400, units = "px", scale = 1, dpi = 450)
## .png can be changed to .pdf to save as a vector file.
## However when exporting as .pdf, the shading transparency (alpha setting) might not look right. This is a limitation of R.


#---------------------------END OF SCRIPT---------------------------

# References ---------------------------  

# Allen, C. W. (1976). Astrophysical quantities (3rd ed. 1973, Repr. with corrections 1976). Athelone Press.; [Distributor for] U.S.A. and Canada, Humanities Press.
# Austin, R. H., Phillips, B. F., & Webb, D. J. (1976). A method for calculating moonlight illuminance at the earth’s surface. The Journal of Applied Ecology, 13(3), 741. https://doi.org/10.2307/2402251
# Buratti, B. J., Hillier, J. K., & Wang, M. (1996). The lunar opposition surge: Observations by clementine. Icarus, 124(2), 490–499. https://doi.org/10.1006/icar.1996.0225
# Hänel, A., Posch, T., Ribas, S. J., Aubé, M., Duriscoe, D., Jechow, A., Kollath, Z., Lolkema, D. E., Moore, C., Schmidt, N., Spoelstra, H., Wuchterl, G., & Kyba, C. C. M. (2018). Measuring night sky brightness: Methods and challenges. Journal of Quantitative Spectroscopy and Radiative Transfer, 205, 278–290. https://doi.org/10.1016/j.jqsrt.2017.09.008
# Krisciunas, K., & Schaefer, B. E. (1991). A model of the brightness of moonlight. Publications of the Astronomical Society of the Pacific, 103, 1033. https://doi.org/10.1086/132921
# Palmer, G., & Johnsen, S. (2015). Downwelling spectral irradiance during evening twilight as a function of the lunar phase. Applied Optics, 54(4), B85. https://doi.org/10.1364/AO.54.000B85
# Schaefer, B. E. (1990). Telescopic limiting magnitudes. Publications of the Astronomical Society of the Pacific, 102, 212. https://doi.org/10.1086/132629
# Seidelmann, P. K., United States Naval Observatory, & Great Britain (Eds.). (1992). Explanatory supplement to the Astronomical almanac (Rev. ed.). University Science Books.
```

### <span style="font-variant:small-caps;">MoonShineP</span>: `moonshine_moon.py`

```python


import time                


from rpi_ws281x import *  # To control the LEDs


import argparse


import csv                # To work with csv files


import os





#-------------------------------------------------------



# Function to clear terminal







LED_COUNT      = 288     # Number of LEDs



LED_PIN        = 18      # GPIO pin connected to the LED strip



LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)



LED_DMA        = 10      # DMA channel to use for generating signal (try 10)



LED_BRIGHTNESS = 255    # 255 levels



LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)



LED_CHANNEL    = 0       # Set to '1' for GPIOs 13, 19, 41, 45 or 53



LED_STRIP = ws.SK6812_STRIP_GRBW    # The GRBW order is correct for addressing the corrosponding channels on the BTF-Lighting LED strips. The order of the GRBW letters can be rearranged to accommodate another RGBW protocol.



# This funtion retrieves the Pi current time using the time library and returns it
def gettime():
    # Epoch time
    etime = time.time()
    # Convert to local time
    ltime = time.localtime(etime)
    # Return the results as separate variables in the correct format
    return time.strftime("%Y", ltime),time.strftime("%m", ltime),time.strftime("%d", ltime),time.strftime("%H", ltime),time.strftime("%M", ltime),time.strftime("%S", ltime)



 # Return epoch time
def timestart():

    etime=time.time()

    ltime= time.ctime(etime)

    return etime


# Defines class led
class led:

    def __init__(self,r,g,b,w):

        self.r=r

        self.g=g

        self.b=b

        self.w=w


# Print the input for a specific LED on the strip
def printled(strip,i):
  # Opens log.txt to append
  file = open("/home/pi/Desktop/control_moon/log.txt", "a")
  # This is where the data is written to the file
  file.write('\n| led ' + str(i) + ' r ' + str(strip[i].r) + ' g ' +str(strip[i].g) + ' b ' +str(strip[i].b) + ' w ' + str(strip[i].w) + '|')
  file.close()

  # Print the same to the terminal
  print("----------------------------")

  print('| led ' + str(i) + ' r ' + str(strip[i].r) + ' g ' +str(strip[i].g) + ' b ' +str(strip[i].b) + ' w ' + str(strip[i].w) + '|')

  print("----------------------------")


# Creates a "virtual strip" for calculating the intensity level of each LEDs
def fillvstrip(LED_COUNT,STRIP,rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine):
# All LEDs in the strip are assigned the apropriate "fill" intensity level
    for i in range(LED_COUNT):
# Red diode
        STRIP[i].r =rfill;
# Green diode
        STRIP[i].g =gfill;
# Blue diode
        STRIP[i].b= bfill;
# White diode
        STRIP[i].w= wfill;
# Variables are set to one and are used as counters for increasing the LEDs properly
    rcount1,rcount2=1,1

    gcount1,gcount2=1,1

    bcount1,bcount2=1,1 

    wcount1,wcount2=1,1

# For every LED in the range of the fine level, alter the red diode if neccisary.
    for i in range(rfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
            # Increase brigness by one
           STRIP[i-rcount2].r = rfill+1
            # Increase counter
           rcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-rcount1+1].r = rfill+1 
            # Increase counter
            rcount1 +=1


# For every LED in the range of the fine level, alter the green diode if neccisary.
    for i in range(gfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
            # Increase brigness by one
            STRIP[i-gcount2].g = gfill+1
            # Increase counter
            gcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-gcount1+1].g = gfill+1 
            # Increase counter
            gcount1 +=1     


# For every LED in the range of the fine level, alter the blue diode if neccisary.
    for i in range(bfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
           # Increase brigness by one
           STRIP[i-bcount2].b = bfill+1
            # Increase counter
           bcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-bcount1+1].b = bfill+1 
            # Increase counter
            bcount1 +=1

# For every LED in the range of the fine level, alter the white diode if neccisary.
    for i in range(wfine):
        # if odd number index
        if i % 2 != 0:
            # Increase brigness by one
            STRIP[i - wcount2].w = wfill + 1
            # Increase counter
            wcount2 += 1

        else:
            # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i + int((LED_COUNT / 2)) - wcount1 + 1].w = wfill + 1
            # Increase counter
            wcount1 += 1



    return STRIP 


# Take the strip and virtual strip as parameters. prints virtual strip to real strip
def colorWipe3(strip, vstrip):


# For every LEDs
    for i in range(strip.numPixels()):
        # Variable holds color made from the values found in the virtual strip
        color=Color(vstrip[i].r,vstrip[i].g,vstrip[i].b,vstrip[i].w)
        # Set pixel color of real led to virtual led level
        strip.setPixelColor(i, color)
    # Execute changes
    strip.show()



       

def clear():



    command = 'clear'



    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls



        command = 'cls'



    os.system(command)



    clear()











# Funtion to match a search term to find a specific row
# Input is a csv file. It requires the term being searched for, and the title of the column you are searching in



def search(filename,term):


    # Open the csv that is passed as filename
    with open(filename, newline='') as csvfile:


        # Reader variable that can be parsed
        reader = csv.DictReader(csvfile)



        search=1  


        # Parsing through all rows in the reader
        for row in reader:


            # When the value is found in the column "datetime"  that matches the current Pi time
            if row['datetime'] == term:
                # Open the log
                file = open("/home/pi/Desktop/control_moon/log.txt", "a")
                # Print the data that is found in the csv
                file.write("found at "+str(term)+" "+str(row['crudered'])+str(row['rfine'])+str(row['crudegreen'])+str(row['gfine'])+str(row['crudeblue'])+str(row['bfine'])+str(row['crudewhite'])+str(row['wfine']))
                # Close log
                file.close()                                                         
                # Print the same to the terminal
                print("found at ",term," ",row['crudered'],row['rfine'],row['crudegreen'],row['gfine'],row['crudeblue'],row['bfine'],row['crudewhite'],row['wfine'])



                search=0


                # Returns the values found under their respective headers in the csv
                return (row['crudered'],row['rfine'],row['crudegreen'],row['gfine'],row['crudeblue'],row['bfine'],row['crudewhite'],row['wfine'])



  



    



# Main program logic follows:



if __name__ == '__main__':



    # Process arguments



    parser = argparse.ArgumentParser()



    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')



    args = parser.parse_args()







    # Create NeoPixel object with appropriate configuration.



    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)



    # Intialize the library (must be called once before other functions).



    strip.begin()


    # Initializing variables for future use
    rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine=0,0,0,0,0,0,0,0

    vstrip=[]



    # In range of number of lights assigned by LED_COUNT
    vstrip = [led(0,1,2,3) for i in range(LED_COUNT)]


    # Assign the variable vstrip by calling fillvstrip(). This initializes the strip and assigns all power levels the value of 0
    vstrip = fillvstrip(LED_COUNT,vstrip,rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine)



    try:
        # Clear log from last time the code was ran
        file = open("/home/pi/Desktop/control_moon/log.txt", "w")

        file.close()

        while True:


            # Get the real current time and assign appropriate variables for futute formatiing
            year,month,day,hour,minute,second=gettime()


            # This code will continue when the current time is a whole minute. This is because the data found in the csv is going to be at one-minute intervals
            if(second=="00"):

                # Creates a string which is formated the same as the "datetime" row in the csv
                searcht=str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
                # Hold values returned by search function
                result = search('/home/pi/Desktop/control_moon/LED_schedule_moon.csv', searcht)
                # If result is not null, a data was found
                if result:
                    # Assign it to its respective variable
                    rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine = result

                else:
                    # If null
                    print("No matching term was found in the CSV file")

                # Casecatching for if there is a matching datetime but no brightness values found at that time. This would occur when the moon is not above the horizion
                if (rfill == "#VALUE!"):

                    rfill = 1



                if (rfine == "#VALUE!"):

                    rfine = 1



                if (gfill == "#VALUE!"):

                    gfill = 1



                if (gfine == "#VALUE!"):

                    gfine = 1



                if (bfill == "#VALUE!"):

                    bfill = 1



                if (bfine == "#VALUE!"):

                    bfine = 1



                if (wfill == "#VALUE!"):

                    wfill = 1



                if (wfine == "#VALUE!"):

                    wfine = 1

                
                # Casting all values to int data type
                rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine = int(rfill), int(rfine), int(gfill), int(gfine), int(bfill), int(bfine), int(wfill), int(wfine)

                



                

        

                              
                # Fill the virtual strip with the values found in the csv
                vstrip = fillvstrip(LED_COUNT, vstrip, rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine)

              




                # Apply changes to real strip, making it match the data stored in the virtual strip
                colorWipe3(strip, vstrip)






                # Print what should be displaying on the light strip for the given number of LEDs 
                for i in range(3):  # Parameter is number of LEDs from virtual strip that are printed



                    printled(vstrip, i)



                time.sleep(52)  # Parameter is time in seconds the program will wait before checking the clock again



            

   

    except KeyboardInterrupt:



        if args.clear:



            colorWipe(strip, Color(0,0,0,0), 10)






```

### <span style="font-variant:small-caps;">MoonShineP</span>: `moonshine_sun.py`

```python


import time                


from rpi_ws281x import *  # To control the LEDs


import argparse


import csv                # To work with csv files


import os





#-------------------------------------------------------



# Function to clear terminal







LED_COUNT      = 576     # Number of LEDs



LED_PIN        = 21      # GPIO pin connected to the LED strip



LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)



LED_DMA        = 10      # DMA channel to use for generating signal (try 10)



LED_BRIGHTNESS = 255    # 255 levels



LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)



LED_CHANNEL    = 0       # Set to '1' for GPIOs 13, 19, 41, 45 or 53



LED_STRIP = ws.SK6812_STRIP_GRBW    # The GRBW order is correct for addressing the corrosponding channels on the BTF-Lighting LED strips. The order of the GRBW letters can be rearranged to accommodate another RGBW protocol.



# This funtion retrieves the Pi current time using the time library and returns it
def gettime():
    # Epoch time
    etime = time.time()
    # Convert to local time
    ltime = time.localtime(etime)
    # Return the results as separate variables in the correct format
    return time.strftime("%Y", ltime),time.strftime("%m", ltime),time.strftime("%d", ltime),time.strftime("%H", ltime),time.strftime("%M", ltime),time.strftime("%S", ltime)



 # Return epoch time
def timestart():

    etime=time.time()

    ltime= time.ctime(etime)

    return etime


# Defines class led
class led:

    def __init__(self,r,g,b,w):

        self.r=r

        self.g=g

        self.b=b

        self.w=w


# Print the input for a specific LED on the strip
def printled(strip,i):
  # Opens log.txt to append
  file = open("/home/pi/Desktop/control_sun/log.txt", "a")
  # This is where the data is written to the file
  file.write('\n| led ' + str(i) + ' r ' + str(strip[i].r) + ' g ' +str(strip[i].g) + ' b ' +str(strip[i].b) + ' w ' + str(strip[i].w) + '|')
  file.close()

  # Print the same to the terminal
  print("----------------------------")

  print('| led ' + str(i) + ' r ' + str(strip[i].r) + ' g ' +str(strip[i].g) + ' b ' +str(strip[i].b) + ' w ' + str(strip[i].w) + '|')

  print("----------------------------")


# Creates a "virtual strip" for calculating the intensity level of each LEDs
def fillvstrip(LED_COUNT,STRIP,rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine):
# All LEDs in the strip are assigned the apropriate "fill" intensity level
    for i in range(LED_COUNT):
# Red diode
        STRIP[i].r =rfill;
# Green diode
        STRIP[i].g =gfill;
# Blue diode
        STRIP[i].b= bfill;
# White diode
        STRIP[i].w= wfill;
# Variables are set to one and are used as counters for increasing the LEDs properly
    rcount1,rcount2=1,1

    gcount1,gcount2=1,1

    bcount1,bcount2=1,1 

    wcount1,wcount2=1,1

# For every LED in the range of the fine level, alter the red diode if neccisary.
    for i in range(rfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
            # Increase brigness by one
           STRIP[i-rcount2].r = rfill+1
            # Increase counter
           rcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-rcount1+1].r = rfill+1 
            # Increase counter
            rcount1 +=1


# For every LED in the range of the fine level, alter the green diode if neccisary.
    for i in range(gfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
            # Increase brigness by one
            STRIP[i-gcount2].g = gfill+1
            # Increase counter
            gcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-gcount1+1].g = gfill+1 
            # Increase counter
            gcount1 +=1     


# For every LED in the range of the fine level, alter the blue diode if neccisary.
    for i in range(bfine):
    # If index is odd number, increase brightness of the matching number LED
       if i%2!=0:
           # Increase brigness by one
           STRIP[i-bcount2].b = bfill+1
            # Increase counter
           bcount2 +=1

       else:
           # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i+int((LED_COUNT/2))-bcount1+1].b = bfill+1 
            # Increase counter
            bcount1 +=1

# For every LED in the range of the fine level, alter the white diode if neccisary.
    for i in range(wfine):
        # if odd number index
        if i % 2 != 0:
            # Increase brigness by one
            STRIP[i - wcount2].w = wfill + 1
            # Increase counter
            wcount2 += 1

        else:
            # If the index is an even number, increase the of the LEDs starting from halfway down the strip.
            STRIP[i + int((LED_COUNT / 2)) - wcount1 + 1].w = wfill + 1
            # Increase counter
            wcount1 += 1



    return STRIP 


# Take the strip and virtual strip as parameters. prints virtual strip to real strip
def colorWipe3(strip, vstrip):


# For every LEDs
    for i in range(strip.numPixels()):
        # Variable holds color made from the values found in the virtual strip
        color=Color(vstrip[i].r,vstrip[i].g,vstrip[i].b,vstrip[i].w)
        # Set pixel color of real led to virtual led level
        strip.setPixelColor(i, color)
    # Execute changes
    strip.show()



       

def clear():



    command = 'clear'



    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls



        command = 'cls'



    os.system(command)



    clear()











# Funtion to match a search term to find a specific row
# Input is a csv file. It requires the term being searched for, and the title of the column you are searching in



def search(filename,term):


    # Open the csv that is passed as filename
    with open(filename, newline='') as csvfile:


        # Reader variable that can be parsed
        reader = csv.DictReader(csvfile)



        search=1  


        # Parsing through all rows in the reader
        for row in reader:


            # When the value is found in the column "datetime"  that matches the current Pi time
            if row['datetime'] == term:
                # Open the log
                file = open("/home/pi/Desktop/control_sun/log.txt", "a")
                # Print the data that is found in the csv
                file.write("found at "+str(term)+" "+str(row['crudered'])+str(row['rfine'])+str(row['crudegreen'])+str(row['gfine'])+str(row['crudeblue'])+str(row['bfine'])+str(row['crudewhite'])+str(row['wfine']))
                # Close log
                file.close()                                                         
                # Print the same to the terminal
                print("found at ",term," ",row['crudered'],row['rfine'],row['crudegreen'],row['gfine'],row['crudeblue'],row['bfine'],row['crudewhite'],row['wfine'])



                search=0


                # Returns the values found under their respective headers in the csv
                return (row['crudered'],row['rfine'],row['crudegreen'],row['gfine'],row['crudeblue'],row['bfine'],row['crudewhite'],row['wfine'])



  



    



# Main program logic follows:



if __name__ == '__main__':



    # Process arguments



    parser = argparse.ArgumentParser()



    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')



    args = parser.parse_args()







    # Create NeoPixel object with appropriate configuration.



    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)



    # Intialize the library (must be called once before other functions).



    strip.begin()


    # Initializing variables for future use
    rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine=0,0,0,0,0,0,0,0

    vstrip=[]



    # In range of number of lights assigned by LED_COUNT
    vstrip = [led(0,1,2,3) for i in range(LED_COUNT)]


    # Assign the variable vstrip by calling fillvstrip(). This initializes the strip and assigns all power levels the value of 0
    vstrip = fillvstrip(LED_COUNT,vstrip,rfill,rfine,gfill,gfine,bfill,bfine,wfill,wfine)



    try:
        # Clear log from last time the code was ran
        file = open("/home/pi/Desktop/control_sun/log.txt", "w")

        file.close()

        while True:


            # Get the real current time and assign appropriate variables for futute formatiing
            year,month,day,hour,minute,second=gettime()


            # This code will continue when the current time is a whole minute. This is because the data found in the csv is going to be at one-minute intervals
            if(second=="00"):

                # Creates a string which is formated the same as the "datetime" row in the csv
                searcht=str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
                # Hold values returned by search function
                result = search('/home/pi/Desktop/control_sun/LED_schedule_sun.csv', searcht)
                # If result is not null, a data was found
                if result:
                    # Assign it to its respective variable
                    rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine = result

                else:
                    # If null
                    print("No matching term was found in the CSV file")

                # Casecatching for if there is a matching datetime but no brightness values found at that time. This would occur when the moon is not above the horizion
                if (rfill == "#VALUE!"):

                    rfill = 1



                if (rfine == "#VALUE!"):

                    rfine = 1



                if (gfill == "#VALUE!"):

                    gfill = 1



                if (gfine == "#VALUE!"):

                    gfine = 1



                if (bfill == "#VALUE!"):

                    bfill = 1



                if (bfine == "#VALUE!"):

                    bfine = 1



                if (wfill == "#VALUE!"):

                    wfill = 1



                if (wfine == "#VALUE!"):

                    wfine = 1

                
                # Casting all values to int data type
                rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine = int(rfill), int(rfine), int(gfill), int(gfine), int(bfill), int(bfine), int(wfill), int(wfine)

                



                

        

                              
                # Fill the virtual strip with the values found in the csv
                vstrip = fillvstrip(LED_COUNT, vstrip, rfill, rfine, gfill, gfine, bfill, bfine, wfill, wfine)

              




                # Apply changes to real strip, making it match the data stored in the virtual strip
                colorWipe3(strip, vstrip)






                # Print what should be displaying on the light strip for the given number of LEDs 
                for i in range(3):  # Parameter is number of LEDs from virtual strip that are printed



                    printled(vstrip, i)



                time.sleep(52)  # Parameter is time in seconds the program will wait before checking the clock again



            

   

    except KeyboardInterrupt:



        if args.clear:



            colorWipe(strip, Color(0,0,0,0), 10)






```