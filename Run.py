import os,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['Marvel','z0'],required=True)
args = parser.parse_args()

pythonpath = '/myhome2/users/vannest/anaconda3/bin/python'

if args.simulation=='Marvel':
    for sim in ['cptmarvel','elektra','storm','rogue']:
        with open(f'textfiles/{sim}.steps.txt') as f:
            steps = f.readlines()
        steps = [s.rstrip('\n') for s in steps]
        steps.reverse()
        for ts in steps:
            print(f'Running {sim}-00{ts}:')
            os.system(f'{pythonpath} Code/BaryonicFractionData.py -s {sim} -t {ts} -n 10')

else:
    for sim in ['cptmarvel','elektra','storm','rogue']:
        print(f'Running {sim}-004096:')
        os.system(f'{pythonpath} Code/Marvel.z0.py -s {sim} -n 10')