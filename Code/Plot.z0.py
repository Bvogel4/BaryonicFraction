import argparse,imageio,os,pickle,warnings
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['Marvel','DCJL'],required=True)
parser.add_argument("-r","--resolved",action="store_true")
args = parser.parse_args()

res_halos = {
    'cptmarvel' :  [1,2,3,5,6,7,10,11,13,14,24],
    'elektra' : [1,2,3,4,5,8,9,10,11,12,17,36,64],
    'storm' : [1,2,3,4,5,6,7,8,10,11,12,14,15,22,23,31,37,44,48,55,118],
    'rogue' : [1,3,7,8,10,11,12,15,16,17,28,31,37,58,116],
    'h148' : [2,3,4,6,7,11,12,13,15,20,23,27,28,29,33,34,37,38,41,43,51,59,65,75,86,94,109,114,122],
    'h229' : [2,3,6,14,15,18,20,22,25,33,47,48,49,52,57,62,89,92,127],
    'h242' : [8,10,21,26,30,34,38,42,44,45,63,70,81,138],
    'h329' : [7,29,30,37,53,92,115,117,127]
}

res = '.Resolved' if args.resolved else ''

Data = pickle.load(open(f'../DataFiles/{args.simulation}.z0.pickle','rb'))
Plots = {'dark':[],'luminous':[],'dark_Inner':[],'luminous_Inner':[],'dark_Center':[],'luminous_Center':[]}
ObsPlots = {'dark':[],'luminous':[],'dark_Inner':[],'luminous_Inner':[],'dark_Center':[],'luminous_Center':[]}
GasPlots = {'dark':[],'luminous':[],'dark_Inner':[],'luminous_Inner':[],'dark_Center':[],'luminous_Center':[]}
StarPlots = {'dark':[],'luminous':[],'dark_Inner':[],'luminous_Inner':[],'dark_Center':[],'luminous_Center':[]}

sims = ['cptmarvel','elektra','storm','rogue'] if args.simulation=='Marvel' else ['h148','h229','h242','h329']
c1,c2 = [['','_Inner','_Center'],['','.1','.01']]
for s in sims:
    for h in Data[s]:
        halo = Data[s][h]
        if args.resolved:
            lum = True if int(h) in res_halos[s] else False
        else:
            lum = True if halo['Mstar']>0 else False
        for t in [0,1,2]:
            if lum:
                Plots['luminous'+c1[t]].append(float((halo[c2[t]+'Mstar']+halo[c2[t]+'Mgas'])/halo[c2[t]+'Mvir']))
                ObsPlots['luminous'+c1[t]].append(float((.6*halo[c2[t]+'Mstar']+1.33*halo[c2[t]+'MHI'])/halo[c2[t]+'Mvir']))
                GasPlots['luminous'+c1[t]].append(float((1.4*(halo[c2[t]+'MHI']+halo[c2[t]+'MHII']))/halo[c2[t]+'Mvir']))
                StarPlots['luminous'+c1[t]].append(float(halo[c2[t]+'Mstar']/halo[c2[t]+'Mvir']))
            else:
                Plots['dark'+c1[t]].append(float((halo[c2[t]+'Mstar']+halo[c2[t]+'Mgas'])/halo[c2[t]+'Mvir']))
                ObsPlots['dark'+c1[t]].append(float((.6*halo[c2[t]+'Mstar']+1.33*halo[c2[t]+'MHI'])/halo[c2[t]+'Mvir']))
                GasPlots['dark'+c1[t]].append(float((1.4*(halo[c2[t]+'MHI']+halo[c2[t]+'MHII']))/halo[c2[t]+'Mvir']))
                StarPlots['dark'+c1[t]].append(float(halo[c2[t]+'Mstar']/halo[c2[t]+'Mvir']))

titles = ['Entire','Inner','Center']
for t in [0,1,2]:
    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'f$_{b}$ within '+c2[t]+r'R$_{vir}$',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([1e-7,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-7,1,50) 
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.hist(Plots['luminous'+c1[t]],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(Plots['luminous'+c1[t]],bins,color='cornflowerblue',alpha=.7)
    ax.hist(Plots['dark'+c1[t]],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(Plots['dark'+c1[t]],bins,color='lightcoral',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/{args.simulation}z0{res}.{titles[t]}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/{args.simulation}z0{res}.{titles[t]}.png')
    meta.creator='Plot.z0.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'Observed f$_{b}$ within '+c2[t]+r'R$_{vir}$',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([1e-11,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-11,1,80)
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.hist(ObsPlots['luminous'+c1[t]],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(ObsPlots['luminous'+c1[t]],bins,color='cornflowerblue',alpha=.7)
    ax.hist(ObsPlots['dark'+c1[t]],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(ObsPlots['dark'+c1[t]],bins,color='lightcoral',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Observed.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Observed.png')
    meta.creator='Plot.z0.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'f$_{gas}$ within '+c2[t]+r'R$_{vir}$',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([1e-6,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-11,1,80)
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.hist(GasPlots['luminous'+c1[t]],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(GasPlots['luminous'+c1[t]],bins,color='cornflowerblue',alpha=.7)
    ax.hist(GasPlots['dark'+c1[t]],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(GasPlots['dark'+c1[t]],bins,color='lightcoral',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Gas.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Gas.png')
    meta.creator='Plot.z0.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'f$_{stellar}$ within '+c2[t]+r'R$_{vir}$',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([10**(-6.2),1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    bins = np.logspace(-11,1,80)
    ax.plot(0,0,color='navy',linewidth=2,label='Luminous Halos')
    ax.plot(0,0,color='darkred',linewidth=2,label='Dark Halos')
    ax.hist(StarPlots['luminous'+c1[t]],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(StarPlots['luminous'+c1[t]],bins,color='cornflowerblue',alpha=.7)
    ax.hist(StarPlots['dark'+c1[t]],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(StarPlots['dark'+c1[t]],bins,color='lightcoral',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Stellar.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/{args.simulation}z0{res}.{titles[t]}.Stellar.png')
    meta.creator='Plot.z0.py'
    plt.close()