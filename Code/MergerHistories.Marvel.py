import argparse,os,pickle,sys
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

parser = argparse.ArgumentParser()
parser.add_argument("-o","--overwrite",action='store_true')
parser.add_argument("-s","--simulation",choices=['cptmarvel','elektra','storm','rogue'],required=True)
args = parser.parse_args()

try:
    Data = pickle.load(open('../DataFiles/MergerHistories.Marvel.pickle','rb'))
    print('DataFile Loaded')
except:
    overwrite = True
if overwrite or args.overwrite:
    print('Creating New DataFile')
    Data = {'cptmarvel':{},'elektra':{},'storm':{},'rogue':{}}

DBs = {
    'cptmarvel':'/myhome2/users/munshi/dwarf_volumes/cptmarvel.cosmo25cmb.4096g5HbwK1BH/',
    'elektra':'/myhome2/users/munshi/dwarf_volumes/elektra.cosmo25cmb.4096g5HbwK1BH/',
    'storm':'/myhome2/users/munshi/dwarf_volumes/storm.cosmo25cmb.4096g5HbwK1BH/',
    'rogue':'/myhome2/users/munshi/dwarf_volumes/rogue.cosmo25cmb.4096g5HbwK1BH/'
}

print('Loading Database...')
os.environ['TANGOS_DB_CONNECTION'] = DBs[args.simulation]+f'{args.simulation}.working.db'
from __future__ import absolute_import
import tangos as db
import tangos.relation_finding
import numpy as np

def get_mergers_of_major_progenitor(input_halo):
    """Given a halo, return the redshifts and ratios of all mergers on the major progenitor branch

    :parameter input_halo - the halo to consider the history of
    :type input_halo tangos.core.Halo

    :returns redshift, ratio, halo - arrays of the redshifts, ratios (1:X) and halo DB objects for the mergers
    """
    times = []
    ratio = []
    halo  = []
    while input_halo is not None:
        mergers = db.relation_finding.MultiHopMostRecentMergerStrategy(input_halo, order_by='weight').all()
        if len(mergers)>0 :
            for m in mergers[1:]:
                times.append(mergers[0].timestep.next.time_gyr)
                halo.append((mergers[0], m))
                ratio.append(float(mergers[0].NDM)/m.NDM)
            input_halo = mergers[0]
        else:
            input_halo = None

    return np.array(times), np.array(ratio), halo

sim = tangos.get_simulation(DBs[args.simulation].split('/')[-1])[-1]
hid,grp,ngas = sim.calculate_all('halo_number()','Grp','N_gas')
hid = hid[ngas>0]
grp = grp[ngas>0]
ngas = ngas[ngas>0]
for i in grp: Data[args.simulation][str(i)] = {'times':[],'ratios':[],'halos':[]}
myprint('Database Loaded',clear=True)

print('Writing: 0.00%')
prog=0
for i in np.arange(len(hid)):
    t,r,h = get_mergers_of_major_progenitor(sim[hid[i]])
    for j in np.arange(len(t)):
        Data[args.simulation][str(grp[i])]['times'].append(t[j])
        Data[args.simulation][str(grp[i])]['ratios'].append(r[j])
        Data[args.simulation][str(grp[i])]['halos'].append((h[j][0]['Grp'],h[j][1]['Grp']))
    myprint(f'Writing: {round(prog/len(hid)*100,2)}%',clear=True)

out = open('../DataFiles/MergerHistories.Marvel.pickle','wb')
pickle.dump(Data,out)
out.close()
myprint('Done',clear=True)