#!/usr/bin/env python
# coding: utf-8

# # LunaSim-moonlight LED scheduler
# 
# LunaSim-moonlight LED scheduler is designed to be used in conjunction with the Lightbox system to recreate moonlight illuminance in the lab.
# 
# LunaSim-moonlight LED scheduler runs the same calculation as the lux calculator to predict moonlight illuminance. However the output is a .csv table of LED intensity values over time. This moon_output.csv contain LED values for each RGBW channels for every minute. The moon_output.csv serves as the schedule for the Lightbox python script to look up.
# 
# 
# ## Key features
# 
# - Recreate a realistic moonlight cycle in the lab
# - Option to simulate the obstruction of moonlight by surrounding obstructions (e.g., mountain ranges)
# - Option to simulate the dimming effects of moving cloud cover
# - Option to change the LED color spectrum to micmic color shift in habitats (e.g., blue shiftiness of ocean at depth), by controlling the intensity fraction of each RGBW channels
