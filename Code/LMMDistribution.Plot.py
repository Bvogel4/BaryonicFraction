import argparse,pickle
import numpy as np
import matplotlib.pylab as plt
#from osxmetadata import OSXMetaData

parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['Marvel','DCJL'],required=True)
args = parser.parse_args()

sims = ['cptmarvel','elektra','storm','rogue'] if args.simulation=='Marvel' else ['h148','h229','h242','h329']



Fb_marvel = pickle.load(open('../DataFiles/Marvel.z0.pickle','rb'))

Fb_dcjl = pickle.load(open('../DataFiles/DCJL.z0.pickle','rb'))

#combine the dictionaries
Fb = {**Fb_marvel,**Fb_dcjl}

LMM = pickle.load(open('../DataFiles/MergerHistories.Both.pickle','rb'))
sims = LMM.keys()
print(sims)

# convert halo numbers to strings
for sim in sims:
    LMM[sim] = {str(h): LMM[sim][h] for h in LMM[sim]}

Nhalo = 0
for sim in sims:
    for h in LMM[sim]:
        Nhalo+=1



T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC = [np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),
                                                              np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo),np.empty(Nhalo)]
for i in [T,FbE,FbI,FbC,FbOE,FbOI,FbOC,FbSE,FbSI,FbSC,FbGE,FbGI,FbGC]:
    i[:] = np.nan

i = 0
for sim in sims:
    for h in LMM[sim]:
        ratio = LMM[sim][h]['ratio']
        threshold = .1
        print(f"\nDebug - Processing {sim}-{h}")
        print(f"Debug - Ratio array length:", len(ratio))
        if len(ratio) != 0:
            print(f"Debug - Ratio range:", np.min(ratio), "to", np.max(ratio))

        mask = np.array(ratio) > threshold
        print(f"Debug - Number of ratios above threshold:", np.sum(mask))

        if np.where(mask)[0].size == 0:
            print(f"Debug - No ratios above threshold for {sim}-{h}")
            T[i] = np.nan
        else:
            T[i] = LMM[sim][h]['time'][np.where(mask)[0][0]]
            print(f"Debug - Found merger time:", T[i])
        #
        # ratio = LMM[sim][h]['ratios']
        # threshold = 4
        # print(f"\nDebug - Processing {sim}-{h}")
        # print(f"Debug - Ratio array length:", len(ratio))
        # if len(ratio) != 0:
        #     print(f"Debug - Ratio range:", np.min(ratio), "to", np.max(ratio))
        #
        # mask = np.array(ratio) < threshold
        # print(f"Debug - Number of ratios above threshold:", np.sum(mask))
        #
        # if np.where(mask)[0].size == 0:
        #     print(f"Debug - No ratios above threshold for {sim}-{h}")
        #     T[i] = np.nan
        # else:
        #     T[i] = LMM[sim][h]['times'][np.where(mask)[0][0]]
        #     print(f"Debug - Found merger time:", T[i])
        #make sure halo is in the Fb dictionary
        #make sure halo is in the Fb dictionary
        if str(h) not in Fb[sim].keys():
            print(f'{sim}-{h} not in Fb dictionary')
            i+=1
            continue
        print(f'analyzing {sim}-{h}')
        halo = Fb[sim][str(h)]
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
# Before creating histograms, add debugging for the arrays
print("\nDebug - Before histograms:")
print(f"Number of valid T values:", np.sum(~np.isnan(T)))
print(f"T range:", np.min(T[~np.isnan(T)]), "to", np.max(T[~np.isnan(T)]))

# Replace the histogram section with this safer version
for l in np.arange(len(loc)):
    for t in np.arange(len(typ)):
        d = data[l][t]
        print(f"\nDebug - Processing {loc[l]}{typ[t]}")
        valid_d = d[~np.isnan(d)]
        if len(valid_d) == 0:
            print("No valid data points, skipping this plot")
            continue

        mid = np.mean(valid_d)
        lower = np.percentile(valid_d, 25)
        upper = np.percentile(valid_d, 75)
        print(f"Debug - Percentiles: lower={lower}, upper={upper}")

        Hi = T[d > upper]
        Low = T[d < lower]
        Hi = Hi[~np.isnan(Hi)]  # Remove NaN values
        Low = Low[~np.isnan(Low)]  # Remove NaN values

        print(f"Debug - Number of high/low values:", len(Hi), len(Low))

        if len(Hi) == 0 and len(Low) == 0:
            print("No data for histograms, skipping plot")
            continue

        f, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.set_xlabel(r'T$_{LMM}$ [Gyr]', fontsize=15)
        ax.set_ylabel('N', fontsize=15)
        ax.set_xlim([0, 14])
        #ax.semilogy()

        if len(Hi) > 0:
            ax.hist(Hi, time_bins, histtype='step', color='navy', linewidth=3)
            ax.hist(Hi, time_bins, color='cornflowerblue', alpha=.7)
        if len(Low) > 0:
            ax.hist(Low, time_bins, histtype='step', color='darkred', linewidth=3)
            ax.hist(Low, time_bins, color='lightcoral', alpha=.7)

        ax.plot(0, 0, color='navy', linewidth=2, label=r'High f$_b$')
        ax.plot(0, 0, color='darkred', linewidth=2, label=r'Low f$_b$')
        ax.legend(loc='upper left', prop={'size': 15})
        f.savefig(f'../Plots/LMMDistribution{loc[l]}{typ[t]}.png',bbox_inches='tight',pad_inches=.1)
        # meta = OSXMetaData(f'../Plots/LMMDistribution.{args.simulation}{loc[l]}{typ[t]}.png')
        # meta.creator='LMMDistribution.Plot.py'
        plt.close()