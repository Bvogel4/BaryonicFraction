import argparse,pickle,pymp,pynbody,sys,warnings
import numpy as np
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['Rom25','RomC'],required=True)
args = parser.parse_args()

fudg,fdwf,sudg,sdwf,cudg,cdwf=[[],[],[],[],[],[]]
Data = pickle.load(open('RomulusData.pickle','rb'))
for h in Data['field']['dwarf']: fdwf.append(int(h))
for h in Data['field']['udg']: fudg.append(int(h))
for h in Data['satellite']['dwarf']: sdwf.append(int(h))
for h in Data['satellite']['udg']: sudg.append(int(h))
for h in Data['cluster']['dwarf']: cdwf.append(int(h))
for h in Data['cluster']['udg']: cudg.append(int(h))

if args.simulation == 'Rom25':
    simpath = '/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192'
    halos = fdwf+fudg+sdwf+sudg
else:
    simpath = '/myhome2/users/munshi/Romulus/h1.cosmo50/h1.cosmo50PLK.1536gst1bwK1BH.004096'
    halos = cdwf+cudg

print(f'Loading {args.simulation}...')
s = pynbody.load(simpath)
s.physical_units()
h = s.halos(dosort=True)
SharedData = pymp.shared.dict()
prog=pymp.shared.array((1,),dtype=int)
myprint(f'{args.simulation} Loaded. {len(halos)} halos to analyze.\nWriting: 0.00%',clear=True)

with pymp.Parallel(10) as pl:
    for i in pl.xrange(len(halos)):
        halo = h[halos[i]]
        current = {}

        current['Mvir'] = halo['mass'].sum()
        current['Mgas'] = halo.g['mass'].sum()
        current['Mstar'] = halo.s['mass'].sum()
        try:
            pynbody.analysis.halo.center(halo)
            Rvir = pynbody.analysis.halo.virial_radius(halo)
            sphere = pynbody.filt.Sphere(.1*Rvir,(0,0,0))
            current['Rvir'] = Rvir
            current['Mvir_Inner'] = halo[sphere]['mass'].sum()
            current['Mgas_Inner'] = halo.g[sphere]['mass'].sum()
            current['Mstar_Inner'] = halo.s[sphere]['mass'].sum()
        except:
            pass

        prog[0]+=1
        myprint(f'\tWriting {round(prog[0]/len(halos)*100,2)}%',clear=True)
        SharedData[str(halos[i])] = current
        del current

for j in halos:
    if j in fdwf: Data['field']['dwarf'][str(j)] = SharedData[str(j)]
    if j in fudg: Data['field']['udg'][str(j)] = SharedData[str(j)]
    if j in sdwf: Data['satellite']['dwarf'][str(j)] = SharedData[str(j)]
    if j in sudg: Data['satellite']['udg'][str(j)] = SharedData[str(j)]
    if j in cdwf: Data['cluster']['dwarf'][str(j)] = SharedData[str(j)]
    if j in cudg: Data['cluster']['udg'][str(j)] = SharedData[str(j)]

out = open('RomulusData.pickle','wb')
pickle.dump(Data,out)
out.close()
myprint('Data File Updated',clear=True)
