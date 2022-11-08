import xarray as xr
import cftime
import matplotlib.pyplot as plt
import numpy as np
import pprint

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

def plot_year(waccm1,waccm2, cam1, cam2, eruption_name):
    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, figsize=(20,10))
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
    
    axs1.axvline(waccm1.year[5], color='k',linestyle='--',dashes=(5, 10))
    axs2.axvline(cam1.year[5], color='k',linestyle='--',dashes=(5, 10))
    
    axs1.set_ylabel(waccm1[0].long_name, fontsize=20)
    axs2.set_ylabel(cam1[0].long_name, fontsize=20)
    
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

def plot_month(waccm1,waccm2, cam1, cam2, eruption_name):
    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, figsize=(20,10))
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
    
    #axs1.axvline(waccm1.isel(time=[12*5]).time.values[0], color='k',linestyle='--',dashes=(5, 10))
    #axs2.axvline(cam1.isel(time=[12*5]).time.values[0], color='k',linestyle='--',dashes=(5, 10))
    
    axs1.set_ylabel(waccm1[0].long_name, fontsize=20)
    axs2.set_ylabel(cam1[0].long_name, fontsize=20)
    
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