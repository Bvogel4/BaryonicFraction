import pickle
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData

Romulus = pickle.load(open('../DataFiles/RomulusData.pickle','rb'))
Marvel = pickle.load(open('../DataFiles/BaryonicFractionData.pickle','rb'))

Plots={'field':{'dwarf':[],'udg':[]},
        'satellite':{'dwarf':[],'udg':[]},
        'cluster':{'dwarf':[],'udg':[]}}
PlotsInner={'field':{'dwarf':[],'udg':[]},
        'satellite':{'dwarf':[],'udg':[]},
        'cluster':{'dwarf':[],'udg':[]}}

envs,types = [['field','satellite','cluster'],['dwarf','udg']]
for e in envs:
    for t in types:
        for h in Romulus[e][t]:
            halo = Romulus[e][t][h]
            Plots[e][t].append((float(halo['Mstar'])+float(halo['Mgas']))/float(halo['Mvir']))
            PlotsInner[e][t].append((float(halo['Mstar_Inner'])+float(halo['Mgas_Inner']))/float(halo['Mvir_Inner']))

MarBf,MarBf_Inner=[[],[]]
for sim in Marvel:
    for h in Marvel[sim]['4096']['halos']:
        halo = Marvel[sim]['4096']['halos'][h]
        MarBf.append((float(halo['Mstar'])+float(halo['Mgas']))/float(halo['Mvir']))
        MarBf_Inner.append((float(halo['Mstar_Inner'])+float(halo['Mgas_Inner']))/float(halo['Mvir_Inner']))


f,ax = plt.subplots(1,1,figsize=(11,8))
ax.set_ylabel('N',fontsize=25)
ax.set_xlabel(r'f$_{b}$ within Rvir',fontsize=25)
ax.tick_params(length=5,labelsize=15)
ax.set_xlim([1e-7,1])
ax.semilogx()
ax.set_ylim([6e-1,2e3])
ax.semilogy()
bins = np.logspace(-7,1,50,)
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Romulus Field')
ax.plot(0,0,color='lightcoral',linewidth=2,label='Marvel')
ax.hist(Plots['field']['udg']+Plots['field']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(Plots['field']['udg']+Plots['field']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.hist(MarBf,bins,histtype='step',color='darkred',linewidth=3)
ax.hist(MarBf,bins,color='lightcoral',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/MarvelVsRomField.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/MarvelVsRomField.png')
meta.creator='MarvelVsRomField.Plot.py'
plt.close()

f,ax = plt.subplots(1,1,figsize=(11,8))
ax.set_ylabel('N',fontsize=25)
ax.set_xlabel(r'f$_{b}$ within .1*Rvir',fontsize=25)
ax.tick_params(length=5,labelsize=15)
ax.set_xlim([1e-7,1])
ax.semilogx()
ax.set_ylim([6e-1,2e3])
ax.semilogy()
bins = np.logspace(-7,1,50,)
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Romulus Field')
ax.plot(0,0,color='lightcoral',linewidth=2,label='Marvel')
ax.hist(PlotsInner['field']['udg']+Plots['field']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(PlotsInner['field']['udg']+Plots['field']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.hist(MarBf_Inner,bins,histtype='step',color='darkred',linewidth=3)
ax.hist(MarBf_Inner,bins,color='lightcoral',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/MarvelVsRomField.Inner.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/MarvelVsRomField.Inner.png')
meta.creator='MarvelVsRomField.Plot.py'
plt.close()