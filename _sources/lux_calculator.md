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
# 1. <span style="font-variant:small-caps;">MoonShineR</span>: R package

_<span style="font-variant:small-caps;">MoonShineR</span>: R package_ predicts ground illuminance of moonlight in lux (lx). A prediction of twilight and sunlight illuminance is also included.

Install and load _<span style="font-variant:sRmall-caps;">MoonShineR</span>: R package_ by following instructions on https://github.com/Crampton-Lab/MoonShine.

(content:luxcalculator2)=
## Key features

- Provides an accurate prediction of moonlight illuminance at any geographic location and over any time period, at user-defined intervals.
- Provides a prediction of twilight and sunlight illuminance as well.
- Generates a `.csv` table of predicted illuminance over time.
- Provides a high-resolution plot of illuminance over time with simple customization.

    ```{note}
    The sunlight and twilight illuminance are predicted by the sun's altitude only, and are not intended to be highly accurate predictions of the absolute illuminance.
    ```
    ```{tip}
    This website [R Coder](https://r-coder.com/r-tutorials/r-basics/) is a good resource for learning basic R functions. Start here if you are completely new to R and need instructions on how to load R, set the working directory, install packages and run code.
    ```
    
## `predict_lux()`

- The first function in _<span style="font-variant:sRmall-caps;">MoonShineR</span>: R package_ is `predict_lux()`, which predicts natural ground illuminance over any defined geographical location and time period in a `data.frame` object.

- More information can be seen by entering `?MoonShineR::predict_lux` in R consle. Simply start with the example provided at the bottom of the R help page, which is also shown here:

    ```
    moonlight_output <- predict_lux(latitude = -4.21528, longitude = -69.94056, site_elev = 0,
                        time_zone = "EST", date_start = "2023-02-27", time_start = "18:00:00",
                        duration_day = 14, time_interval_minutes = 5, darksky_value = 0.0008,
                        output_directory = NULL, export_table = FALSE)
    ```

- This example creates a `data.frame` object named "moonlight_output", which is a prediction of the nighttime moonlight illuminance in Leticia, Colombia, for 14 days starting on 2023-02-27 at 6pm. The definitions of the columns within the `data.frame` is provided in the R help page, which is also shown here:

    ```{figure} /images/columns2.jpg
    :name: column

    Definition of the output `data.frame` columns.
    ```
    
    
- The console also print a message to inform the user if there are lunar eclipse events within the simulation.
- If there is no eclipse, a "no eclipse in simulation" message will appear in the R console after the simulation is complete.
- If there is an eclipse, “ECLIPSE IN SIMULATION!!!” will appear in the console. _<span style="font-variant:small-caps;">MoonShineR</span>_ will also report a list of all time intervals affected by both the penumbral and umbral stages of the eclipse ({numref}`eclipse`). Note that _<span style="font-variant:small-caps;">MoonShineR</span>_ does not simulate the transient reduction in illuminated fraction or moonlight illuminance during a lunar eclipse (these variables will therefore be incorrectly reported reported by _<span style="font-variant:small-caps;">MoonShineR</span>_ during the event). 
    ```{figure} /images/eclipse.jpg
    :name: eclipse

    Running a _<span style="font-variant:small-caps;">MoonShineR</span>_ simulation during an eclipse will return a warning message and a list of the minutes of the eclipse event.
    ```
- If the above example works, you can now change the arguments to your desire. See Arguments section in the R help page for detailed descriptions.

## `plot_lux()`

- The second function in _<span style="font-variant:sRmall-caps;">MoonShineR</span>: R package_ is `plot_lux()`, which takes the `data.frame` object created by `predict_lux()` to produce a clean looking plot.

- More information can be seen by entering `?MoonShineR::plot_lux` in R consle. Simply start with the example provided at the bottom of the R help page, which is also shown here:

    ```
    plot_lux(df = moonlight_output, illuminance_type_plot = "total_illuminance_all",
             plot_y_max = 0.3,  plot_dayttime_gray_mask = TRUE, plot_eclipse_red_mask = TRUE,
             plot_twilight = "astro", vertical_tiqme_label = TRUE, time_label_interval_hr = 24,
             time_labe_shift_hr = 0)
    ```

- This example took the `data.frame` object named "moonlight_output" we created from the previous section and creates a plot ({numref}`plot_lux`).
- If the above example works, you can now change the arguments to your desire. See Arguments section in the R help page for detailed descriptions.

    ```{figure} /images/plot_lux.jpeg
    :name: plot_lux

    Plot created in the example.
    ```
    
```{note}
If plot_eclipse_red_mask = TRUE, and there is an eclipse during the plotted simulation period, the eclipse period will be highlighted red to warn the user that those illuminances are overestimates. This is necessary because MoonShineR does not model the illuminance reduction during an eclipse.
```