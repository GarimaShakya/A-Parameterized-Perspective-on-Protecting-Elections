#i input txt file
#output: show and save the plot

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from operator import add
from matplotlib.font_manager import FontProperties
font0 = FontProperties()
N = 9



### open the data file and loading the data
fWCO1 = open('ToPlotProfile=1000n=12000Groups=12Randomized4Generator4.txt', 'r')
for line in fWCO1.readlines():
    exec(line)
fWCO1.close()

Plurality=[[],[],[],[],[]]
veto=[[],[],[],[],[]]
borda=[[],[],[],[],[]]
#
for index in xrange(len(Plu_2_10)):
    Plurality[index].append(Plu_2_10[index])
    
for index in xrange(len(Plu_3_9)):
    Plurality[index].append(Plu_3_9[index])

for index in xrange(len(Plu_4_8)):
    Plurality[index].append(Plu_4_8[index])
    
for index in xrange(len(Plu_5_7)):
    Plurality[index].append(Plu_5_7[index])

for index in xrange(len(Plu_6_6)):
    Plurality[index].append(Plu_6_6[index])
#    
for index in xrange(len(Plu_7_5)):
    Plurality[index].append(Plu_7_5[index])
    
for index in xrange(len(Plu_8_4)):
    Plurality[index].append(Plu_8_4[index])
    
for index in xrange(len(Plu_9_3)):
    Plurality[index].append(Plu_9_3[index])

for index in xrange(len(Plu_10_2)):
    Plurality[index].append(Plu_10_2[index])

for index in xrange(len(vet_2_10)):
    veto[index].append(vet_2_10[index])
    
for index in xrange(len(vet_3_9)):
    veto[index].append(vet_3_9[index])

for index in xrange(len(vet_4_8)):
    veto[index].append(vet_4_8[index])
    
for index in xrange(len(vet_5_7)):
    veto[index].append(vet_5_7[index])

for index in xrange(len(vet_6_6)):
    veto[index].append(vet_6_6[index])

for index in xrange(len(vet_7_5)):
    veto[index].append(vet_7_5[index])    

for index in xrange(len(vet_8_4)):
    veto[index].append(vet_8_4[index])   

for index in xrange(len(vet_9_3)):
    veto[index].append(vet_9_3[index])    

for index in xrange(len(vet_10_2)):
    veto[index].append(vet_10_2[index])    


for index in xrange(len(bor_2_10)):
    borda[index].append(bor_2_10[index])
    
for index in xrange(len(bor_3_9)):
    borda[index].append(bor_3_9[index])
    
for index in xrange(len(bor_4_8)):
    borda[index].append(bor_4_8[index])

for index in xrange(len(bor_5_7)):
    borda[index].append(bor_5_7[index])
   
for index in xrange(len(bor_6_6)):
    borda[index].append(bor_6_6[index])

for index in xrange(len(bor_7_5)):
    borda[index].append(bor_7_5[index]) 

for index in xrange(len(bor_8_4)):
    borda[index].append(bor_8_4[index])   
    
for index in xrange(len(bor_9_3)):
    borda[index].append(bor_9_3[index])
#    
for index in xrange(len(bor_10_2)):
    borda[index].append(bor_10_2[index]) 
print Plurality, veto,borda




ind = np.arange(N)  # the x locations for the groups
width = 0.25    # the width of the bars
gap = 0.05

print ind


fig, ax = plt.subplots()
rects1 = ax.bar(ind + gap, Plurality[0], width, color='g')
rects2 = ax.bar(ind + width + 2*gap, veto[0], width, color='g')
rects3 = ax.bar(ind + width + width + 3*gap, borda[0], width, color='g')


rects4 = ax.bar(ind+gap, Plurality[1], width, color='b',bottom=Plurality[0], yerr=np.subtract(Plurality[3], Plurality[1]),ecolor='black')
rects5 = ax.bar(ind + width + 2*gap, veto[1], width, color='b', bottom=veto[0],yerr=np.subtract(veto[3], veto[1]),ecolor='black')
rects6 = ax.bar(ind + width + width + 3*gap, borda[1], width, color='b', bottom=borda[0], yerr=np.subtract(borda[3], borda[1]),ecolor='black')


rects7 = ax.bar(ind+gap, Plurality[2], width, color='r',bottom=list( map(add, Plurality[0], Plurality[1]) ) )
rects8 = ax.bar(ind + width + 2*gap, veto[2], width, color='r', bottom=list( map(add, veto[0], veto[1]) ))
rects9 = ax.bar(ind + width + width + 3*gap, borda[2], width, color='r', bottom=list( map(add, borda[0], borda[1]) ))





# add some text for labels, title and axes ticks
ax.set_ylabel('Voting profiles',fontsize=15, color='k')
ax.set_xlabel(r'$k_d$',fontsize=15, color='k')
#ax.set_title('',fontsize=25, color='k')
#ax.set_xticks(ind + width / 2)
plt.xticks(ind+width+2*gap+ width/2, ('2','3','4','5','6','7','8','9','10'))
plt.rcParams["figure.figsize"] = (9,5)


ax.legend( (rects1[0], rects4[0],rects7[0]), ('optimal and defended', 'optimal but not defended','not optimal'),fontsize=10,loc='lower right',fancybox=True, framealpha=0.8)
plt.ylim(0,1005)
#plt.xlim(0,len(ind)*width+5)

# # Add counts above the two bar graphs
#i=0
for rect in rects7 :
    height = 1005
    plt.text(rect.get_x() + 3*gap + rect.get_width()/2.0, height, 'Plurality', ha='center', va='bottom',rotation=45)

    

for rect in rects8:
    height = 1005
    plt.text(rect.get_x() + 2*gap+ rect.get_width()/2.0, height, 'Veto', ha='center', va='bottom',rotation=45)


for rect in rects9:
    height = 1005
    plt.text(rect.get_x() + 2*gap+ rect.get_width()/2.0, height, 'Borda', ha='center', va='bottom',rotation=45)

plt.grid(True)
plt.savefig('ToPlotProfile=1000n=12000Groups=12Randomized5Generator4(1).pdf')
plt.show()

for i in range (0,len(Plurality[4])):
    if(Plurality[2][i]!=0):
        Plurality[4][i]=float(Plurality[4][i])/Plurality[2][i]
    if(veto[2][i]!=0):
        veto[4][i]=float(veto[4][i])/veto[2][i]
    if(borda[2][i]!=0):
        borda[4][i]=float(borda[4][i])/borda[2][i]


fig2, ax2 = plt.subplots()
rects1 = ax2.bar(ind + gap, Plurality[4], width, color='g')
rects2 = ax2.bar(ind + width + 2*gap, veto[4], width, color='g')
rects3 = ax2.bar(ind + width + width + 3*gap, borda[4], width, color='g')

ax2.set_ylabel('Voting profiles',fontsize=15, color='k')
ax2.set_xlabel(r'$k_d$',fontsize=15, color='k')
#ax.set_title('',fontsize=25, color='k')
#ax.set_xticks(ind + width / 2)
plt.xticks(ind+width+2*gap+ width/2, ('2','3','4','5','6','7','8','9','10'))
plt.rcParams["figure.figsize"] = (9,5)
ax2.legend( (rects1[0], rects2[0],rects3[0]), ('Plurality', 'Veto','Borda'),fontsize=10,loc='lower right',fancybox=True, framealpha=0.8)
plt.ylim(0,1)


plt.grid(True)
plt.savefig('ToPlotProfile=1000n=12000Groups=12Randomized5Generator4(2).pdf')
plt.show()
