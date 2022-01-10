import argparse,pickle,xlrd
import numpy as np
import matplotlib.pylab as plt
from osxmetadata import OSXMetaData
res_halos = {
    'cptmarvel' :  [1,2,3,5,6,7,10,11,13,14,24],
    'elektra' : [1,2,3,4,5,8,9,10,11,12,17,36,64],
    'storm' : [1,2,3,4,5,6,7,8,10,11,12,14,15,22,23,31,37,44,48,55,118],
    'rogue' : [1,3,7,8,10,11,12,15,16,17,28,31,37,58,116]
}
parser = argparse.ArgumentParser()
parser.add_argument("-r","--resolved",action="store_true")
parser.add_argument("-d","--dyn",action="store_true")
args = parser.parse_args()

res = '.Resolved' if args.resolved else ''
skip_res = False if args.resolved else True

Data = pickle.load(open('../DataFiles/Marvel.z0.pickle','rb'))
ObsPlots = {'dark':[],'luminous':[]}

sims = ['cptmarvel','elektra','storm','rogue']
for s in sims:
    for h in Data[s]:
        if skip_res or (int(h) in res_halos[s]):
            halo = Data[s][h]
            if halo['Mstar']>0:
                ObsPlots['luminous'].append(float((.6*halo['Mstar']+1.33*halo['MHI'])/halo['Mvir']))

wkbk = xlrd.open_workbook('../PaperData.xls')

#Sheet 1
sheet1 = []
s1 = wkbk.sheet_by_name('Sheet1')
line = 1
while line < 1716:
    if args.dyn:
        sheet1.append((.6*s1.cell_value(line,0)*10**9+1.33*s1.cell_value(line,2)*10**9)/s1.cell_value(line,7))
    else:
        sheet1.append((.6*s1.cell_value(line,0)*10**9+1.33*s1.cell_value(line,2)*10**9)/s1.cell_value(line,8))
    line+=1

#Sheet 2
sheet2 = []
s2 = wkbk.sheet_by_name('Sheet2')
line = 1
while line < 116:
    if args.dyn:
        sheet2.append((.6*s2.cell_value(line,10)+1.33*10**s2.cell_value(line,0))/s2.cell_value(line,6))
    else:
        sheet2.append((.6*s2.cell_value(line,10)+1.33*10**s2.cell_value(line,0))/s2.cell_value(line,7))
    line+=1

#Sheet 3
sheet3 = []
s3 = wkbk.sheet_by_name('Sheet3')
line = 1
while line < 12:
    if args.dyn:
        sheet3.append((.6*10**s3.cell_value(line,0)+1.33*10**s3.cell_value(line,2))/s3.cell_value(line,8))
    else:
        sheet3.append((.6*10**s3.cell_value(line,0)+1.33*10**s3.cell_value(line,2))/s3.cell_value(line,9))
    line+=1

#Sheet 4
sheet4 = []
s4 = wkbk.sheet_by_name('Sheet4')
line = 1
while line < 11:
    sheet4.append((.6*10**s4.cell_value(line,0)+1.33*10**s4.cell_value(line,2))/(10**s4.cell_value(line,5)))
    line+=1

#Sheet 5
sheet5 = []
s5 = wkbk.sheet_by_name('Sheet5')
line = 1
while line < 27:
    if s5.cell_value(line,1)!='':
        sheet5.append(((.6*s5.cell_value(line,1))*10**7+1.33*10**s5.cell_value(line,3))/(10**s5.cell_value(line,4)))
    line+=1

#Sheet 6
sheet6 = []
s6 = wkbk.sheet_by_name('Sheet6')
line = 2
while line < 66:
    if s6.cell_value(line,3)!='' and s6.cell_value(line,4)!='':
        if args.dyn:
            sheet6.append((.6*float(s6.cell_value(line,3))*10**6+1.33*float(s6.cell_value(line,4))*10**6)/s6.cell_value(line,8))
        else:
            sheet6.append((.6*float(s6.cell_value(line,3))*10**6+1.33*float(s6.cell_value(line,4))*10**6)/s6.cell_value(line,9))
    line+=1

#Sheet 7
sheet7 = []
s7 = wkbk.sheet_by_name('Sheet7')
line = 1
while line < 12:
    if args.dyn:
        sheet5.append((.6*10**s7.cell_value(line,2)+1.33*10**s7.cell_value(line,3))/s7.cell_value(line,6))
    else:
        sheet5.append((.6*10**s7.cell_value(line,2)+1.33*10**s7.cell_value(line,3))/s7.cell_value(line,6))
    line+=1


f,ax = plt.subplots(1,1,figsize=(11,8))
ax.set_ylabel('N',fontsize=25)
ax.set_xlabel(r'Observed f$_{b}$ within '+r'R$_{vir}$',fontsize=25)
ax.tick_params(length=5,labelsize=15)
ax.set_xlim([1e-7,1])
ax.semilogx()
ax.set_ylim([6e-1,2e3])
ax.semilogy()
bins = np.logspace(-7,1,80)
ax.hist(ObsPlots['luminous'],bins,histtype='step',color='k',linewidth=3,label='MARVEL')
ax.hist(sheet1,bins,histtype='step',color='blue',linewidth=3,label='SDSS')
ax.hist(sheet2,bins,histtype='step',color='red',linewidth=3,label='ALFALFA')
ax.hist(sheet3,bins,histtype='step',color='green',linewidth=3,label='VLA HUDS')
ax.hist(sheet4,bins,histtype='step',color='orange',linewidth=3,label='MATLAS')
ax.hist(sheet5,bins,histtype='step',color='purple',linewidth=3,label='Little Things')
ax.hist(sheet6,bins,histtype='step',color='pink',linewidth=3,label='FIGGS')
ax.hist(sheet6,bins,histtype='step',color='cyan',linewidth=3,label='SHIELD')
ax.legend(loc='upper left',prop={'size':15})
f.savefig(f'../Plots/PaperComparison.png',bbox_inches='tight',pad_inches=.1)
meta = OSXMetaData(f'../Plots/TEST.png')
meta.creator='PaperComparisons.py'
plt.close()