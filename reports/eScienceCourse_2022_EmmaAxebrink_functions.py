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
    ds2 = []
    for i in ds.data_vars:
        weights = np.cos(np.deg2rad(ds.lat))
        weights.name = "weights"
        # Compute weighted mean
        air_weighted = ds[i].weighted(weights)
        weighted_mean = air_weighted.mean(("lon", "lat"), keep_attrs=True)
        ds2.append(weighted_mean)
    ds3 = xr.merge(ds2)
    return ds3

def calc_yearly_anomaly(ds,end_prior_eruption):
    ds2 = []
    end_prior_eruption = cftime.DatetimeNoLeap(end_prior_eruption,1,15)
    for i in ds.data_vars:
        start = ds[i].time[0].values
        ds_post_eruption = ds[i].squeeze().groupby('time.year').mean('time', keep_attrs=True)
        ds_climatology=ds[i].sel(time=slice(start,end_prior_eruption)).squeeze(). \
        groupby('time.year').mean('time',keep_attrs=True).mean('year',keep_attrs=True)
        ds_anomaly = ds_post_eruption - ds_climatology
        ds_anomaly.attrs = ds_climatology.attrs
        ds2.append(ds_anomaly)
    ds3 = xr.merge(ds2)
    return ds3

def calc_monthly_anomaly(ds,end_prior_eruption):
    ds2 = []
    end_prior_eruption = cftime.DatetimeNoLeap(end_prior_eruption,1,15)
    for i in ds.data_vars:
        start = ds[i].time[0].values
        ds_post_eruption = ds[i]
        ds_climatology = ds[i].sel(time=slice(start,end_prior_eruption)).groupby('time.month').mean('time', keep_attrs=True)
        ds_anomaly = ds_post_eruption.groupby('time.month') - ds_climatology
        ds_anomaly.attrs = ds_climatology.attrs
        ds2.append(ds_anomaly)
    ds3 = xr.merge(ds2)
    return ds3

def plot3_year(w1,w2,w3,c1,c2,c3,eruption_name):
    fig, (axs1, axs2, axs3) = plt.subplots(1, 3, constrained_layout=True, sharey=True, figsize=(30,10))
    color = ['green','darkviolet','darkorange']
    
    for i in range(3):
        j = i+1
        w1[i].plot(label='WACCM-'+ str(j), ax=axs1, linewidth=3, color=color[i])
        w2[i].plot(label='WACCM-'+ str(j), ax=axs2, linewidth=3, color=color[i])
        w3[i].plot(label='WACCM-'+ str(j), ax=axs3, linewidth=3, color=color[i])
        
    
    for i in range(3):
        j = i+1
        c1[i].plot(label='CAM-'+ str(j), ax=axs1, linestyle='--', linewidth=3, color=color[i])
        c2[i].plot(label='CAM-'+ str(j), ax=axs2, linestyle='--', linewidth=3, color=color[i])
        c3[i].plot(label="CAM-"+ str(j), ax=axs3, linestyle='--', linewidth=3, color=color[i])
    
    axs1.axvline(w1.year[5], color='k',linestyle='--',dashes=(5, 10))
    axs2.axvline(w1.year[5], color='k',linestyle='--',dashes=(5, 10))
    axs3.axvline(w1.year[5], color='k',linestyle='--',dashes=(5, 10))
    
    fig.suptitle('    Yearly mean ' + eruption_name, fontsize=40)
    
    axs1.set_xticks(w1.year)
    axs2.set_xticks(w1.year)
    axs3.set_xticks(w1.year)
    
    axs1.set_ylabel(w1[0].long_name + '\n(' + w1[0].units +')', fontsize=20)
    axs2.set_ylabel('', fontsize=20)
    axs3.set_ylabel('', fontsize=20)
    
    axs1.set_xlabel('Year', fontsize=20)
    axs2.set_xlabel('Year', fontsize=20)
    axs3.set_xlabel('Year', fontsize=20)
    
    axs1.tick_params(axis="x", labelsize=20)
    axs2.tick_params(axis="x", labelsize=20)
    axs3.tick_params(axis="x", labelsize=20)
    
    axs1.tick_params(axis="y", labelsize=20)
    axs2.tick_params(axis="y", labelsize=20)
    axs3.tick_params(axis="y", labelsize=20)
    
    axs1.set_title(" Arctic (60N–90N) \n" , fontsize=25)
    axs2.set_title("60S ~ 60N \n" , fontsize=25)
    axs3.set_title(" Antarctic (60S–90S) \n" , fontsize=25)
    
    axs1.legend(fontsize=20)
    return

def plot3_month_mean(w1,w2,w3, c1, c2, c3, eruption_name,erup):
    fig, (axs1, axs2, axs3) = plt.subplots(1, 3, constrained_layout=True, sharey=True, figsize=(30,10))
    color = ['green','darkviolet','darkorange']
    
    w1.plot(label="WACCM", ax=axs1, linewidth=3, color=color[1])
    w2.plot(label='WACCM', ax=axs2, linewidth=3, color=color[1])
    w3.plot(label='WACCM', ax=axs3, linewidth=3, color=color[1])
    
    c1.plot(label="CAM", ax=axs1, linestyle='--', linewidth=3, color=color[2])
    c2.plot(label="CAM", ax=axs2, linestyle='--', linewidth=3, color=color[2])
    c2.plot(label="CAM", ax=axs3, linestyle='--', linewidth=3, color=color[2])

    fig.suptitle('    Monthly mean ' + eruption_name, fontsize=30)
    time_erupt = []
    for i in range(0,len(w1.time.values)):
        if len(w1.time.values) < 50:
            if w1.time.values[i].month==2 or w1.time.values[i].month==6 or w1.time.values[i].month==10:
                time_erupt.append(w1.time.values[i])
        if len(w1.time.values) > 40:
            if w1.time.values[i].month==6 :
                time_erupt.append(w1.time.values[i])
            
    axs1.set_xticks(time_erupt)
    axs2.set_xticks(time_erupt)
    axs3.set_xticks(time_erupt)
    
    axs1.tick_params(axis='x', labelrotation = 45)
    axs2.tick_params(axis='x', labelrotation = 45)
    axs3.tick_params(axis='x', labelrotation = 45)
    
    stop = cftime.DatetimeNoLeap(erup,6,15)
    axs1.axvline(stop, color='k',linestyle='--',dashes=(5, 10))
    axs2.axvline(stop, color='k',linestyle='--',dashes=(5, 10))
    axs3.axvline(stop, color='k',linestyle='--',dashes=(5, 10))
    
    axs1.set_ylabel(w1.long_name + '\n(' + w1.units +')', fontsize=20)
    axs2.set_ylabel('', fontsize=20)
    axs3.set_ylabel('', fontsize=20)
    
    axs1.set_xlabel('Time', fontsize=20)
    axs2.set_xlabel('Time', fontsize=20)
    axs3.set_xlabel('Time', fontsize=20)
    
    axs1.tick_params(axis="x", labelsize=20)
    axs2.tick_params(axis="x", labelsize=20)
    axs3.tick_params(axis="x", labelsize=20)
    
    axs1.tick_params(axis="y", labelsize=20)
    axs2.tick_params(axis="y", labelsize=20)
    axs3.tick_params(axis="y", labelsize=20)
    
    axs1.set_title(" Arctic (60N–90N) \n" , fontsize=25)
    axs2.set_title("60S ~ 60N \n" , fontsize=25)
    axs3.set_title(" Antarctic (60S–90S) \n" , fontsize=25)
    
    axs1.legend(fontsize=20)
    return


