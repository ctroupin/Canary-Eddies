import os
import glob
import datetime
#import xarray as xr
import netCDF4
#import cartopy.crs as ccrs
import matplotlib.pyplot as plt
#import cartopy.feature as cfeature
import cmocean
#coast = cfeature.GSHHSFeature(scale="f")

import py_eddy_tracker
from py_eddy_tracker.dataset.grid import RegularGridDataset
from py_eddy_tracker.tracking import Correspondances
from py_eddy_tracker.featured_tracking.area_tracker import AreaTracker
from py_eddy_tracker.gui import GUI

#mainproj = ccrs.Mercator(central_longitude=-60.0, min_latitude=-70.0, max_latitude=40.0)
#datacrs = ccrs.PlateCarree()

datadir = "/home/ctroupin/data/Altimetry/Canary/EddyTracking/"
outputdir = os.path.join(datadir, "tracking")
if not(os.path.exists(outputdir)):
    os.mkdir(outputdir)

datestart = datetime.datetime(1993, 1, 1)
dateend = datetime.datetime(1993, 12, 31)
ndays = 1 + (dateend - datestart).days
print(f"{ndays} days")


cyclonic_filelist = sorted(glob.glob(os.path.join(datadir, "*Cyclonic*nc")))
anticyclonic_filelist = sorted(glob.glob(os.path.join(datadir, "*Anticyclonic*nc")))

corr = Correspondances(datasets=cyclonic_filelist, virtual=3)
corr.track()
corr.prepare_merging()
cycl_eddies_default_tracker = corr.merge(raw_data=False)
cycl_eddies_default_tracker.virtual[:] = cycl_eddies_default_tracker.time == 0
cycl_eddies_default_tracker.filled_by_interpolation(cycl_eddies_default_tracker.virtual == 1)

corr = Correspondances(datasets=anticyclonic_filelist, virtual=3)
corr.track()
corr.prepare_merging()
anticycl_eddies_default_tracker = corr.merge(raw_data=False)
anticycl_eddies_default_tracker.virtual[:] = anticycl_eddies_default_tracker.time == 0
anticycl_eddies_default_tracker.filled_by_interpolation(anticycl_eddies_default_tracker.virtual == 1)