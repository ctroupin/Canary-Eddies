#!/usr/bin/env python
# coding: utf-8

# # Seguimiento de remolinos

import os
import glob
import datetime
import netCDF4
import py_eddy_tracker
from py_eddy_tracker.dataset.grid import RegularGridDataset
from py_eddy_tracker.tracking import Correspondances
from py_eddy_tracker.featured_tracking.area_tracker import AreaTracker
from py_eddy_tracker.gui import GUI

#shareddir = "/home/jovyan/shared-readwrite/ohwe24_hackaton/"
datadir = "/home/ctroupin/data/Altimetry/Canary/"
outputdir = "/home/ctroupin/data/Altimetry/Canary/EddyTracking/"

if not(os.path.exists(outputdir)):
    os.mkdir(outputdir)

yearstart = 1994
yearend = 2024

# Loop on years (as there is one file per year to split the download)

for theyear in range(yearstart, yearend):
    
    # currentfile_alti = os.path.join(datadir, f"cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_adt-ugos-vgos_64.94W-40.06W_44.94S-30.06S_{theyear}-01-01-{theyear}-12-31.nc")
    currentfile_alti = os.path.join(datadir, f"cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.125deg_P1D_adt-ugos-vgos_19.94W-13.06W_25.06N-29.94N_{theyear}-01-01-{theyear}-12-31.nc")

    datestart = datetime.datetime(theyear, 1, 1)
    dateend = datetime.datetime(theyear, 12, 31)
    ndays = 1 + (dateend - datestart).days
    print(f"{ndays} días")

    for ii in range(0, ndays):
        h = RegularGridDataset(currentfile_alti, "longitude", "latitude", indexs={'time':ii})
        h.bessel_high_filter("adt", 500, order=3)
        thedate = datestart + datetime.timedelta(days=ii)
        
        a, c = h.eddy_identification(
            "adt",
            "ugos",
            "vgos",  # Variables used for identification
            thedate,  # Date of identification
            0.001,  # step between two isolines of detection (m)
            pixel_limit=(5, 500),  # Min and max pixel count for valid contour
            shape_error=55,  # Error max (%) between ratio of circle fit and contour
        )
        
        with netCDF4.Dataset(os.path.join(outputdir, thedate.strftime('Brasil-Malvinas_Anticyclonic_%Y%m%d%H%M%S.nc')), 'w') as nc:
            a.to_netcdf(nc)
        with netCDF4.Dataset(os.path.join(outputdir, thedate.strftime('Brasil-Malvinas_Cyclonic_%Y%m%d%H%M%S.nc')), 'w') as nc:
            c.to_netcdf(nc)
