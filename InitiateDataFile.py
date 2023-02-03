import argparse,pickle
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",choices=['Marvel','Romulus','z0','DCJL'],required=True)
args = parser.parse_args()

erase = False

if args.simulation=='Marvel':
    try:
        Data = pickle.load(open('DataFiles/BaryonicFractionData.pickle','rb'))
        contents = False
        for s in ['cptmarvel','elektra','storm','rogue']:
            if Data[s]:
                contents = True
        if contents:
            cont = input('Data File has contents. Erase and continue? y/n: ')
        if cont == 'y' or cont == 'yes': erase = True
    except:
        erase = True

    if erase:
        Data={}
        for s in ['cptmarvel','elektra','storm','rogue']:
            Data[s] = {}
        out = open('DataFiles/BaryonicFractionData.pickle','wb')
        pickle.dump(Data,out)
        out.close()
        print('Empty Data file created.')

elif args.simulation=='z0':
    try:
        Data = pickle.load(open('DataFiles/Marvel.z0.pickle','rb'))
        contents = False
        for s in ['cptmarvel','elektra','storm','rogue']:
            if Data[s]:
                contents = True
        if contents:
            cont  = input('Data File has contents. Erase and continue? y/n: ')
        if cont == 'y' or cont == 'yes': erase = True
    except:
        erase = True

    if erase:
        Data={}
        for s in ['cptmarvel','elektra','storm','rogue']:
            Data[s] = {}
        out = open('DataFiles/Marvel.z0.pickle','wb')
        pickle.dump(Data,out)
        out.close()
        print('Empty Data file created.')

elif args.simulation=='DCJL':
    try:
        Data = pickle.load(open('DataFiles/DCJL.z0.pickle','rb'))
        contents = False
        for s in ['h148','h229','h242','h329']:
            if Data[s]:
                contents = True
        if contents:
            cont  = input('Data File has contents. Erase and continue? y/n: ')
        if cont == 'y' or cont == 'yes': erase = True
    except:
        erase = True

    if erase:
        Data={}
        for s in ['h148','h229','h242','h329']:
            Data[s] = {}
        out = open('DataFiles/DCJL.z0.pickle','wb')
        pickle.dump(Data,out)
        out.close()
        print('Empty Data file created.')

else:
    try:
        Data = pickle.load(open('DataFiles/RomulusData.pickle','rb'))
        cont = input('Data File exists. Erase and continue? y/n: ')
        if cont == 'y' or cont == 'yes': erase = True
    except:
        erase=True
    if erase:
        Data={'field':{'dwarf':{},'udg':{}},
                'satellite':{'dwarf':{},'udg':{}},
                'cluster':{'dwarf':{},'udg':{}}}
        with open('textfiles/Rom25_IsoDwarf.txt') as f:
            fdwf = f.readlines()
            fdwf = [int(l) for l in fdwf]
            for h in fdwf:
                Data['field']['dwarf'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        with open('textfiles/Rom25_IsoUDG.txt') as f:
            fudg = f.readlines()
            fudg = [int(l) for l in fudg]
            for h in fudg:
                Data['field']['udg'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        with open('textfiles/Rom25_SatDwarf.txt') as f:
            sdwf = f.readlines()
            sdwf = [int(l) for l in sdwf]
            for h in sdwf:
                Data['satellite']['dwarf'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        with open('textfiles/Rom25_SatUDG.txt') as f:
            sudg = f.readlines()
            sudg = [int(l) for l in sudg]
            for h in sudg:
                Data['satellite']['udg'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        with open('textfiles/RomC_Dwarf.txt') as f:
            cdwf = f.readlines()
            cdwf = [int(l) for l in cdwf]
            for h in cdwf:
                Data['cluster']['dwarf'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        with open('textfiles/RomC_UDG.txt') as f:
            cudg = f.readlines()
            cudg = [int(l) for l in cudg]
            for h in cudg:
                Data['cluster']['udg'][str(h)] = {'Mvir':np.nan,'Mgas':np.nan,'Mstar':np.nan,'Rvir':np.nan,
                                'Mvir_Inner':np.nan,'Mgas_Inner':np.nan,'Mstar_Inner':np.nan }
        out = open('DataFiles/RomulusData.pickle','wb')
        pickle.dump(Data,out)
        out.close()
        print('Empty Data file created.')