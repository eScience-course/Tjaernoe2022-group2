"""This is a general purpose module containing routines
(a) that are used in multiple notebooks; or 
(b) that are complicated and would thus otherwise clutter notebook design.
"""

import re
import socket

def is_ncar_host():
    """Determine if host is an NCAR machine."""
    hostname = socket.getfqdn()
    
    return any([re.compile(ncar_host).search(hostname) 
                for ncar_host in ['cheyenne', 'casper', 'hobart']])


def calculate_general_mass_plev(da,ds,Mm,ulim,llim):
    """Function calculates the total mass/m2 of a gas between ulim and llim pressure levels.
    Parameters: da: xarray.DataArray containing gas molar (or volume) mixing ratio;
    ds: xarray.Dataset containing the other necessary parameters (hybrid coefficients, PS and P0);
    Mm: Molar mass of the gas in question; ulim: Upper pressure limit; llim: lower pressure limit.
    Call signature a = calculate_general_concentration(Cly,data,Mm,100,1)"""
    #gas_mmm = da*(MW/28.94)
   
    g = 9.81
    Na = 6.022e23
    P0 = ds.p0
    PS = ds.ps
    hyai = ds.a
    hybi = ds.b
    Plevi = hyai*p0+hybi*ps
    #print(Plevi)
   
    dp = np.empty(shape=da.shape)
   
    dpa = xr.DataArray(dp, coords=da.coords, dims=da.dims)
   
    for i in range(1,Plevi.ilev.shape[0]):
        dpa[dict(lev=i-1)] = Plevi[dict(ilev=i)]-Plevi[dict(ilev=i-1)]
     
    mass_of_air_in_box = dpa/g
    #print(mass_of_air_in_box)
    #no_of_air_moles_in_box = dpa/28.94
    no_of_air_moles_in_box = mass_of_air_in_box*1000/28.94
    no_of_air_molec_in_box = no_of_air_moles_in_box*Na
    tot_no_of_air_molec = no_of_air_molec_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    tot_no_of_air_moles = no_of_air_moles_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    tot_mass_of_column_times_area = (tot_no_of_air_moles*28.94/1000.)*4*np.pi*6.3781e6**2
    #print(tot_mass_of_column_times_area)
   
    no_of_gas_moles_in_box = da*no_of_air_moles_in_box
    tot_no_of_gas_moles = no_of_gas_moles_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    #tot_no_of_gas_moles = tot_no_of_gas_molec/Na
    #print(tot_no_of_gas_moles)
    tot_mass_of_gas = tot_no_of_gas_moles*Mm/1000.
    #general_concentration = tot_no_of_gas_molec/tot_no_of_air_molec
    return tot_mass_of_gas 

def calculate_general_mass(da,ds,Mm,ulim,llim):
    """Function calculates the total mass/m2 of a gas between ulim and llim pressure levels.
    Parameters: da: xarray.DataArray containing gas molar (or volume) mixing ratio;
    ds: xarray.Dataset containing the other necessary parameters (hybrid coefficients, PS and P0);
    Mm: Molar mass of the gas in question; ulim: Upper pressure limit; llim: lower pressure limit.
    Call signature a = calculate_general_concentration(Cly,data,Mm,100,1)"""
    #gas_mmm = da*(MW/28.94)
   
    g = 9.81
    Na = 6.022e23
    P0 = ds['p0']
    PS = ds['ps']
    hyai = ds['hyai']
    hybi = ds['hybi']
    Plevi = hyai*p0+hybi*ps
    #print(Plevi)
   
    dp = np.empty(shape=da.shape)
   
    dpa = xr.DataArray(dp, coords=da.coords, dims=da.dims)
   
    for i in range(1,Plevi.ilev.shape[0]):
        dpa[dict(lev=i-1)] = Plevi[dict(ilev=i)]-Plevi[dict(ilev=i-1)]
     
    mass_of_air_in_box = dpa/g
    #print(mass_of_air_in_box)
    #no_of_air_moles_in_box = dpa/28.94
    no_of_air_moles_in_box = mass_of_air_in_box*1000/28.94
    no_of_air_molec_in_box = no_of_air_moles_in_box*Na
    tot_no_of_air_molec = no_of_air_molec_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    tot_no_of_air_moles = no_of_air_moles_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    tot_mass_of_column_times_area = (tot_no_of_air_moles*28.94/1000.)*4*np.pi*6.3781e6**2
    #print(tot_mass_of_column_times_area)
   
    no_of_gas_moles_in_box = da*no_of_air_moles_in_box
    tot_no_of_gas_moles = no_of_gas_moles_in_box.sel(lev=slice(llim,ulim)).sum(dim='lev')
    #tot_no_of_gas_moles = tot_no_of_gas_molec/Na
    #print(tot_no_of_gas_moles)
    tot_mass_of_gas = tot_no_of_gas_moles*Mm/1000.
    #general_concentration = tot_no_of_gas_molec/tot_no_of_air_molec
    return tot_mass_of_gas 

def cal_O3_burden_raw(do):
    Mm = 48 # O3 molar mass g/mol
    ulim = 1000
    llim = 0
    A_e = 510.1e12 # area of earth m2
    tlen = do['o3'].time.shape[0]
    da = do['o3']
    ds = do[dict(time=slice(None,tlen))]
    do['O3_burden'] = calculate_general_mass(da, ds, Mm, ulim, llim)/2.1415e-5
    do['O3_burden'].attrs['units'] = 'DU'
    return do