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
(content:edit)=
# Edit <span style="font-variant:small-caps;">MoonSim</span> schedule

- One of the most powerful feature of _<span style="font-variant:small-caps;">MoonSim</span>_ is that the user can create any light scenario by editing the `LED_schedule_moon.csv` or `LED_schedule_sun.csv`.

- While _<span style="font-variant:small-caps;">MoonSim</span>_ is great for recreating realistic illuminance (by running the `LED_schedule_sun.csv` directly from _<span style="font-variant:small-caps;">MoonSim</span>: Schedulers_), we expect many experiments to require a manipulated (e.g. remove a full moon night from the lunar cycle) or a standardized (e.g. same sunrise/set time everyday).

## The sky is the limit

- To create a customized `LED_schedule .csv`, the user first generate a blue print `LED_schedule .csv` for your location and time duration, at 1 minute intervals.
- Then edit the LED values (crude and fine) in the `LED_schedule .csv`.
- Crude ranges 0-255 (LED intensity level).
- Fine ranges 0-the total number of LEDs in the array.
- Here are some examples of how you might want to edit your `LED_schedule .csv`:
- **IN PROGRESS**
## Problem with Excel datetime
- When opening a newly created `LED_schedule .csv` in R, or with a text editor (e.g. Notepad in Windows or TextEdit in Mac), the `datetime` column is presented in this correct format: 
    - `YYYY-MM-DD hh:mm:ss`

```{figure} /images/original_datetime.png
:name: original_datetime

The correct datetime format when opened with a text editor.
```

- As soon as the same `LED_schedule .csv` is opened in Excel, the datetime will automatically reformat to the Excel format. How the datetime is reformatted probably depends on the user's computer's country setting. If the user save the `LED_schedule .csv` now, datetime will be in a wrong format that _<span style="font-variant:small-caps;">MoonSim</span>_ does not recognize.

```{figure} /images/excel_datetime.png
:name: excel_datetime

The wrong datetime format as soon as `LED_schedule .csv` is opened in Excel. The order of year, month, and day is wrong, the number of digits are wrong, and the seconds is missing.
```

- To remedy this issue, the datetime format needs to be specified every time you are opening and saving `LED_schedule .csv` in Excel.
    1. Right click at the `datetime` **column B**, click **Format Cells...**:
        ![format_column.jpg](./images/format_column.jpg "format_column.jpg")
        <p>&nbsp;</p>
    
    2. Click **Custom**, and paste `YYYY-MM-DD hh:mm:ss` in **Type:**. Then **OK**.
        ![format_cells.jpg](./images/format_cells.jpg)
        <p>&nbsp;</p>
    
    3. Now the datetime is correct, and the `LED_schedule .csv` is ready for saving
        ![fixed_time.jpg](./images/fixed_time.jpg "fixed_time.jpg")
        <p>&nbsp;</p>
    
    5. This problem will reappear as soon as the user open the `LED_schedule .csv` again in Excel.