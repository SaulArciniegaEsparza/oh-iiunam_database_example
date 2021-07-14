# -*- coding: utf-8 -*-
"""
Example of How To Read the OH-IIUNAM database of precipitation at high-temporal resolution

This database has been converted to NetCDF and can be downloaded from: https://doi.org/10.5281/zenodo.5098275

Real-time data can be downloaded from: https://www.oh-iiunam.mx/



Example by:
    Saul Arciniega Esparza
    zaul.ae@gmail.com

Database:
    A spatio-temporal high-resolution precipitation dataset for Mexico City
    derived from optical disdrometers and weighting rain gauges
    
Authors:
    Adrián Pedrozo-Acuña, José Agustín Breña-Naranjo, Pamela Iskra Mejía-Estrada,
    Mauricio Osorio-González, Saúl Arciniega-Esparza, Jorge Blanco-Figueroa,
    Jorge Alberto Magos-Hernández, Juan Alejandro Sánchez-Peralta

Affiliations:
    Institute of Engineering, Universidad Nacional Autónoma de México
    Mexican Institute of Water Technology, Morelos, Mexico
"""

#%% Import libraries
import numpy as np
import pandas as pd
import xarray as xr

import matplotlib.pyplot as plt


#%% How to read a Disdrometer data file
# OH database has been converted to NetCDF, and can be readed by any library
# that works with such files. We highly recomended xarray for such purpose

## Read data
filename = r"~/DISDRO_IIUNAM.nc"  # inser the full filename
dataset = xr.open_dataset(filename)

## Show dataset info
print(dataset)

## Get name's variables
varnames = list(dataset.variables.keys())
print(varnames)

## Extract rain intensity as a Pandas' Serie
varname = "intensity"
data  = dataset[varname]  # extract data
serie = data.to_pandas()  # convert to pandas serie
prec = serie / 60         # conver to rain amount by minute

# plot 1 min intensity
fig, ax = plt.subplots(figsize=(7, 3.5))
data.plot(ax=ax, linewidth=0.8)
ax.grid(True)
ax.set_xlabel("")
fig.tight_layout()

## Plot data rainfall spectrum
date     = "2018-08-30 18:20"
spectrum = dataset["spectrum"].loc[date, :, :]
fig, ax = plt.subplots()
spectrum.plot(cmap="Spectral_r", ax=ax)
ax.set_xlim(0, 6)
ax.set_ylim(0, 10)
fig.tight_layout()

## Plot data rainfall spectrum for a date range
start_date = "2018-08-30 00:00"
end_date   = "2018-08-30 23:59"
spectrum = dataset["spectrum"].loc[start_date:end_date, :, :].sum(dim="time")
fig, ax = plt.subplots()
spectrum.plot(cmap="Spectral_r", ax=ax)
ax.set_xlim(0, 6)
ax.set_ylim(0, 10)
fig.tight_layout()

## Close dataset conection
dataset.close()


#%% How to read a Pluviometer data file
# the dada structure of Pluviometer and Disdrometers is similar
# the difference is the variables stored in each database

## Read data
filename = r"~/PLUVIO_PREPA2.nc"  # inser the full filename
dataset = xr.open_dataset(filename)

## Show dataset info
print(dataset)

## Get name's variables
varnames = list(dataset.variables.keys())
print(varnames)

## Extract rain intensity as a Pandas' Serie
varname = "intensity"
data  = dataset[varname]  # extract data
serie = data.to_pandas()  # convert to pandas serie

# ignore unreal intensity
mask        = serie > 400  # unreal intensity values over 400 mm/hr
serie[mask] = np.nan       # set unreal values as nan
prec        = serie / 60   # conver to rain amount by minute

# plot 1 min intensity
fig, ax = plt.subplots(figsize=(7, 3.5))
prec.plot(ax=ax, linewidth=0.8)
ax.grid(True)
ax.set_xlabel("")
ax.set_ylabel("Precipitation [mm]")
fig.tight_layout()

## Close dataset conection
dataset.close()


