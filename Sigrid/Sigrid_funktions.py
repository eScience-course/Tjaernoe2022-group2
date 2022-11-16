
import xarray as xr
xr.set_options(display_style='html')
import intake
import cftime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

start_pina = cftime.DatetimeNoLeap(1985,1,15)
end_prior_eruption_pina = cftime.DatetimeNoLeap(1991,1,15)
end_pina = cftime.DatetimeNoLeap(2000,1,15)



def computeWeightedMean(data):
    # Compute weights based on the xarray you use
    weights = np.cos(np.deg2rad(data.lat))
    weights.name = "weights"
    # Compute weighted mean
    air_weighted = data.weighted(weights)
    weighted_mean = air_weighted.mean(("lon", "lat"))
    return weighted_mean



def forcing_plot(data,data2):
    #Before using this funktion the data and data2 has to be opened and one variable has to be selected.
    #Pinatubo
    start_pina = cftime.DatetimeNoLeap(1985,1,15)
    end_prior_eruption_pina = cftime.DatetimeNoLeap(1991,1,15)
    end_pina = cftime.DatetimeNoLeap(2000,1,15)

    #Krakatao
    start_krak = cftime.DatetimeNoLeap(1876,1,15)
    end_prior_eruption_krak = cftime.DatetimeNoLeap(1882,1,15)
    end_krak = cftime.DatetimeNoLeap(1891,1,15)
    
    df = data.sel(time=slice(start_pina,end_pina))
    dg = data2.sel(time=slice(start_krak,end_krak))
    
    north_p = computeWeightedMean(df.where(df['lat']>60.)).compute()
    south_p = computeWeightedMean(df.where(df['lat']<-60.)).compute()
    global_p = computeWeightedMean(df).compute()
    
    north_k = computeWeightedMean(dg.where(dg['lat']>60.)).compute()
    south_k = computeWeightedMean(dg.where(dg['lat']<-60.)).compute()
    global_k = computeWeightedMean(dg).compute()

    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, sharey=True, figsize=(14,7))
    #Plotting
    north_p.plot(label='North >60N', ax=axs1)
    north_k.plot(label='North >60N', ax=axs2)

    south_p.plot(label="South >60S", ax=axs1)
    south_k.plot(label="South >60S", ax=axs2)

    global_p.plot(label="Global",ax=axs1)
    global_k.plot(label="Global",ax=axs2)
    
    #Making the figure look nice, adding titles.
    fig.suptitle('SO4 AOD', fontsize=15)
    
    axs1.set_xlabel('Time', fontsize=15)
    axs1.set_ylabel('SO4 AOD at 550nm', fontsize=15)
    
    axs2.set_xlabel('Time', fontsize=15)
    axs2.set_ylabel(' ', fontsize=15)

    axs1.grid()
    axs1.tick_params(labelsize=15) 
    axs2.grid()
    axs2.tick_params(labelsize=15)
    
    axs1.set_title(" Mt. Pinatubo \n" , fontsize=15)
    axs2.set_title(" Krakatao \n" , fontsize=15)
    
    plt.legend(fontsize=15)
    
    
def mean_plot_doub(data,data2,vulcano):
    #Funftion that calculates yearly avereged climatologies.
    #Reads in two datasets
    if vulcano==1:
        start = cftime.DatetimeNoLeap(1985,1,15)
        end_prior_eruption = cftime.DatetimeNoLeap(1991,1,15)
        end = cftime.DatetimeNoLeap(2000,1,15)
    if vulcano ==2:
        start = cftime.DatetimeNoLeap(1876,1,15)
        end_prior_eruption= cftime.DatetimeNoLeap(1882,1,15)
        end = cftime.DatetimeNoLeap(1891,1,15)

    #Selecting time period in datasets
    ds = data.sel(time=slice(start,end))
    ds2 = data2.sel(time=slice(start,end))
    
    #Claculating climatology, annual mean and anomaly
    climatology = ds.sel(time=slice(start, end_prior_eruption)).groupby('time.year').mean('time',keep_attrs=True).mean('year')
    annual_mean = ds.groupby('time.year').mean('time')
    anom=annual_mean-climatology
    
    climatology2 = ds2.sel(time=slice(start, end_prior_eruption)).groupby('time.year').mean('time',keep_attrs=True).mean('year')
    annual_mean2 = ds2.groupby('time.year').mean('time')
    anom2=annual_mean2-climatology2
    
    #Computing the weighted mean for different regions
    north_anomaly = computeWeightedMean(anom.where(anom['lat']>60.)).compute()
    south_anomaly = computeWeightedMean(anom.where(anom['lat']<-60.)).compute()
    global_anomaly= computeWeightedMean(anom).compute()
    
    north_anomaly2 = computeWeightedMean(anom2.where(anom2['lat']>60.)).compute()
    south_anomaly2 = computeWeightedMean(anom2.where(anom2['lat']<-60.)).compute()
    global_anomaly2= computeWeightedMean(anom2).compute()
    
    
    #Plotting
    fig, (axs1, axs2, axs3) = plt.subplots(1, 3, constrained_layout=True, sharey=True, figsize=(20,10))

    north_anomaly.plot(label="NorESM 14", ax=axs1)
    north_anomaly2.plot(label='NorESM 16', ax=axs1)
    
    south_anomaly.plot(label="NorESM 14", ax=axs2)
    south_anomaly2.plot(label='NorESM 16', ax=axs2)
    
    global_anomaly.plot(label="Ex. 14 (w/vulcanic)",ax=axs3)
    global_anomaly2.plot(label='Ex. 16 (no vulcanic)', ax=axs3)

    fig.suptitle('Yearly mean, Total Ozone column\n', fontsize=30)

    axs1.set_xlabel('Year',fontsize=20)
    axs2.set_xlabel('Year',fontsize=20)
    axs3.set_xlabel('Year',fontsize=20)
    #axs1.tick_params(fontsize=20)
    
    axs1.tick_params(labelsize=15) 
    axs2.tick_params(labelsize=15) 
    axs3.tick_params(labelsize=15)
    
    axs1.set_xlabel('Year', fontsize=20)
    axs1.set_ylabel('O3 [DU]', fontsize=20)
    
    axs2.set_xlabel('Year', fontsize=20)
    axs2.set_ylabel(' ', fontsize=20)
    
    axs3.set_xlabel('Year', fontsize=20)
    axs3.set_ylabel(' ', fontsize=20)

    axs1.grid()
    axs2.grid()
    axs3.grid()

    axs1.set_title(" North polar region >60N \n" , fontsize=20)
    axs2.set_title(" South polar region >60S \n" , fontsize=20)
    axs3.set_title('Global Mean \n', fontsize=20)
    plt.legend(fontsize=25)
    
def mean_plot_sing(data,vulcano):
    #Funftion that calculated weighted means, anomalies and plots it
    #Reads in only one dataset
    if vulcano==1:
        start = cftime.DatetimeNoLeap(1985,1,15)
        end_prior_eruption = cftime.DatetimeNoLeap(1991,1,15)
        end = cftime.DatetimeNoLeap(2000,1,15)
    if vulcano ==2:
        start = cftime.DatetimeNoLeap(1876,1,15)
        end_prior_eruption= cftime.DatetimeNoLeap(1882,1,15)
        end = cftime.DatetimeNoLeap(1891,1,15)

    #Selecting time period in datasets
    ds = data.sel(time=slice(start,end))
    
    #Claculating climatology, annual mean and anomaly
    climatology = ds.sel(time=slice(start, end_prior_eruption)).groupby('time.year').mean('time',keep_attrs=True).mean('year')
    annual_mean = ds.groupby('time.year').mean('time')
    anom=annual_mean-climatology
       
    #Computing the weighted mean for different regions
    north_anomaly = computeWeightedMean(anom.where(anom['lat']>60.)).compute()
    south_anomaly = computeWeightedMean(anom.where(anom['lat']<-60.)).compute()
    global_anomaly= computeWeightedMean(anom).compute()
    
    #Plotting
    fig, (axs1, axs2, axs3) = plt.subplots(1, 3, constrained_layout=True, figsize=(20,10), sharey=True )

    north_anomaly.plot(ax=axs1)
    
    south_anomaly.plot(ax=axs2)
    
    global_anomaly.plot(ax=axs3)

    fig.suptitle('Total Ozone column\n', fontsize=30)

    axs1.set_xlabel('Year',fontsize=20)
    axs2.set_xlabel('Year',fontsize=20)
    axs3.set_xlabel('Year',fontsize=20)
    #axs1.tick_params(fontsize=20)
    
    axs1.set_xlabel('Year', fontsize=20)
    axs1.set_ylabel('O3 [DU]', fontsize=20)
    
    axs2.set_xlabel('Year', fontsize=20)
    axs2.set_ylabel(' ', fontsize=20)
    
    axs3.set_xlabel('Year', fontsize=20)
    axs3.set_ylabel(' ', fontsize=20)
    
    axs1.grid()
    axs2.grid()
    axs3.grid()
    
    axs1.tick_params(labelsize=15) 
    axs2.tick_params(labelsize=15) 
    axs3.tick_params(labelsize=15)

    axs1.set_title(" Northern Hemisphere \n" , fontsize=20)
    axs2.set_title(" Southern Hemisphere \n" , fontsize=20)
    axs3.set_title('Global Mean \n', fontsize=20)

def north_multi_plot(data,yr,cs,title):
    proj_plot = ccrs.Orthographic(0, 90)

    p = data.sel(time = data.time.dt.year.isin([yr])).squeeze().plot(x='lon',y='lat',transform=ccrs.PlateCarree(),levels=np.linspace(-1.5e-6,1.5e-6,31),subplot_kws={"projection": proj_plot}, col='time', col_wrap=6, robust=True, cmap=cs)
    # We have to set the map's options on all four axes
    for ax,i in zip(p.axes.flat,  data.time.sel(time = data.time.dt.year.isin([yr])).values):
        ax.coastlines()
        ax.set_title(i.strftime("%B %Y"), fontsize=18)
        
    ax.text(-2.1, 2.60, title, fontsize=25, transform=ax.transAxes, ha='center')