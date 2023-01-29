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

# LS-lightbox: Hardware setup

## Materials

| Item  | SKU/model number | Company  | Quantity required | Price | Link   | Note |
|-------|------------------|----------|-------------------|-------|--------|------|
| Raspberry Pi 4 model B kit | XXX | GeeekPi | 1 | $200 | [Amazon](https://www.amazon.com/GeeekPi-Raspberry-2GB-Starter-Kit/dp/B0B7DFF7TY/ref=sr_1_5?crid=1BQNGTSE4SSDJ&keywords=raspberry+pi+4+kit&qid=1674623289&sprefix=raspberry+pi+4+kit%2Caps%2C121&sr=8-5&ufe=app_do%3Aamzn1.fos.f5122f16-c3e8-4386-bf32-63e904010ad0) | [^1] |
| RTC module (DS3231) | 3-01-1198 | HiLetgo | 1 | $ | [Amazon](https://www.amazon.com/HiLetgo-DS3231-Precision-Arduino-Raspberry/dp/B01N1LZSK3/ref=sr_1_2?crid=33U6N5U6HSRWK&keywords=rtc+ds+3231&qid=1674685955&sprefix=rtc+ds+3231%2Caps%2C72&sr=8-2) | - |
| Generic ouse and keyboard | - | - | 1 | ~40 | - | - |
| Generic HDMI monitor | - | - | 1 | ~$100 | - | - |
| SK6812 RGBW LED strip | SK68121M144-RGBWWW65 | BTF-Lighting | At least 2 | $35 | [Amazon](https://www.amazon.com/BTF-LIGHTING-Individually-Addressable-Flexible-Waterproof/dp/B01N2PCIB9/ref=sr_1_6?crid=3OWYKHJC7QV57&keywords=sk6812%2Bwarm&qid=1674596692&sprefix=sk6812%2Bwarm%2Caps%2C104&sr=8-6&th=1) | [^2] |
| 2.54mm pitch crimp connector kit | XXX | OCR | 1 | $12 |[ Amazon ](https://www.amazon.com/OCR-Connector-Housing-Assortment-640Pcs-Set/dp/B071JLCFT6/ref=sr_1_15?crid=1RCAOTD9CWZTD&keywords=gpio+connector+kit&qid=1674669821&sprefix=gpio+connector+kit%2Caps%2C91&sr=8-15)| - |
| 3 Pin JST SM connector cable (pack of 2m x 4) | HL-LED79 | Hualand | At least 1 | $12 |[ Amazon ](https://www.amazon.com/Connector-WS2812B-Symphony-connectors%EF%BC%8CSM3P-controller/dp/B07G6PRDBQ/ref=sr_1_11?keywords=jst+3+pin+connector&qid=1674670291&sprefix=JST+3+pin+conn%2Caps%2C105&sr=8-11)| [^3] |
| 3 conductor wire 100ft | AT-3P-100FT | AOTOINK | 1 | $16 | [Amazon](https://www.amazon.com/AOTOINK-Extension-Electrical-Stranded-Lighting/dp/B08JTZKN4M/?crid=2MQUPBVHO898U&sprefix=3+core+wir,aps,104) | - |
| 5V10A DC power adapter | P5V10A | BTF-Lighting | One per LED strip | $22 |[ Amazon ](https://www.amazon.com/BTF-LIGHTING-Plastic-Adapter-Transformer-WS2812B/dp/B01D8FM71S?ref_=ast_sto_dp&th=1)| - |
| Lumber boards | - | Home Depot | One set per LED strip | $17 | - | [^4] |
| Generic black spray paint | - | - | 1 | $6 | - | - |
| Neutral Density (ND) filter sheets | - | Lee Filters | Depends | ~$20 per diffusion box | [BarnDoor](https://www.filmandvideolighting.com/lee-neutral-denisty-nd-gel-filter-sheet-film-video-photo-lighting.html) | [^5] |
| Lux meter/radiometer/spectrometer | - | - | 1 | $200 to >5000 | - | [^6] |
| UPS backup battery power | BE425M | APC | 1 | $60 | [Amazon](https://www.amazon.com/APC-Battery-Protector-Back-UPS-BE425M/dp/B01HDC236Q/ref=sr_1_7?keywords=uninterruptible%2Bpower%2Bsupply&qid=1674685859&sprefix=uninter%2Caps%2C105&sr=8-7&ufe=app_do%3Aamzn1.fos.006c50ae-5d4c-4777-9bc0-4513d670b6bc&th=1) | - |
|  |  |  |  | $ |  |  |
|  |  |  |  | $ |  |  |
```{note}
Estimated total cost for one LS-lightbox system (excluding the illuminance measuring device) = $653 (Jan 2023)
```

### Tools
- Soldering iron
- Wire stripper (for small gauge wire ~22-26 AWG)
- Needle pliers
- Wood hand saw
- Driver
- Heat gun (or just a lighter for contracting heat shrink)

### Basic supplies
- Solder
- Small heat shrinks
- Wood screws
- Masking tape
- Foam pieces

[^1]: Equivalent kit of the Raspberry Pi 4 model B from any company would work. Beside the Pi itself, the kit should include all the accessories such as cable, power supply, case, SD card, etc. You only need the 2GB RAM option, but you can opt for more RAM (4GB or 8GB) if budget allows.

You only need one Pi for moonlight recreation or sunlight and twilight recreation. You can use two Pi in conjunction to recreate both.

[^2]: We recommend the following options: 1m, 144 LED, Warm White. There is also the option of IP65 water resistant and IP30 normal version, choose the one more suitable for your application. Choose warm white because we do not want the big blue spike in the white channel spectrum. You can pick a different length and LED number as needed, but we believe 1m 144 LED is the best suited for most situations.

You need two LED strips to start. You can add more in multiple of two to daisy chain a lot more strips, e.g., when trying to recreate more closely to sunlight illuminance.

[^3]: Buy enough connector cable so that you can daisy chain LED strips across the room.

[^4]: These are the lumber board dimensions for building one diffusion box:
- Base: One of 5/4" x 6" x 4' [home depot](https://www.homedepot.com/p/WeatherShield-5-4-in-x-6-in-x-4-ft-Premium-Ground-Contact-Pressure-Treated-Decking-Board-253944/300526781) ($6)
- Two Sides: Two of 1" x 4" x 4' [home depot](https://www.homedepot.com/p/WeatherShield-1-in-x-4-in-x-4-ft-Appearance-Grade-Pressure-Treated-Board-275086/300573653) ($7.4)
- End caps: Cut down a 1" x 4" x 4' [home depot](https://www.homedepot.com/p/WeatherShield-1-in-x-4-in-x-4-ft-Appearance-Grade-Pressure-Treated-Board-275086/300573653) ($3.7)

[^5]: The ND filter you will need depends on your starting (no filter) illuminance. You'll likely need two or three filters per diffusion box. See {ref}`content:lightbox:calibration`.

Lee ND filter sheet lineup:
- Lee 298 (ND 0.15, ½ Stop) = Transmission 69.3%
- Lee 209 (ND 0.3, 1 Stop) = Transmission 51.2%
- Lee 210 (ND 0.6, 2 Stop) = Transmission 23.5%
- Lee 211 (ND 0.9, 3 Stop) = Transmission 13.7%
- Lee 299 (ND 1.2, 4 Stop) = Transmission 6.6%

Rosco is another company that makes ND filter sheets.

[^6]: "Lux meter" is just a commercial term for radiometer, both measure illuminance in lx. We need to measure the illuminance of the LED for calibrating it. Spectrometer is like an upgraded radiometer. It measures spectral irradiance, giving you spectral information about the light. And spectral irradiance measurements can be easily converted into illuminance. Spectrometer is generally high cost.

An accurate illuminance measuring device is critical for calibrating LS-lightbox, but a good one designed for low light is expensive. We do not want the cost of a good radiometer to discourage the use of LS-lightbox for moonlight experiments. Still, you should certainly get a meter that has NIST-Traceable calibration, like this [ILT10C](https://www.intl-lighttech.com/products/ilt10c-luxlight-meter-nist-traceable-calibration?gclid=Cj0KCQiAw8OeBhCeARIsAGxWtUzB0YaQDpYF5fXMYee-U9zSQgnbmph4LrlmD0inkbSdw4FtaJ-AjjsaApwYEALw_wcB). Lower cost meters can not measure at moonlight illuminance level (i.e., >0.3lux), still we can calibrate the LS-lightbox. Please see further explanations and solutions in the "LS-lightbox calibration" section.

For us, we use the International Light Technology [ILT-5000](https://www.intl-lighttech.com/products/ilt5000-researchlab-radiometer) radiometer, with a SUD100/U detector equipped with Y4 photopic filter (total ~$4000).


## Assemble Pi and LED strips
```{figure} /images/raspberry-pi.png
:name: schematic

Connection diagram for the Pi and LED strips. Wire colors according to SK6812 made by BTF-Lighting, Guangdong, China.  
```
```{figure} /images/cable.png
:name: cable

Photo of the actual connection. Click the figure to zoom in.
```

1. Follow the Raspberry Pi kit assembly instruction.
2. Decide how much wire length you need between the Pi and the first LED strip, and cut the 3 conductor wire accordingly.
3. On one end of the 3 conductor wire, put on a female crimp connector with 6 slots. See [this guide](https://www.youtube.com/watch?v=JsoqBS1-k7M) for installing crimp pins with needle nose pliers.
    - Follow {numref}`schematic` orientation and color scheme:
        - Red in the first slot
        - White in the third slot
        - Green in the sixth slot
4. Plug in the female crimp connector so that the wires are fed into the correct GPIO.
    - Follow {numref}`schematic` So that when Pi is oriented so that the GPIO are facing up and on the right side,the crimp connected is plugged into the upper right corner of the GPIO array.
        - Red wire goes into the 5V PIN.
        - White wire goes into the ground PIN.
        - Green wire goes into the GPIO 18 data PIN.
5. On the other end of the 3 conductor wire, solder on and heat shrink the 3-pin cable female connector (comes with the LED strip).
6. Connect the female connector to the LED strip male connector.
7. Install the power female connector (comes with the DC power supply) to the voltage-adding wires (loose red and white).
8. Plug in DC power supply.
9. Connector to additional LED strips by daisy chaining from the other end of the first LED strip. Add additional DC power supply on subsequent LED strips.
10. Install the RTC module as shown in {numref}`schematic` & {numref}`cable`, so that it is on the same end of the crimp connector and next to it. 

## Construction of diffusion box
```{figure} /images/diffusion_box.png
:name: box

Construction of a diffusion box housing one LED strip.
```
1. Construct the wooden box as {numref}`box` with screws. With:
    - 5/4" x 6" x 4' board as the base.
    - A 1" x 4" x 4' board on each long side.
    - Cut down a 1" x 4" x 4' to get two end caps.
2. Spray paint the interior in black.
3. Place the LED strip in the center and glue it on. The bottom of the LED strip should already have sticky tape.
4. Drill a small hole on each end of the box for the cables. Plug it with small pieces of foam to prevent light leak.
5. Cut ND filter sheets into the correct size, and secure them on the top opening with masking tape. Ensure no light leak. See {ref}`content:lightbox:calibration` regarding how many ND filter sheets to use.