import argparse,imageio,os,pickle
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData

parser = argparse.ArgumentParser()
parser.add_argument("-o","--observed",action='store_true')
args = parser.parse_args()

pre = 'Observed' if args.observed else ''
xlower=1e-11 if args.observed else 1e-7
tlower=7e-4 if args.observed else 1e-2

mint = [1.29,1.94,2.2,2.5,3,3.8,4,4.4,4.7,5,5.17,5.5,6.05,6.4,6.7,7.2,7.7,8,8.3,
        8.6,9,9.4,9.8,10,10.6,10.8,11,11.5,11.9,12.1,12.4,12.8,13.3,13.7]
maxt = [1.3,2.16,2.3,2.6,3.3,3.9,4.3,4.6,4.9,5.16,5.5,5.8,6.2,6.5,6.9,7.5,7.8,8.2,8.6,
        8.9,9.1,9.7,10,10.4,10.8,11,11.3,11.6,12.1,12.3,12.6,12.9,13.6,13.8]
Data = pickle.load(open('../DataFiles/BaryonicFractionData.pickle','rb'))
Plots = {'times':[],'dark':[],'luminous':[],'dark_Inner':[],'luminous_Inner':[]}

sims,times = [['cptmarvel','elektra','storm','rogue'],[]]
for i in np.arange(len(mint)):
    Plots['times'].append((mint[i]+maxt[i])/2)
    Plots['dark'].append([])
    Plots['luminous'].append([])
    Plots['dark_Inner'].append([])
    Plots['luminous_Inner'].append([])
    for sim in sims:
        for t in Data[sim]:
            if mint[i]<Data[sim][t]['time']<maxt[i]:
                for h in Data[sim][t]['halos']:
                    halo = Data[sim][t]['halos'][h]
                    if args.observed:
                        if halo['Mstar'] == 0:
                            Plots['dark'][-1].append((.6*halo['Mstar']+1.33*halo['MHI'])/halo['Mvir'])
                            Plots['dark_Inner'][-1].append(float((.6*halo['Mstar_Inner']+1.33*halo['MHI_Inner'])/halo['Mvir_Inner']))
                        else:
                            Plots['luminous'][-1].append((.6*halo['Mstar']+1.33*halo['MHI'])/halo['Mvir'])
                            Plots['luminous_Inner'][-1].append(float((.6*halo['Mstar_Inner']+1.33*halo['MHI_Inner'])/halo['Mvir_Inner']))
                    else:
                        if halo['Mstar'] == 0:
                            Plots['dark'][-1].append((halo['Mstar']+halo['Mgas'])/halo['Mvir'])
                            Plots['dark_Inner'][-1].append(float((halo['Mstar_Inner']+halo['Mgas_Inner'])/halo['Mvir_Inner']))
                        else:
                            Plots['luminous'][-1].append((halo['Mstar']+halo['Mgas'])/halo['Mvir'])
                            Plots['luminous_Inner'][-1].append(float((halo['Mstar_Inner']+halo['Mgas_Inner'])/halo['Mvir_Inner']))

for i in np.flip(np.arange(len(Plots['times']))):
    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(pre+r' f$_{b}$ within Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([xlower,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-11,1,80) if args.observed else np.logspace(-7,1,50)
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.text(tlower,1e3,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    ax.hist(Plots['dark'][i],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(Plots['dark'][i],bins,color='lightcoral',alpha=.7)
    ax.hist(Plots['luminous'][i],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(Plots['luminous'][i],bins,color='cornflowerblue',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../GifPlots/{pre}Entire.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/{pre}Entire.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='Plot.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(pre+r' f$_{b}$ within .1*Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([xlower,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-11,1,80) if args.observed else np.logspace(-7,1,50)
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.text(tlower,1e3,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    ax.hist(Plots['dark_Inner'][i],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(Plots['dark_Inner'][i],bins,color='lightcoral',alpha=.7)
    ax.hist(Plots['luminous_Inner'][i],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(Plots['luminous_Inner'][i],bins,color='cornflowerblue',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../GifPlots/{pre}Inner.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/{pre}Inner.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='Plot.py'
    plt.close()

imagenames = os.listdir('../GifPlots/')
imagenames = np.sort(np.array(imagenames))
images,images_inner = [[],[]]
for name in imagenames:
    if name.split('.')[0]==f'{pre}Entire':
        images.append(imageio.imread(f'../GifPlots/{name}'))
    elif name.split('.')[0]==f'{pre}Inner':
        images_inner.append(imageio.imread(f'../GifPlots/{name}'))
imageio.mimsave(f'../Plots/{pre}EntireBaryonicFraction.gif', images, duration=.15)
meta = OSXMetaData(f'../Plots/{pre}EntireBaryonicFraction.gif')
meta.creator='Plot.py'
imageio.mimsave(f'../Plots/{pre}InnerBaryonicFraction.gif', images_inner, duration=.15)
meta = OSXMetaData(f'../Plots/{pre}InnerBaryonicFraction.gif')
meta.creator='Plot.py'