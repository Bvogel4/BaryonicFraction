import argparse,os,pickle,sys,warnings
warnings.filterwarnings('ignore')
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

parser = argparse.ArgumentParser()
parser.add_argument("-o","--overwrite",action='store_true')
parser.add_argument("-s","--simulation",choices=['h148','h229','h242','h329'],required=True)
args = parser.parse_args()

try:
    Data = pickle.load(open('../DataFiles/MergerHistories.DCJL.pickle','rb'))
    overwrite = False
except:
    overwrite = True
if overwrite or args.overwrite:
    print('Creating New DataFile')
    Data = {'h148':{},'h229':{},'h242':{},'h329':{}}
else:
    print('DataFile Loaded')

DBs = {
    'h148':'/myhome2/users/munshi/e12gals/h148.cosmo50PLK.3072g3HbwK1BH/',
    'h229':'/myhome2/users/munshi/e12gals/h229.cosmo50PLK.3072gst5HbwK1BH/',
    'h242':'/myhome2/users/munshi/e12gals/h242.cosmo50PLK.3072gst5HbwK1BH/',
    'h329':'/myhome2/users/munshi/e12gals/h329.cosmo50PLK.3072gst5HbwK1BH/'
}

print('Loading Database...')
os.environ['TANGOS_DB_CONNECTION'] = f'{DBs[args.simulation]}{args.simulation}.working.db'
import tangos
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
        mergers = tangos.relation_finding.MultiHopMostRecentMergerStrategy(input_halo, order_by='weight').all()
        if len(mergers)>0 :
            for m in mergers[1:]:
                times.append(mergers[0].timestep.next.time_gyr)
                halo.append((mergers[0], m))
                ratio.append(float(mergers[0].NDM)/m.NDM)
            input_halo = mergers[0]
        else:
            input_halo = None

    return np.array(times), np.array(ratio), halo

sim = tangos.get_simulation(DBs[args.simulation].split('/')[-2])[-1]
hid,grp,ngas,nstar = sim.calculate_all('halo_number()','Grp','N_gas','N_star')
hid = hid[(ngas>0) | (nstar>0)]
grp = grp[(ngas>0) | (nstar>0)]
for i in grp: Data[args.simulation][str(i)] = {'times':[],'ratios':[],'halos':[]}
myprint('Database Loaded',clear=True)

print('Writing: 0.00%')
prog=0
for i in np.arange(len(hid)):
    t,r,h = get_mergers_of_major_progenitor(sim[int(hid[i])])
    for j in np.arange(len(t)):
        Data[args.simulation][str(grp[i])]['times'].append(t[j])
        Data[args.simulation][str(grp[i])]['ratios'].append(r[j])
        Data[args.simulation][str(grp[i])]['halos'].append((h[j][0]['Grp'],h[j][1]['Grp']))
    prog+=1
    myprint(f'Writing: {round(prog/len(hid)*100,2)}%',clear=True)

out = open('../DataFiles/MergerHistories.DCJL.pickle','wb')
pickle.dump(Data,out)
out.close()
myprint('Done',clear=True)
