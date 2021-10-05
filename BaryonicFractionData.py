import argparse,pickle,pymp,pynbody,sys,warnings
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['cptmarvel','elektra','storm','rogue'],required=True)
parser.add_argument("-t","--timestep",required=True)
parser.add_argument("-n","--numproc",required=True,type=int)
args = parser.parse_args()

simpath = f'/myhome2/users/munshi/dwarf_volumes/{args.simulation}.cosmo25cmb.4096g5HbwK1BH/{args.simulation}.cosmo25cmb.4096g5HbwK1BH.00{args.timestep}'
try:
    with open(simpath+'.M200.amiga.stat') as f:
        stat = f.readlines()
        del stat[0]
except:
    print(f'Timestep {args.simulation}-00{args.timestep} has no stat file.')
    sys.exit()

try:
    Data = pickle.load(open('BaryonicFractionData.pickle','rb'))
    

luminous,dark,resolved = [[],[],[]]
for line in stat:
    grp = int(line.split()[0])
    ngas = int(line.split()[2])
    nstar = int(line.split()[3])
    if ngas > 0:
        resolved.append(grp)
        if nstar > 0:
            luminous.append(grp)
        else:
            dark.append(grp)
print(f'{len(resolved)} resolved halos to analyze.\nLoading {args.simulation}-00{args.timestep}...')

s = pynbody.load(simpath)
s.physical_units()
h = s.halos()
time = s.properties['time'].in_units('Gyr')
myprint(f'{args.simulation}-00{args.timestep} Loaded.',clear=True)

with pymp.Parallel(args.numproc) as pl:
    for i in pl.xrange(len(resolved)):
        hid = resolved[i]