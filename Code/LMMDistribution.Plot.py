import argparse,pickle
import numpy as np
import matplotlib.pylab as plt
# from osxmetadata import OSXMetaData
import traceback

simualtions = ['Marvel','DCJL','Both']

LMM = None
for type in ['old','all','stellar_only','hybrid']:
    print(f'Analyzing {type} data')
    if type == 'old':
        Marvel = pickle.load(open('../DataFiles/MergerHistories.Marvel.pickle','rb'))
        for sim in Marvel.keys():
            print(f'{sim}: {len(Marvel[sim].keys())}')
        DCJL = pickle.load(open('../DataFiles/MergerHistories.DCJL.pickle','rb'))
        #LMM = {**Marvel, **DCJL}
        output_folder = '../Plots/LMM/old/'
    elif type == 'all':
        LMM = pickle.load(open('../DataFiles/major_mergers_all.pkl','rb'))
        for sim in Marvel.keys():
            print(f'{sim}: {len(LMM[sim].keys())}')
        output_folder = '../Plots/LMM/all/'
    elif type == 'stellar_only':
        LMM = pickle.load(open('../DataFiles/major_mergers_stellar_only.pkl','rb'))
        output_folder = '../Plots/LMM/stellar_only/'
    elif type == 'hybrid':
        LMM = pickle.load(open('../DataFiles/major_mergers_hybrid.pkl','rb'))
        output_folder = '../Plots/LMM/hybrid/'

    for simulation in simualtions:
        if simulation=='Marvel':
            if LMM == None: LMM = Marvel
            Fb = pickle.load(open('../DataFiles/Marvel.z0.pickle','rb'))
            sims = ['cptmarvel','elektra','storm','rogue']
        elif simulation=='DCJL':
            if LMM == None: LMM = DCJL
            Fb = pickle.load(open('../DataFiles/DCJL.z0.pickle','rb'))
            sims = ['h148','h229','h242','h329']
        elif simulation=='Both':
            if LMM == None: LMM = {**Marvel, **DCJL}
            Fb = {**pickle.load(open('../DataFiles/Marvel.z0.pickle','rb')),
                  **pickle.load(open('../DataFiles/DCJL.z0.pickle','rb'))}
            sims = ['cptmarvel','elektra','storm','rogue','h148','h229','h242','h329']

        Nhalo = 0
        # for sim in sims:
        #     for h in LMM[sim]:
        #         Nhalo+=1
        for sim in Fb:
            for h in Fb[sim]:
                Nhalo+=1
        print(f'Analyzing {Nhalo} halos')

        T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC = [np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                                      np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                                      np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                                      np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo)]
        for i in [T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC]:
            i[:] = np.nan

        i = 0
        for sim in Fb:
            for h in Fb[sim]:
                if str(h) not in LMM[sim].keys():
        # for sim in LMM:
        #     for h in LMM[sim]:
        #         if h not in Fb[sim].keys():
        #             continue
                    #print(f'{sim}-{h} not in LMM dictionary')
                    T[i] = np.nan
                else:
                    ratio = LMM[sim][h]['ratios']
                    threshold = 4
                    #print(f"\nDebug - Processing {sim}-{h}")
                    #print(f"Debug - Ratio array length:", len(ratio))
                    # if len(ratio) != 0:
                    #     print(f"Debug - Ratio range:", np.min(ratio), "to",
                    #           np.max(ratio))

                    mask = np.array(ratio) < threshold
                    # if np.sum(mask) != 0:
                    #     print(f"Debug - Number of ratios above threshold:",
                    #       np.sum(mask))

                    if np.where(mask)[0].size == 0:
                        #print(f"Debug - No ratios above threshold for {sim}-{h}")
                        T[i] = np.nan
                    else:
                        #if np.where(mask)[0].size > 1:
                            #print(f'major merger times: {np.array(LMM[sim][h]["times"])[mask]}')
                        T[i] = LMM[sim][h]['times'][np.where(mask)[0][0]]
                        #print(f"Debug - Found merger time:", T[i])

                #print(f'analyzing {sim}-{h}')
                halo = Fb[sim][h]
                FbE[i] = (halo['Mstar']+halo['Mgas'])/halo['Mvir']
                FbI[i] = (halo['.1Mstar']+halo['.1Mgas'])/halo['.1Mvir']
                FbC[i] = (halo['.01Mstar']+halo['.01Mgas'])/halo['.01Mvir']
                FbOE[i] = (.6*halo['Mstar']+1.33*halo['MHI'])/halo['Mvir']
                FbOI[i] = (.6*halo['.1Mstar']+1.33*halo['.1MHI'])/halo['.1Mvir']
                FbOC[i] = (.6*halo['.01Mstar']+1.33*halo['.01MHI'])/halo['.01Mvir']
                FbSE[i] = halo['Mstar']/halo['Mvir']
                FbSI[i] = halo['.1Mstar']/halo['.1Mvir']
                FbSC[i] = halo['.01Mstar']/halo['.01Mvir']
                FbGE[i] = (1.4*halo['MHI']+halo['MHII'])/halo['Mvir']
                FbGI[i] = (1.4*halo['.1MHI']+halo['.1MHII'])/halo['.1Mvir']
                FbGC[i] = (1.4*halo['.01MHI']+halo['.01MHII'])/halo['.01Mvir']
                #if T[i]>12: print(f'{sim}-{h}: {T[i]} , {FbE[i]:.2e}')
                i+=1
        #print(FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC)
        loc,typ = ['.Entire','.Inner','.Center'],['','.Observed','.Gas','.Stellar']
        data = [[FbE,FbOE,FbGE,FbSE],[FbI,FbOI,FbGI,FbSI],[FbC,FbOC,FbGC,FbSC]]
        time_bins = np.linspace(0,14,50)

        for l in np.arange(len(loc)):
            for t in np.arange(len(typ)):

                d = data[l][t]
                # zero_mask = d==0
                # mid = np.mean(d[~zero_mask])
                # lower = np.percentile(d[~zero_mask],25)
                # upper = np.percentile(d[~zero_mask],75)

                mid = np.nanmean(d)
                lower = np.nanpercentile(d,25)
                upper = np.nanpercentile(d,75)

                print(f'{simulation}{loc[l]}{typ[t]}:\t mean: {mid:.2e}, lower: ({lower:.2e}, upper:{upper:.2e})')
                Hi = T[d>upper]
                # Low = T[d < lower]
                Low = T[d<=lower]
                # T = T[~zero_mask]
                # Hi = T[d[~zero_mask]>upper]
                # Low = T[d[~zero_mask]<=lower]


                #
                #
                #
                #print when Hi or Low is entirely filled with nan
                Hi_nan_mask = np.isnan(Hi)
                Low_nan_mask = np.isnan(Low)
                if np.sum(Hi_nan_mask) == len(Hi):
                    print(f'All high {typ[t]} values are nan')
                if np.sum(Low_nan_mask) == len(Low):
                    print(f'All low {typ[t]} values are nan')
                    print(np.mean(d[d>upper][~Hi_nan_mask]))
                    #print(d[d_nan_mask])
                    break

                

                f,ax = plt.subplots(1,1,figsize=(8,6))
                ax.set_xlabel(r'T$_{LMM}$ [Gyr]',fontsize=15)
                ax.set_ylabel('N',fontsize=15)
                ax.set_xlim([0,14])
                ax.semilogy()
                ax.plot(0,0,color='navy',linewidth=2,label=r'High f$_b$')
                ax.plot(0,0,color='darkred',linewidth=2,label=r'Low f$_b$')
                ax.legend(loc='upper right',prop={'size':15})

                ax.hist(Hi,time_bins,histtype='step',color='navy',linewidth=3)
                ax.hist(Hi,time_bins,color='cornflowerblue',alpha=.7)
                ax.hist(Low,time_bins,histtype='step',color='darkred',linewidth=3)
                ax.hist(Low,time_bins,color='lightcoral',alpha=.7)
                save_path = output_folder+f'LMMDistribution.{simulation}{loc[l]}{typ[t]}.png'
                f.savefig(save_path,bbox_inches='tight',pad_inches=.1)
                # meta = OSXMetaData(f'../Plots/LMMDistribution.{args.simulation}{loc[l]}{typ[t]}.png')
                # meta.creator='LMMDistribution.Plot.py'
                plt.close()