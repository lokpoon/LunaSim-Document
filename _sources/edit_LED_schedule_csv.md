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

- While _<span style="font-variant:small-caps;">MoonSim</span>_ is optimized for recreating realistic illuminance (by running the `LED_schedule_moon.csv` or `LED_schedule_sun.csv` directly from _<span style="font-variant:small-caps;">MoonSim</span>: Schedulers_), we expect many experiments to require a manipulated light regime (e.g., remove a full moon night from the lunar cycle) or a standardized regime (e.g. same sunrise/set times everyday).

## Creating customized schedules

- To create a customized `LED_schedule .csv`, the user can either modify an existing _<span style="font-variant:small-caps;">MoonSim</span>_ generated `LED_schedule .csv` with Excel, or create it manually using the provided `manual_scheduler.xlsx` Excel spreadsheet template. The user can also combine both approaches to a create a customized `LED_schedule .csv`, as both methods are better suited for different scenarios.

- MoonShine can run any `LED_schedule .csv` when the following conditions are met:
    - A .csv file with the nine required columns (extra columns with other headers will be ignored):
        - `datetime` in "YYYY-MM-DD hh:mm:ss" format (make sure that the schedule starts before the intended launch time)
        - The eight RGBW LED values: `crudewhite`, `wfine`, `crudered`, `rfine`, `crudegreen`, `gfine`, `crudeblue`, `bfine`
            - Crude intensity ranges from 0-255 (LED intensity level).
            - Fine intensity ranges from 0 to the total number of LEDs in the array.
        - A correct file name `LED_schedule_moon.csv` or `LED_schedule_sun.csv`

### Option 1: Modify an existing `LED_schedule .csv`
- This method is suited for simple modifications such as setting a period of darkness, or repeating certain part of the existing schedule.
- To create a novel light regime, see Option 2.

#### Steps
1. Generate a “blueprint” LED_schedule .csv for a chosen location and time period, with 1 minute intervals.
2. Then edit the LED values (crude and fine) in the `LED_schedule .csv` with Excel.
3. Here are some examples of how you might want to edit your `LED_schedule .csv`:

**Turning off light for certain period**
```{figure} /images/zero.png
:name: zero

A dark period can be inserted simply by replacing the LED values by zero.
```

**Copy and pasting the LED intensity**
```{figure} /images/copy.jpg
:name: copy

Copy and pasting the LED intensity from one row to other rows at differnt times. As an example, the user can copy an entire night of LED intensity progression during a full moon and paste it in another night.
```
(content:datetime)=
#### Problem with Excel datetime
- When opening a newly created `LED_schedule .csv` in R, or with a text editor (e.g. Notepad/Notepad++ in Windows or TextEdit in Mac), the `datetime` column is presented in this correct format: 
    - `YYYY-MM-DD hh:mm:ss`

```{figure} /images/original_datetime.png
:name: original_datetime

The correct datetime format when opened with a text editor.
```

- If the same `LED_schedule .csv` is opened in Excel, the datetime will automatically reformat to the Excel format. How the datetime is reformatted probably depends on the user's computer's country setting. If the user then saves the `LED_schedule .csv` in Excel, the datetime will be saved in an erroneous format that _<span style="font-variant:small-caps;">MoonSim</span>_ does not recognize.

```{figure} /images/excel_datetime.png
:name: excel_datetime

The wrong datetime format is displayed when `LED_schedule .csv` is opened in Excel. The order of year, month, and day is incorrect, the number of digits is incorrect, and the seconds are missing.
```

- To remedy this problem, the datetime format needs to be specified every time the user opens and then saves LED_schedule .csv in Excel.
    1. Right click at the `datetime` **column B**, and click **Format Cells...**:
        ![format_column.jpg](./images/format_column.jpg "format_column.jpg")
        <p>&nbsp;</p>
    
    2. Click **Custom**, and paste `YYYY-MM-DD hh:mm:ss` in **Type:**. Then click **OK**.
        ![format_cells.jpg](./images/format_cells.jpg)
        <p>&nbsp;</p>
    
    3. Now the datetime is correct, and the `LED_schedule .csv` is ready for saving
        ![fixed_time.jpg](./images/fixed_time.jpg "fixed_time.jpg")
        <p>&nbsp;</p>
    
    5. This problem will reappear if user opens the `LED_schedule .csv` again in Excel.

(content:excel_scheduler)=
### Option 2: Create LED schedule manually using `manual_scheduler.xlsx` 

- This method is suited for the requirement of a fully customized LED schedule. The `manual_scheduler.xlsx` functions as template to convert a list of desired illuminance into LED intensity values. The user can recreate any novel illuminance schedule as desired.

#### Steps
```{figure} /images/manualexcel.jpg
:name: manualexcel

The layout of `manual_scheduler.xlsx`. Datetime (red box), desired illuminance (orange box), RGBW LED intensity values (green), LED settings (blue), and preview plot (purple). Currently the desired illuminance list is a linear function, increasing 0.5 lx every minute until it reaches 200 lx in 6 hours and 40 minutes.
```

1. Set the LED settings in the upper panel. The theoretical_max is the calibration illuminance, see {ref}`content:lightbox:calibration`. Different values depending on whether recreating moonlight or sunlight/twilight.
2. Create your list of datetime. It must be at 1 minute intervals.
3. Create your list of desired illuminance in lux.
4. The RGBW intensity values (crude and fine) will be updated automatically.
5. Save this .xlsx file first. Since this will preserve the formatting.
6. Then save this file as a .csv
7. Rename this .csv file as "LED_schedule_moon.csv" or "LED_schedule_sun.csv" depending on what the user is recreating.
8. Open the .csv and correct the datetime into the correct format for MoonShine. See our online manual chapter "Edit MoonShine schedule".
9. Remove the  unnecessary columns (i.e., column L and beyond).
10. Save the .csv file
11. The user can run this .csv with _<span style="font-variant:small-caps;">MoonSim</span>_, or append it to an existing `LED_schedule .csv` by matching the corresponding columns.

```{figure} /images/manualexp.jpg
:name: manualexp

A second example of a manual schedule. The desired illuminance list consists of a natural exponent function at the start and end of the sequence, and a plateau of illuminance in the center. The LED intensity values calculate automatically based on the desired illuminance list, which MoonShine would convert into accurate illumination in the room.
```