import pickle

erase = False
try:
    Data = pickle.load(open('BaryonicFractionData.pickle','rb'))
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
    out = open('BaryonicFractionData.pickle','wb')
    pickle.dump(Data,out)
    out.close()
    print('Empty Data file created.')