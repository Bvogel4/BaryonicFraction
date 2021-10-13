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

stellarbins = np.linspace(2,10,9)

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
    f.savefig(f'../GifPlots/FbVsMstar.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/FbVsMstar.{int(Plots["times"][i]*100):04d}.png')
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
    f.savefig(f'../GifPlots/FbInnerVsMstar.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/FbInnerVsMstar.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='FbVsMstar.Plot.py'
    plt.close()

    f1,ax1 = plt.subplots(1,1,figsize=(11,8))
    ax1.set_ylabel('N',fontsize=25)
    ax1.set_xlabel(r'f$_{b}$ within .Rvir',fontsize=25)
    ax1.tick_params(length=5,labelsize=15)
    ax1.set_xlim([1e-7,1])
    ax1.semilogx()
    ax1.set_ylim([6e-1,2e3])
    ax1.semilogy()
    ax1.text(1e-2,1e3,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    f2,ax2 = plt.subplots(1,1,figsize=(11,8))
    ax2.set_ylabel('N',fontsize=25)
    ax2.set_xlabel(r'f$_{b}$ within .1*Rvir',fontsize=25)
    ax2.tick_params(length=5,labelsize=15)
    ax2.set_xlim([1e-7,1])
    ax2.semilogx()
    ax2.set_ylim([6e-1,2e3])
    ax2.semilogy()
    ax2.text(1e-2,1e3,f'Time: {round(Plots["times"][i],2)} Gyr',fontsize=25)
    bins = np.logspace(-7,1,50)
    for j in np.arange(len(stellarbins)-1):
        Fb,Fb_Inner= [[],[]]
        for ind in np.arange(len(Plots['Mstar'][i])):
            if stellarbins[j]<np.log10(Plots['Mstar'][i][ind])<stellarbins[j+1]:
                Fb.append(Plots['Fb'][i][ind])
                Fb_Inner.append(Plots['Fb_Inner'][i][ind])
        ax1.plot(0,0,color=plt.get_cmap('hsv')(1*j/(len(stellarbins)-1)),linewidth=2,label=f'{stellarbins[j]}'+r'$<$Log$_{10}$(M$_*$)$<$'+f'{stellarbins[j+1]}')
        ax2.plot(0,0,color=plt.get_cmap('hsv')(1*j/(len(stellarbins)-1)),linewidth=2,label=f'{stellarbins[j]}'+r'$<$Log$_{10}$(M$_*$)$<$'+f'{stellarbins[j+1]}')
        ax1.hist(Fb,bins,histtype='step',color=plt.get_cmap('hsv')(1*j/(len(stellarbins)-1)),linewidth=3)
        ax2.hist(Fb_Inner,bins,histtype='step',color=plt.get_cmap('hsv')(1*j/(len(stellarbins)-1)),linewidth=3)
    ax1.legend(loc='upper left',prop={'size':15})
    f1.savefig(f'../GifPlots/FbStellarBins.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/FbStellarBins.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='FbVsMstar.Plot.py'
    ax2.legend(loc='upper left',prop={'size':15})
    f2.savefig(f'../GifPlots/FbStellarBinsInner.{int(Plots["times"][i]*100):04d}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../GifPlots/FbStellarBinsInner.{int(Plots["times"][i]*100):04d}.png')
    meta.creator='FbVsMstar.Plot.py'
    plt.close(f1)
    plt.close(f2)

imagenames = os.listdir('../GifPlots/')
imagenames = np.sort(np.array(imagenames))
images,images_inner,binimages,binimages_inner = [[],[],[],[]]
for name in imagenames:
    if name.split('.')[0]=='FbVsMstar':
        images.append(imageio.imread(f'../GifPlots/{name}'))
    elif name.split('.')[0]=='FbInnerVsMstar':
        images_inner.append(imageio.imread(f'../GifPlots/{name}'))
    elif name.split('.')[0]=='FbStellarBins':
        binimages.append(imageio.imread(f'../GifPlots/{name}'))
    elif name.split('.')[0]=='FbStellarBinsInner':
        binimages_inner.append(imageio.imread(f'../GifPlots/{name}'))
imageio.mimsave('../Plots/FbVsMstar.gif', images, duration=.15)
meta = OSXMetaData('../Plots/FbVsMstar.gif')
meta.creator='FbVsMstar.Plot.py'
imageio.mimsave('../Plots/FbInnerVsMstar.gif', images_inner, duration=.15)
meta = OSXMetaData('../Plots/FbInnerVsMstar.gif')
meta.creator='FbVsMstar.Plot.py'
imageio.mimsave('../Plots/FbStellarBins.gif',binimages, duration=.15)
meta = OSXMetaData('../Plots/FbStellarBins.gif')
meta.creator='FbVsMstar.Plot.py'
imageio.mimsave('../Plots/FbStellarBinsInner.gif', binimages_inner, duration=.15)
meta = OSXMetaData('../Plots/FbStellarBinsInner.gif')
meta.creator='FbVsMstar.Plot.py'