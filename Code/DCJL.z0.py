import argparse,pickle,pymp,pynbody,sys,warnings
import numpy as np
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['h148','h229','h242','h329'],required=True)
parser.add_argument("-n","--numproc",required=True,type=int)
args = parser.parse_args()

#Verify that data file exists, and that the data hasn't already been calculated
try:
    Data = pickle.load(open('DataFiles/DCJL.z0.pickle','rb'))
except:
    print('Please initiate Data File')
    sys.exit()

if Data[args.simulation]:
    print('Simulation already completed')
    sys.exit()

#Verify that simulation step is readable/exists
if args.simulation=='h148':
    simpath = '/myhome2/users/munshi/e12gals/h148.cosmo50PLK.3072g3HbwK1BH/h148.cosmo50PLK.3072g3HbwK1BH.004096/h148.cosmo50PLK.3072g3HbwK1BH.004096'
else:
    simpath = f'/myhome2/users/munshi/e12gals/{args.simulation}.cosmo50PLK.3072gst5HbwK1BH/{args.simulation}.cosmo50PLK.3072gst5HbwK1BH.004096/{args.simulation}.cosmo50PLK.3072gst5HbwK1BH.004096'
try:
    with open(simpath+'.M200.amiga.stat') as f:
        stat = f.readlines()
        del stat[0]
except:
    print(f'\tTimestep {args.simulation}-004096 has no stat file.')
    sys.exit()

Data[args.simulation] = {}
resolved = []
for line in stat:
    grp = int(line.split()[0])
    ngas = int(line.split()[2])
    nstar = int(line.split()[3])
    if ngas > 0:
        resolved.append(grp)
        Data[args.simulation][str(grp)] = {'Rvir':float(line.split()[6]),
                                            'Mvir':float(line.split()[5]),
                                            'Mgas':float(line.split()[7]),
                                            'Mstar':float(line.split()[8])}
print(f'\t{len(resolved)} resolved halos to analyze.\n\tLoading {args.simulation}-004096...')

s = pynbody.load(simpath)
s.physical_units()
h = s.halos()
InnerData = pymp.shared.dict()
prog=pymp.shared.array((1,),dtype=int)
myprint(f'\t{args.simulation}-004096 Loaded.',clear=True)
print('\tWriting: 0.00%')

with pymp.Parallel(args.numproc) as pl:
    for i in pl.xrange(len(resolved)):
        halo = h[resolved[i]]
        current = {'MHI':sum(halo.g['HI']*halo.g['mass']),'MHII':sum(halo.g['HII']*halo.g['mass']),
                    '.1Mvir':np.nan,'.1Mstar':np.nan,'.1Mgas':np.nan,'.1MHI':np.nan,'.1MHII':np.nan,
                    '.01Mvir':np.nan,'.01Mstar':np.nan,'.01Mgas':np.nan,'.01MHI':np.nan,',01MHII':np.nan}

        try:
            pynbody.analysis.halo.center(halo)
            Rvir = Data[args.simulation][str(resolved[i])]['Rvir']
            sphere = pynbody.filt.Sphere(.1*Rvir,(0,0,0)) if .1*Rvir>.2 else pynbody.filt.Sphere(.2,(0,0,0))
            current['.1Mvir'] = halo[sphere]['mass'].sum()
            current['.1Mgas'] = halo.g[sphere]['mass'].sum()
            current['.1Mstar'] = halo.s[sphere]['mass'].sum()
            current['.1MHI'] = sum(halo.g[sphere]['HI']*halo.g[sphere]['mass'])
            current['.1MHII'] = sum(halo.g[sphere]['HII']*halo.g[sphere]['mass'])
            sphere = pynbody.filt.Sphere(.01*Rvir,(0,0,0)) if .01*Rvir>.2 else pynbody.filt.Sphere(.2,(0,0,0))
            current['.01Mvir'] = halo[sphere]['mass'].sum()
            current['.01Mgas'] = halo.g[sphere]['mass'].sum()
            current['.01Mstar'] = halo.s[sphere]['mass'].sum()
            current['.01MHI'] = sum(halo.g[sphere]['HI']*halo.g[sphere]['mass'])
            current['.01MHII'] = sum(halo.g[sphere]['HII']*halo.g[sphere]['mass'])
        except:
            pass

        prog[0]+=1
        myprint(f'\tWriting {round(prog[0]/len(resolved)*100,2)}%',clear=True)
        InnerData[str(resolved[i])] = current
        del current

for halo in resolved:
    Data[args.simulation][str(halo)]['MHI'] = InnerData[str(halo)]['MHI']
    Data[args.simulation][str(halo)]['MHII'] = InnerData[str(halo)]['MHII']
    Data[args.simulation][str(halo)]['.1Mvir'] = InnerData[str(halo)]['.1Mvir']
    Data[args.simulation][str(halo)]['.1Mgas'] = InnerData[str(halo)]['.1Mgas']
    Data[args.simulation][str(halo)]['.1Mstar'] = InnerData[str(halo)]['.1Mstar']
    Data[args.simulation][str(halo)]['.1MHI'] = InnerData[str(halo)]['.1MHI']
    Data[args.simulation][str(halo)]['.1MHII'] = InnerData[str(halo)]['.1MHII']
    Data[args.simulation][str(halo)]['.01Mvir'] = InnerData[str(halo)]['.01Mvir']
    Data[args.simulation][str(halo)]['.01Mgas'] = InnerData[str(halo)]['.01Mgas']
    Data[args.simulation][str(halo)]['.01Mstar'] = InnerData[str(halo)]['.01Mstar']
    Data[args.simulation][str(halo)]['.01MHI'] = InnerData[str(halo)]['.01MHI']
    Data[args.simulation][str(halo)]['.01MHII'] = InnerData[str(halo)]['.01MHII']

out = open('DataFiles/DCJL.z0.pickle','wb')
pickle.dump(Data,out)
out.close()
myprint(f'\tData File Updated with {args.simulation}-004096',clear=True)