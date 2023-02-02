import pickle
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData

Fb = pickle.load(open('../DataFiles/Marvel.z0.pickle','rb'))
LMM = pickle.load(open('../DataFiles/MergerHistories.Marvel.pickle','rb'))
Nhalo = 0
for sim in ['cptmarvel','elektra','storm','rogue']:
    for h in LMM[sim]:
        Nhalo+=1

T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC = [np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo)]
for i in [T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC]:
    i[:] = np.NaN

i = 0
for sim in ['cptmarvel','elektra','storm','rogue']:
    for h in LMM[sim]:
        try:
            T[i] = LMM[sim][h]['times'][np.where(np.array(LMM[sim][h]['ratios'])<4)[0][0]]
        except:
            T[i] = np.NaN
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
        if T[i]>12: print(f'{sim}-{h}: {T[i]} , {FbE[i]}')
        i+=1

loc,typ = ['.Entire','.Inner','.Center'],['','.Observed','.Gas','.Stellar']
data = [[FbE,FbOE,FbGE,FbSE],[FbI,FbOI,FbGI,FbSI],[FbC,FbOC,FbGC,FbSC]]
time_bins = np.linspace(0,14,50)

for l in np.arange(len(loc)):
    for t in np.arange(len(typ)):
        d = data[l][t]
        mid = np.mean(d)
        lower = np.percentile(d,25)
        upper = np.percentile(d,75)
        Hi = T[d>upper]
        Low = T[d<lower]

        f,ax = plt.subplots(1,1,figsize=(8,6))
        ax.set_xlabel(r'T$_{LMM}$ [Gyr]',fontsize=15)
        ax.set_ylabel('N',fontsize=15)
        ax.set_xlim([0,14])
        ax.semilogy()
        ax.plot(0,0,color='navy',linewidth=2,label=r'High f$_b$')
        ax.plot(0,0,color='darkred',linewidth=2,label=r'Low f$_b$')
        ax.legend(loc='upper left',prop={'size':15})

        ax.hist(Hi,time_bins,histtype='step',color='navy',linewidth=3)
        ax.hist(Hi,time_bins,color='cornflowerblue',alpha=.7)
        ax.hist(Low,time_bins,histtype='step',color='darkred',linewidth=3)
        ax.hist(Low,time_bins,color='lightcoral',alpha=.7)

        f.savefig(f'../Plots/LMMDistribution{loc[l]}{typ[t]}.png',bbox_inches='tight',pad_inches=.1)
        meta = OSXMetaData(f'../Plots/LMMDistribution{loc[l]}{typ[t]}.png')
        meta.creator='LMMDistribution.Plot.py'
        plt.close()