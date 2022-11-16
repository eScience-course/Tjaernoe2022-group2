def n_forcing_plot(data,data2):
    #Before using this funktion the data and data2 has to be opened and one variable has to be selected.
    df = data.sel(time=slice(start_pina,end_pina))
    dg = data.sel(time=slice(start_krak,end_krak))
    
    north_p = computeWeightedMean(df.where(df['lat']>60.)).compute()
    south_p = computeWeightedMean(df.where(df['lat']<-60.)).compute()
    global_p = computeWeightedMean(df).compute()
    
    north_k = computeWeightedMean(dg.where(df['lat']>60.)).compute()
    south_k = computeWeightedMean(dg.where(df['lat']<-60.)).compute()
    global_k = computeWeightedMean(dg).compute()

    fig, (axs1, axs2) = plt.subplots(1, 2, constrained_layout=True, sharey=True, figsize=(7,7))
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
    axs2.set_ylabel('SO4 AOD at 550nm', fontsize=15)

    axs1.grid()
    axs1.tick_params(labelsize=15) 
    axs2.grid()
    axs2.tick_params(labelsize=15)
    
    axs1.set_title(" Mt. Pinatubo \n" , fontsize=15)
    axs2.set_title(" Krakatao \n" , fontsize=15)
    
    plt.legend(fontsize=15)
    
    