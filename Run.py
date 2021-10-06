import os

pythonpath = '/myhome2/users/vannest/anaconda3/bin/python'
for sim in ['cptmarvel','elektra','storm','rogue']:
    with open(f'textfiles/{sim}.steps.txt') as f:
        steps = f.readlines()
    steps = [s.rstrip('\n') for s in steps]
    steps.reverse()
    for ts in steps:
        print(f'Running {sim}-00{ts}:')
        os.system(f'{pythonpath} BaryonicFractionData.py -s {sim} -t {ts} -n 10')