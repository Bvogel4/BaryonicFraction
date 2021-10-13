import imageio,os,pickle
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData

Data = pickle.load(open('../DataFiles/RomulusData.pickle','rb'))

Plots={'field':{'dwarf':[],'udg':[]},
        'satellite':{'dwarf':[],'udg':[]},
        'cluster':{'dwarf':[],'udg':[]}}
PlotsInner={'field':{'dwarf':[],'udg':[]},
        'satellite':{'dwarf':[],'udg':[]},
        'cluster':{'dwarf':[],'udg':[]}}

envs,types = [['field','satellite','cluster'],['dwarf','udg']]
for e in envs:
    for t in types:
        for h in Data[e][t]:
            halo = Data[e][t][h]
            Plots[e][t].append((float(halo['Mstar'])+float(halo['Mgas']))/float(halo['Mvir']))
            PlotsInner[e][t].append((float(halo['Mstar_Inner'])+float(halo['Mgas_Inner']))/float(halo['Mvir_Inner']))

f,ax = plt.subplots(1,1,figsize=(11,8))
ax.set_ylabel('N',fontsize=25)
ax.set_xlabel(r'f$_{b}$ within Rvir',fontsize=25)
ax.tick_params(length=5,labelsize=15)
ax.set_xlim([1e-7,1])
ax.semilogx()
ax.set_ylim([6e-1,2e3])
ax.semilogy()
bins = np.logspace(-7,1,50,)
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Dwarfs')
ax.plot(0,0,color='lightcoral',linewidth=2,label='UDGs')
ax.hist(Plots['field']['udg']+Plots['satellite']['udg']+Plots['cluster']['udg'],bins,histtype='step',color='darkred',linewidth=3)
ax.hist(Plots['field']['udg']+Plots['satellite']['udg']+Plots['cluster']['udg'],bins,color='lightcoral',alpha=.7)
ax.hist(Plots['field']['dwarf']+Plots['satellite']['dwarf']+Plots['cluster']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(Plots['field']['dwarf']+Plots['satellite']['dwarf']+Plots['cluster']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/Romulus.UDG.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/Romulus.UDG.png')
meta.creator='PlotRomulus.py'
plt.close()

f,ax = plt.subplots(1,1,figsize=(11,8))
ax.set_ylabel('N',fontsize=25)
ax.set_xlabel(r'f$_{b}$ within Rvir',fontsize=25)
ax.tick_params(length=5,labelsize=15)
ax.set_xlim([1e-7,1])
ax.semilogx()
ax.set_ylim([6e-1,2e3])
ax.semilogy()
bins = np.logspace(-7,1,50,)
ax.plot(0,0,color='lightcoral',linewidth=2,label='Isolated')
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Satellite')
ax.plot(0,0,color='0.5',linewidth=2,label='Cluster')
ax.hist(Plots['field']['udg']+Plots['field']['dwarf'],bins,histtype='step',color='darkred',linewidth=3)
ax.hist(Plots['field']['udg']+Plots['field']['dwarf'],bins,color='lightcoral',alpha=.7)
ax.hist(Plots['satellite']['udg']+Plots['satellite']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(Plots['satellite']['udg']+Plots['satellite']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.hist(Plots['cluster']['udg']+Plots['cluster']['dwarf'],bins,histtype='step',color='k',linewidth=3)
ax.hist(Plots['cluster']['udg']+Plots['cluster']['dwarf'],bins,color='0.5',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/Romulus.Environment.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/Romulus.Environment.png')
meta.creator='PlotRomulus.py'
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
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Dwarfs')
ax.plot(0,0,color='lightcoral',linewidth=2,label='UDGs')
ax.hist(PlotsInner['field']['udg']+PlotsInner['satellite']['udg']+PlotsInner['cluster']['udg'],bins,histtype='step',color='darkred',linewidth=3)
ax.hist(PlotsInner['field']['udg']+PlotsInner['satellite']['udg']+PlotsInner['cluster']['udg'],bins,color='lightcoral',alpha=.7)
ax.hist(PlotsInner['field']['dwarf']+PlotsInner['satellite']['dwarf']+PlotsInner['cluster']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(PlotsInner['field']['dwarf']+PlotsInner['satellite']['dwarf']+PlotsInner['cluster']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/RomulusInner.UDG.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/RomulusInner.UDG.png')
meta.creator='PlotRomulus.py'
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
ax.plot(0,0,color='lightcoral',linewidth=2,label='Isolated')
ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Satellite')
ax.plot(0,0,color='0.5',linewidth=2,label='Cluster')
ax.hist(PlotsInner['field']['udg']+PlotsInner['field']['dwarf'],bins,histtype='step',color='darkred',linewidth=3)
ax.hist(PlotsInner['field']['udg']+PlotsInner['field']['dwarf'],bins,color='lightcoral',alpha=.7)
ax.hist(PlotsInner['satellite']['udg']+PlotsInner['satellite']['dwarf'],bins,histtype='step',color='navy',linewidth=3)
ax.hist(PlotsInner['satellite']['udg']+PlotsInner['satellite']['dwarf'],bins,color='cornflowerblue',alpha=.7)
ax.hist(PlotsInner['cluster']['udg']+PlotsInner['cluster']['dwarf'],bins,histtype='step',color='k',linewidth=3)
ax.hist(PlotsInner['cluster']['udg']+PlotsInner['cluster']['dwarf'],bins,color='0.5',alpha=.7)
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/RomulusInner.Environment.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/RomulusInner.Environment.png')
meta.creator='PlotRomulus.py'
plt.close()

for e in Plots:
    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'f$_{b}$ within Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([1e-7,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    ax.set_title(e,fontsize=25)
    bins = np.logspace(-7,1,50,)
    ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Dwarfs')
    ax.plot(0,0,color='lightcoral',linewidth=2,label='UDGs')
    ax.hist(Plots[e]['udg'],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(Plots[e]['udg'],bins,color='lightcoral',alpha=.7)
    ax.hist(Plots[e]['dwarf'],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(Plots[e]['dwarf'],bins,color='cornflowerblue',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/Romulus.UDG.{e}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/Romulus.UDG.{e}.png')
    meta.creator='PlotRomulus.py'
    plt.close()

    f,ax = plt.subplots(1,1,figsize=(11,8))
    ax.set_ylabel('N',fontsize=25)
    ax.set_xlabel(r'f$_{b}$ within .1*Rvir',fontsize=25)
    ax.tick_params(length=5,labelsize=15)
    ax.set_xlim([1e-7,1])
    ax.semilogx()
    ax.set_ylim([6e-1,2e3])
    ax.semilogy()
    ax.set_title(e,fontsize=25)
    bins = np.logspace(-7,1,50,)
    ax.plot(0,0,color='cornflowerblue',linewidth=2,label='Dwarfs')
    ax.plot(0,0,color='lightcoral',linewidth=2,label='UDGs')
    ax.hist(PlotsInner[e]['udg'],bins,histtype='step',color='darkred',linewidth=3)
    ax.hist(PlotsInner[e]['udg'],bins,color='lightcoral',alpha=.7)
    ax.hist(PlotsInner[e]['dwarf'],bins,histtype='step',color='navy',linewidth=3)
    ax.hist(PlotsInner[e]['dwarf'],bins,color='cornflowerblue',alpha=.7)
    ax.legend(loc='upper left',prop={'size':15})
    f.savefig(f'../Plots/RomulusInner.UDG.{e}.png',bbox_inches='tight',pad_inches=.1)
    meta = OSXMetaData(f'../Plots/RomulusInner.UDG.{e}.png')
    meta.creator='PlotRomulus.py'
    plt.close()