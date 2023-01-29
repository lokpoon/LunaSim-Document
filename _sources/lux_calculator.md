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

# LunaSim: Lux calculator

**LunaSim-Lux calculator** is a R program that predicts ground illuminance (lux) of moonlight. A basic prediction of twilight and sunlight illuminance is also provided as an option.

It is intended for use for ecological studies where biologists requires moonlight illuminance as a model predictor.

## Key features

- Accurate prediction of moonlight illuminance at any geographic location and over any time period
- Offers basic prediction of twilight and sunlight illuminance as well
- Generates .csv table of illuminance over time
- Quickly plot illuminance over time

```{figure} /images/one_month.png
:name: one_month

Plot example of moonlight ground illuminance over a month in 2022 in Leticia, Colombia.
```

##  Packages required
- `library(suncalc)` Calculate astronomical variables given a time and location, including moon phase, moon altitude, sun altitude, the Moon and Earth distance
- `library(dplyr)` Data wrangling
- `library(lubridate)` Makes datetime format easier to work with
- `library(REdaS)` Convert between degree angle and radian
- `library(npreg)` Fit smoothing spline
- `library(ggplot2)` Create plots
- `library(beepr)` Makes a notification sound

##  Workflow
1. Set the time period and location.
2. Set the simulation time interval (i.e., the temporal resolution).
3. Save a lux_prediction.csv, containing the illuminance prediction over time.
4. Save a plot of the illuminance prediction over time.