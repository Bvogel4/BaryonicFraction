import imageio,os,pickle
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData

mint = [1.29,1.94,2.2,2.5,3,3.8,4,4.4,4.7,5,5.17,5.5,6.05,6.4,6.7,7.2,7.7,8,8.3,
        8.6,9,9.4,9.8,10,10.6,10.8,11,11.5,11.9,12.1,12.4,12.8,13.3,13.7]
maxt = [1.3,2.16,2.3,2.6,3.3,3.9,4.3,4.6,4.9,5.16,5.5,5.8,6.2,6.5,6.9,7.5,7.8,8.2,8.6,
        8.9,9.1,9.7,10,10.4,10.8,11,11.3,11.6,12.1,12.3,12.6,12.9,13.6,13.8]
Data = pickle.load(open('../DataFiles/BaryonicFractionData.pickle','rb'))
Plots = {'times':[],'Mstar':[],'Fb':[],'Fb_Inner':[]}

sims,times = [['cptmarvel','elektra','storm','rogue'],[]]
for i in np.arange(len(mint)):
    Plots['times'].append((mint[i]+maxt[i])/2)
    Plots['Mstar'].append([])
    Plots['Fb'].append([])
    Plots['Fb_Inner'].append([])
    for sim in sims:
        for t in Data[sim]:
            if mint[i]<Data[sim][t]['time']<maxt[i]:
                for h in Data[sim][t]['halos']:
                    halo = Data[sim][t]['halos'][h]
                    if halo['Mstar'] > 0:
                        Plots['Fb'][-1].append((halo['Mstar']+halo['Mgas'])/halo['Mvir'])
                        Plots['Fb_Inner'][-1].append(float((halo['Mstar_Inner']+halo['Mgas_Inner'])/halo['Mvir_Inner']))
                        Plots['Mstar'][-1].append(halo['Mstar'])

for i in np.flip(np.arange(len(Plots['times']))):
    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_xlabel(r'M$_*$',fontsize=25)
    ax.set_ylabel(r'f$_{b}$ within Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_ylim([1e-7,1])
    ax.semilogy()
    ax.set_xlim([1e2,1e10])
    ax.semilogx()
    ax.text(4e7,2e-7,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    ax.scatter(Plots['Mstar'][i],Plots['Fb'][i],c='k')
    f.savefig(f'../GifPlots/Observed.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/Observed.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='FbVsMstar.Plot.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_xlabel(r'M$_*$',fontsize=25)
    ax.set_ylabel(r'f$_{b}$ within Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_ylim([1e-7,1])
    ax.semilogy()
    ax.set_xlim([1e2,1e10])
    ax.semilogx()
    ax.text(4e7,2e-7,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    ax.scatter(Plots['Mstar'][i],Plots['Fb_Inner'][i],c='k')
    f.savefig(f'../GifPlots/ObservedInner.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/ObservedInner.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='FbVsMstar.Plot.py'
    plt.close()

imagenames = os.listdir('../GifPlots/')
imagenames = np.sort(np.array(imagenames))
images,images_inner = [[],[]]
for name in imagenames:
    if name.split('.')[0]=='Observed':
        images.append(imageio.imread(f'../GifPlots/{name}'))
    elif name.split('.')[0]=='ObservedInner':
        images_inner.append(imageio.imread(f'../GifPlots/{name}'))
imageio.mimsave('../Plots/ObservedBaryonicFraction.gif', images, duration=.15)
meta = OSXMetaData('../Plots/ObservedBaryonicFraction.gif')
meta.creator='FbVsMstar.Plot.py'
imageio.mimsave('../Plots/ObservedInnerBaryonicFraction.gif', images_inner, duration=.15)
meta = OSXMetaData('../Plots/ObservedInnerBaryonicFraction.gif')
meta.creator='FbVsMstar.Plot.py'