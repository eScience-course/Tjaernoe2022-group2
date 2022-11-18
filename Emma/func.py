import xarray as xr
xr.set_options(display_style='html')
import intake
import cftime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from dask.distributed import Client
import pprint

def calculate_total_ozone(ds):
    O3_vmm = ds.o3
    O3_mmm = O3_vmm*(48.0/28.94)
    
    g=9.81
    P0 = ds.p0
    PS = ds.ps
    hyai = ds.a
    hybi = ds.b
    Plevi = hyai*P0+hybi*PS
    
    dp = np.empty(shape=O3_vmm.shape)
    
    dpa=xr.DataArray(dp,coords=ds.o3.coords,dims=ds.o3.dims)
    
    for i in range(1,Plevi.shape[0]):
        dpa[dict(lev=i-1)]=-(Plevi[i]-Plevi[i-1])
        
    O3_t=O3_mmm*dpa/g
    
    totO3=O3_t.sum(dim='lev')
    
    totO3DU = totO3/2.1415e-5
    print('Minimum column ozone value: {}'.format(totO3DU.min()))
    ds2=totO3DU.to_dataset(name='totO3')
    ds3=ds.merge(ds2)
    ds3.totO3.attrs['units']='DU'
    ds3.totO3.attrs['long_name']='Column ozone in Dobson Units'
    return ds3

def calculate_total_ozone_p(ds):
    O3_vmm = ds.o3
    O3_mmm = O3_vmm*(48.0/28.94)
    
    g=9.81
    Plevi = ds.plev
    
    dp = np.empty(shape=O3_vmm.shape)
    
    dpa=xr.DataArray(dp,coords=ds.o3.coords,dims=ds.o3.dims)
    
    for i in range(1,Plevi.shape[0]):
        dpa[dict(plev=i-1)]=-(Plevi[i]-Plevi[i-1])
        
    O3_t=O3_mmm*dpa/g
    
    totO3=O3_t.sum(dim='plev')
    
    totO3DU = totO3/2.1415e-5
    print('Minimum column ozone value: {}'.format(totO3DU.min()))
    ds2=totO3DU.to_dataset(name='totO3')
    ds3=ds.merge(ds2)
    ds3.totO3.attrs['units']='DU'
    ds3.totO3.attrs['long_name']='Column ozone in Dobson Units'
    return ds3

def computeWeightedMean(ds):
    # Compute weights based on the xarray you pass
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    # Compute weighted mean
    air_weighted = ds.weighted(weights)
    weighted_mean = air_weighted.mean(("lon", "lat"), keep_attrs=True)
    return weighted_mean