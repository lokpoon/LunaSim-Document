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

LunaSim-lux calculator is a standalone R program that predicts ground illuminance (lux) of moonlight. A basic prediction of twilight and sunlight illuminance is also provided as an option.

It is intended for use for ecological studies where biologists requires moonlight illuminance as a model predictor.

## Key features

- Accurate prediction of moonlight illuminance at any geographic location and over any time period
- Offers basic prediction of twilight and sunlight illuminance as well
- Generates .csv table of illuminance over time
- Quickly plot illuminance over time

:::{figure-md} markdown-fig
<img src="images/one_month.png" alt="one_month" class="bg-primary mb-1" width="1000px">

Plot example of moonlight ground illuminance over a month in 2022 in Leticia, Colombia.
:::