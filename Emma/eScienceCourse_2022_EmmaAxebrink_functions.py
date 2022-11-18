import xarray as xr
import cftime
import matplotlib.pyplot as plt
import numpy as np

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

def calc_yearly_anomaly(ds,end_prior_eruption):
    start = ds.time[0].values
    end_prior_eruption = cftime.DatetimeNoLeap(end_prior_eruption,1,15)
    ds_post_eruption = ds.squeeze().groupby('time.year').mean('time', keep_attrs=True)
    ds_climatology = ds.sel(time=slice(start,end_prior_eruption)).squeeze().groupby('time.year').mean('time', keep_attrs=True).mean('year', keep_attrs=True)
    ds_anomaly = ds_post_eruption - ds_climatology
    ds_anomaly.attrs = ds_climatology.attrs
    return ds_anomaly

def calc_monthly_anomaly(ds,end_prior_eruption):
    start = ds.time[0].values
    end_prior_eruption = cftime.DatetimeNoLeap(end_prior_eruption,1,15)
    ds_post_eruption = ds
    ds_climatology = ds.sel(time=slice(start,end_prior_eruption)).groupby('time.month').mean('time', keep_attrs=True)
    ds_anomaly = ds_post_eruption.groupby('time.month') - ds_climatology
    ds_anomaly.attrs = ds_climatology.attrs
    return ds_anomaly

def plot2_year(waccm1,waccm2, cam1, cam2, eruption_name):
    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, sharey=True, figsize=(20,10))
    #color = ['red','black','blue']
    color = ['green','darkviolet','darkorange']
    
    for i in range(3):
        j = i+1
        waccm1[i].plot(label="WACCM-"+ str(j), ax=axs1, linewidth=3, color=color[i])
        waccm2[i].plot(label='WACCM-'+ str(j), ax=axs2, linewidth=3, color=color[i])
    
    for i in range(3):
        j = i+1
        cam1[i].plot(label="CAM-"+ str(j), ax=axs1, linestyle='--', linewidth=3, color=color[i])
        cam2[i].plot(label="CAM-"+ str(j), ax=axs2, linestyle='--', linewidth=3, color=color[i])
    
    fig.suptitle(eruption_name, fontsize=30)
    
    axs1.set_xticks(waccm1.year)
    axs2.set_xticks(cam1.year)
    
    axs1.axvline(waccm1.year[5], color='k',linestyle='--',dashes=(5, 10))
    axs2.axvline(cam1.year[5], color='k',linestyle='--',dashes=(5, 10))
    
    axs1.set_ylabel(waccm1[0].long_name + '\n(' + cam1[0].units +')', fontsize=20)
    axs2.set_ylabel('', fontsize=20)
    
    axs1.set_xlabel('Year', fontsize=20)
    axs2.set_xlabel('Year', fontsize=20)
    
    axs1.tick_params(axis="x", labelsize=20)
    axs2.tick_params(axis="x", labelsize=20)
    
    axs1.tick_params(axis="y", labelsize=20)
    axs2.tick_params(axis="y", labelsize=20)
    
    axs1.set_title(" Northern Hemisphere \n" , fontsize=25)
    axs2.set_title(" Southern Hemisphere \n" , fontsize=25)
    
    plt.legend(fontsize=25)
    return 

def plot2_month(waccm1,waccm2, cam1, cam2, eruption_name):
    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, sharey=True, figsize=(20,10))
    #color = ['red','black','blue']
    color = ['green','darkviolet','darkorange']
    
    for i in range(3):
        j = i+1
        waccm1[i].plot(label="WACCM-"+ str(j), ax=axs1, linewidth=3, color=color[i])
        waccm2[i].plot(label='WACCM-'+ str(j), ax=axs2, linewidth=3, color=color[i])
        
    for i in range(3):
        j = i+1
        cam1[i].plot(label="CAM-"+ str(j), ax=axs1, linestyle='--', linewidth=3, color=color[i])
        cam2[i].plot(label="CAM-"+ str(j), ax=axs2, linestyle='--', linewidth=3, color=color[i])
    
    fig.suptitle(eruption_name, fontsize=30)
    test_tid = []
    for i in range(0,len(waccm1[0].time.values)):
        if waccm1[0].time.values[i].month==6 :
            test_tid.append(waccm1[0].time.values[i])
            
    axs1.set_xticks(test_tid)
    axs2.set_xticks(test_tid)
    axs1.tick_params(axis='x', labelrotation = 45)
    axs2.tick_params(axis='x', labelrotation = 45)
    
    axs1.axvline(waccm1.isel(time=[12*5]).time.values[0], color='k',linestyle='--',dashes=(5, 10))
    axs2.axvline(cam1.isel(time=[12*5]).time.values[0], color='k',linestyle='--',dashes=(5, 10))
    
    axs1.set_ylabel(waccm1[0].long_name + '\n(' + cam1[0].units +')', fontsize=20)
    axs2.set_ylabel('', fontsize=20)
    
    axs1.set_xlabel('Year', fontsize=20)
    axs2.set_xlabel('Year', fontsize=20)
    
    axs1.tick_params(axis="x", labelsize=20)
    axs2.tick_params(axis="x", labelsize=20)
    
    axs1.tick_params(axis="y", labelsize=20)
    axs2.tick_params(axis="y", labelsize=20)
    
    axs1.set_title(" Northern Hemisphere \n" , fontsize=25)
    axs2.set_title(" Southern Hemisphere \n" , fontsize=25)
    
    plt.legend(fontsize=25)
    return 

