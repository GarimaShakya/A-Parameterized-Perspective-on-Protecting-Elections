# Each Profile is: A collection of groups(or Classes, a collection of voters in a county) contains 40% of the votes where any candidate 'a' is preferred most and 
# 40% have any other candidate 'b' on top. Remaining 20% votes are generated uniformally randomly over the set of all possible preference order over set of candidates.

# Defence policy: for each of the losing candidates,a:
#                    sort the groups with descending order of winning margin
#                    and find the front kd number of groups for the pair (winner, a)
#                for each group,g:
#                    find the frequency of g in find the front kd number of groups for pair (winner, a) forall a 
#                pick the most frequent kd groups as groups should be defended
#                
# Attack policy: for each of the losing candidates,a:
#                    sort the groups with descending order of winning margin
#                    and find the front ka number of groups for the pair (winner, a)
#                    check: attacking those ka groups will change the outcome?
#                    if yes: take these groups as the groups should be attacked.:
#                        no: continue
#                if the above for loop do not give a set of groups, then the set of attacked groups is empty.

# Checking for optimality: If greedy fails:
#                                if attack is always possible for each of the possible kd groups:
#                                    'attack is always possible for this profile. \n  '
#                                    greedy is optimal
#                                else:
#                                    greedy is not optimal
#                          else:
#                                greedy is optimal
#
# Parallel Processing over the iterations


import numpy as np
import itertools
import math
import random
from itertools import permutations
from joblib import Parallel, delayed
import multiprocessing




noOfIterations=1000
n = 12000 #number of total voters
ListOfGroups=[]
Groups = 12 #number of groups
votingRuleList = ['plurality', 'veto','borda'] #
RuleList=['Plu','vet','bor'] # 
ResultForEachProfile=[[]*noOfIterations]

kaAll= [10,9,8,7,6,5,4,3,2]
kdAll= [2,3,4,5,6,7,8,9,10]
#kaAll= [18,16,14,12,10,8,6,4,2]
#kdAll= [2,4,6,8,10,12,14,16,18]
FinalResult=[]

profile= []
m = 5  #number of candidates
scores=[]   #scoring vector representing the scoring rule

final_scores=[]  #list of scores of candidates in overall population 
RandomRed=0
RandomGreen=0

candidates=[]  

scores_in_Groups=[]  #list of scores of candidates in groups of voters 
winningMargin_in_Groups=[]  #list of margin between the winner and runner in different groups

sortedGroupsWinnningMargin=[]  #sorted list of group with decrease in winning margin

defendedGroups=[]
attackedGroups=[]

newFinal_scores=[]          #after attack

timesDefended=0             #number of times the winner is same
timesNotDefended=0
timesAtackedGroupsChanged=0  #number of times the attacker takes any losing candidates other than the second winner to change the winner
timesGreedyIsNotOptimal=0
timesGreedyIsOptimal=0
RandomTimesdefended=0
RandomTimesNotdefended=0

for i in range(0,Groups):
    ListOfGroups.append(i)
    
#----------------------initialization--------------------
 
for i in range(0,Groups):
    winningMargin_in_Groups.append([0] * m);
    
for i in range(0,Groups):
    sortedGroupsWinnningMargin.append([0] * m);
    
for i in range(0,m):
    newFinal_scores.append(0)
    
newScores_in_Groups=[]
for i in range(0,Groups):
    newScores_in_Groups.append([0] * m);
    
for i in range(0,Groups):
    scores_in_Groups.append([0] * m);
    
for i in range(0,Groups):
    winningMargin_in_Groups.append(0);
    
for i in range(0,m):
    final_scores.append(0)



#-----------------functions---------------------------------------------------------------------------------#

def get_scoringVector(votingRule):  #scoring rule
#    
    if votingRule == 'plurality':
        for k in range(0,m): #plurality
            if (k==0):
                scores.append(1)
            else:
                scores.append(0)
                
    if votingRule == 'borda':
        for k in range(0,m):
            scores.append(m-1-k)
#            
    if votingRule == 'veto':
        for k in range(0,m):
            if k==m-1:
                scores.append(0)
            else:
                scores.append(1)
                
    return scores


def generate_profile():
    profile=[]
    perm = []
    candidates=[]
    if(m==3):
        A=['a','b','c']
        perm = list(permutations(A))
    if(m==5):
        A=['a','b','c','d','e']
        perm = list(permutations(A))
    if(m==9):
        A=['a','b','c','d','e','f','g','h','i']
        perm = list(permutations(A))

    for k in range(0,m):
        candidates.append(A[k])
    
    for k in range(0,Groups): #------------------for different groups
        temp_profile=[]
        
        for i in range(0,int((0.2)*n/Groups)):
            j = int(random.uniform(0,math.factorial(m)))
            temp_profile.append(list(perm[j]))
            
        for i in range(0,int((0.4)*n/Groups)):
            j = int(random.uniform(0,math.factorial(m-1)))
            temp_profile.append(list(perm[j]))
            
        for i in range(0,int((0.4)*n/Groups)):
            j = int(random.uniform(math.factorial(m-1),math.factorial(m-1)+math.factorial(m-1)))
            temp_profile.append(list(perm[j]))
            
        profile.append(temp_profile)
    return candidates, profile
        

            
def get_scoresAndWinner(profile, candidates, scores):  #to get winner, second_winner, final_scores, scores_in_Groups
    final_scores=[]
    for i in range(0,m):
        final_scores.append(0)
    scores_in_Groups=[]
    for i in range(0,Groups):
        scores_in_Groups.append([0] * m);  
        
    for k in range(0,Groups):            
        for j in range(0,m):
            for l in range(0,n/Groups):
                index= profile[k][l].index(chr(ord(candidates[j])))
                temp_score=scores[index]
                scores_in_Groups[k][j]=scores_in_Groups[k][j]+temp_score
                final_scores[j]=final_scores[j]+temp_score
    temp_winner=0
    highest_score=0
    
    for j in range(0,m):
        if(final_scores[j]> highest_score):
            highest_score = final_scores[j]
            temp_winner_index=j
            temp_winner = candidates[j]
    winner_index=temp_winner_index
    winner=temp_winner
    second_score=0
    
    for j in range(0,m):
        if(winner_index==j):
            continue
        else:
            if(final_scores[j]> second_score):
                second_score = final_scores[j]
                second_winner = candidates[j]    
    return winner, second_winner, final_scores, scores_in_Groups
        
    

def WinningMargin(A,B,candidates, scores_in_Groups):  # to get winningMargin_in_Groups, sortedGroupsWinnningMargin
    winningMargin_in_GroupsAB=[]
    for i in range(0,Groups):
        winningMargin_in_GroupsAB.append(0);
    sortedGroupsWinnningMarginAB=[]    
    for k in range(0,Groups):
        indexOfA=candidates.index(chr(ord(A)))
        indexOfB=candidates.index(chr(ord(B)))
        margin=scores_in_Groups[k][indexOfA]-scores_in_Groups[k][indexOfB]
        winningMargin_in_GroupsAB[k]=winningMargin_in_GroupsAB[k] + margin
    for k in range(0,Groups):
        temp_margin=(-1)*n         
        for l in range(0,Groups):
            if l in sortedGroupsWinnningMarginAB:            
                continue
            else:
                if(winningMargin_in_GroupsAB[l] > temp_margin):
                    temp_margin=winningMargin_in_GroupsAB[l]
                    temp_group=l
        sortedGroupsWinnningMarginAB.append(temp_group)
    return winningMargin_in_GroupsAB, sortedGroupsWinnningMarginAB
            
           

def chooseGroupsDefenders(kd,winningMargin_in_Groups, sortedGroupsWinnningMargin, candidates, winner): 
    defendedGroups=[]
    frequencyOfGroups=[0]*Groups
    sortedGroupsByFrequency=[]
    for i in range(0,len(candidates)):
        defendedGroupsForI=[]
        if (candidates[i]!=winner):            
            for k in range(0, kd):
                if winningMargin_in_Groups[i][sortedGroupsWinnningMargin[i][k]] >= 0:
                    defendedGroupsForI.append(sortedGroupsWinnningMargin[i][k])
                    frequencyOfGroups[sortedGroupsWinnningMargin[i][k]]=frequencyOfGroups[sortedGroupsWinnningMargin[i][k]]+1
                else:
                    break
        else:
            defendedGroupsForI=[-1]*kd  # -1 is for the winner
#        print 'defendedGroupsFor ' + str(i) + ' is '+str(defendedGroupsForI) +'\n'
#    print 'frequencyOfGroups: ' + str(frequencyOfGroups) +'\n\n'
    for k in range(0,Groups):
        tempGroup=-1 
        tempFrequency=-1
        for l in range(0,Groups):
            if l in sortedGroupsByFrequency:            
                continue
            else:
                if(frequencyOfGroups[l] > tempFrequency):
                    tempGroup=l
                    tempFrequency=frequencyOfGroups[l]
        sortedGroupsByFrequency.append(tempGroup)
#    print 'sortedGroupsByFrequency ' +str(sortedGroupsByFrequency)
    for k in range(0, kd):
        defendedGroups.append(sortedGroupsByFrequency[k])
    return defendedGroups



def defendersJob(kd,winningMargin_in_Groups, sortedGroupsWinnningMargin, candidates, winner):
    defendedGroups = chooseGroupsDefenders(kd,winningMargin_in_Groups, sortedGroupsWinnningMargin, candidates, winner);
    return defendedGroups



def chooseGroupsAttackers(ka,winningMargin_in_Groups, sortedGroupsWinnningMargin, defendedGroups):
    temp_ka= ka
    attackedGroups_Ab=[]
    for l in range(0, Groups):
        if temp_ka > 0 :
            if winningMargin_in_Groups[sortedGroupsWinnningMargin[l]] >= 0 and sortedGroupsWinnningMargin[l] not in defendedGroups:
                attackedGroups_Ab.append(sortedGroupsWinnningMargin[l])
                temp_ka=temp_ka -1
        else:
            break
    return attackedGroups_Ab
    
    
def attackersJob(ka, defendedGroups, A, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged):
    attackedGroups=[]
    winningMargin_in_GroupsAB, sortedGroupsWinnningMarginAB = WinningMargin(A, second_winner, candidates, scores_in_Groups)
    attackedGroups= chooseGroupsAttackers(ka,winningMargin_in_GroupsAB, sortedGroupsWinnningMarginAB, defendedGroups);
    newWinnerAorB, newSecondWinnerAorB, newFinal_scores, newScores_in_Groups= getNewWinner(candidates, profile, attackedGroups, scores)
    
    if(newWinnerAorB != A):
            return attackedGroups, timesAtackedGroupsChanged
    else:  
        for i in range(0,len(candidates)):    
            B=candidates[i]
            if(B != A and B!= second_winner):
                winningMargin_in_GroupsAB, sortedGroupsWinnningMarginAB = WinningMargin(A,B,candidates, scores_in_Groups)
                attackedGroups_AB= chooseGroupsAttackers(ka,winningMargin_in_GroupsAB, sortedGroupsWinnningMarginAB, defendedGroups);
                newWinnerAorB, newSecondWinnerAorB, newFinal_scores, newScores_in_Groups= getNewWinner(candidates, profile, attackedGroups_AB, scores)
                if(newWinnerAorB != A):
                    attackedGroups=attackedGroups_AB
                    timesAtackedGroupsChanged=timesAtackedGroupsChanged+1
                    break
                else:
                    continue       
    return attackedGroups, timesAtackedGroupsChanged
    
    
    
def getNewWinner(candidates, profile, attackedGroups, scores):  #winner after defense and attack
    newFinal_scores=[]
    for i in range(0,m):
        newFinal_scores.append(0) 
    newScores_in_Groups=[]
    for i in range(0,Groups):
        newScores_in_Groups.append([0] * m);
        
    for k in range(0,Groups): 
        if k not in attackedGroups:
            for j in range(0,m):
                for l in range(0,n/Groups):
                    index= profile[k][l].index(chr(ord(candidates[j])))
                    temp_score=scores[index]
                    newScores_in_Groups[k][j]=newScores_in_Groups[k][j]+temp_score
                    newFinal_scores[j]=newFinal_scores[j]+temp_score
    temp_winner=0
    newHighest_score=0
    temp_winner_index =-1
    for j in range(0,m):
        if(newFinal_scores[j] > newHighest_score):
            newHighest_score = newFinal_scores[j]
            temp_winner_index=j
            temp_winner = candidates[j]
    newWinner_index=temp_winner_index
    newWinner=temp_winner
    
    newSecond_score=0
    for j in range(0,m):
        if(newWinner_index==j):
            continue
        else:
            if(newFinal_scores[j]> newSecond_score):
                newSecond_score = newFinal_scores[j]
                newSecond_winner = candidates[j]
        
    return newWinner, newSecond_winner, newFinal_scores, newScores_in_Groups


def checkOptimality(ka,GroupsChooseKd, winner, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged):
    flag = 'no'
#    print 'checking for optimality . . .'
    for i in range(0,len(GroupsChooseKd)):
        
        attackedGroups, timesAtackedGroupsChanged =attackersJob( ka,GroupsChooseKd[i], winner, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged);
        newWinner, newSecond_winner, newFinal_scores, newScores_in_Groups = getNewWinner(candidates, profile, attackedGroups, scores); #give the new first and second winner using scoring rule
        if (winner!=newWinner):
            flag = 'Yes'
        else:
            flag = 'no'
            return flag, i
    return flag, len(GroupsChooseKd)        
#    print 'winner is same\n\n\n'
            
#    print 'ka is: '+ str(ka) + '  attackedGroups  ' + str(attackedGroups) 

    
#-----------------------------------------------------------------------------main instructions---------------------   
    
    
def iterations(votingRule,kd,ka,profile,candidates,scores,Defended, timesAtackedGroupsChanged, GreedyIsOptimal,RandomRed,RandomGreen):
    
    for i in range(0,Groups):
        winningMargin_in_Groups.append([0] * m);
    for i in range(0,Groups):
        sortedGroupsWinnningMargin.append([0] * m);
   
    
    
    winner, second_winner, final_scores, scores_in_Groups = get_scoresAndWinner(profile, candidates, scores); #give first and second winner using score vector
    #print 'winner is ' + str(winner) + '\n'
    for x in range(0,m): #to calculate the winning margin between winner and every other candidate
        if(candidates[x]!=winner):
            winningMargin_in_Groups[x], sortedGroupsWinnningMargin[x] = WinningMargin(winner,candidates[x], candidates, scores_in_Groups);
        else:
            winningMargin_in_Groups[x] = [0]*Groups
            sortedGroupsWinnningMargin[x] = [0]*Groups 
       
    defendedGroups= defendersJob(kd,winningMargin_in_Groups, sortedGroupsWinnningMargin, candidates,winner);
    print 'kd is: ' + str(kd) + '  defendedGroups  ' + str(defendedGroups) 
    
    attackedGroups, timesAtackedGroupsChanged =attackersJob(ka, defendedGroups, winner, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged);
    print 'ka is: '+ str(ka) + '  attackedGroups  ' + str(attackedGroups) 
    
    newWinner, newSecond_winner, newFinal_scores, newScores_in_Groups = getNewWinner(candidates, profile, attackedGroups, scores); #give the new first and second winner using scoring rule
#
#    print 'winner was '+str(winner)
#    print 'second winner was ' + str (second_winner)
#    print 'new winner is '+str(newWinner)
#    print 'new second winner is ' + str (newSecond_winner)    

    if(winner!=newWinner):
        Defended = 0      
        GroupsChooseKd=[]
        for subset in itertools.combinations(ListOfGroups, kd):
            GroupsChooseKd.append(list(subset))
        flag, i = checkOptimality(ka,GroupsChooseKd, winner, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged);
        if(flag=='no'):
#            print 'no attack possible if the defended groups are:  ' + str(GroupsChooseKd[i]) + '\n'
            GreedyIsOptimal=0

            for i in range(0,100):
                TryKd=np.random.choice(Groups, kd, replace=False)
                attackedGroups, notNeeded = attackersJob(ka, TryKd, winner, second_winner, profile, candidates, scores_in_Groups, timesAtackedGroupsChanged);  
                newTempWinner, newTempSecond_winner, newTempFinal_scores, newTempScores_in_Groups = getNewWinner(candidates, profile, attackedGroups, scores); 
                if(winner!=newTempWinner):
                    RandomRed=RandomRed+1   
                    
                else:
                    RandomGreen=RandomGreen+1
            
        else:
#            print 'attack is always possible for this profile. \n  '
            GreedyIsOptimal= 1
    else:
        GreedyIsOptimal= 1
#        print 'greedy is optimal \n'
        Defended=1
    toReturn=[Defended, 1-Defended, timesAtackedGroupsChanged, GreedyIsOptimal, 1-GreedyIsOptimal ,float(RandomRed)/100,float(RandomGreen)/100]
    return toReturn
    
def forNoOfProfiles():
    datafile=open('data_Profile='+str(1000)+'n='+str(n)+'Groups='+str(Groups)+'.csv', 'a')
    datafile.write('[')
    candidates, profile = generate_profile();
    tempList1=[]
    for k in range(0,len(votingRuleList)):
        
        votingRule=votingRuleList[k]
        Rule=RuleList[k]
        scores=get_scoringVector(votingRule)
        for j in range(0,len(kaAll)):
            
            kd=kdAll[j]
            ka=kaAll[j]
#            print 'ka is:' + str(ka) + '\n'
#            print 'kd is:' + str(kd) + '\n'
            tempList2=[Rule,kd]
            Defended=-1
            timesAtackedGroupsChanged=0
            GreedyIsOptimal= -1
            RandomRed=0
            RandomGreen=0
            Result2=iterations(votingRule,kd,ka,profile,candidates,scores,Defended, timesAtackedGroupsChanged, GreedyIsOptimal,RandomRed,RandomGreen)
            if(Result2[0]!=1):
                tempList2.append(0)
            else:
                tempList2.append(1)
            if(Result2[3]==1):
                tempList2.append(1)
            else:
                tempList2.append(0)   
            tempList2.append(Result2[5])
            tempList2.append(Result2[6])
            datafile.write( '(' +str(Rule)+ ',' +str(kd)+',' +str(tempList2[2]) + ',' + str(tempList2[3])+ ',' + str(round(Result2[6],2)) +'),' )
            tempList1.append(tempList2)
    toReturn2=tempList1    
    datafile.write('],' +str(profile))
    datafile.write('\n\n')
#    toReturn2=[tempList1,profile]           
    return toReturn2         

    
if __name__ == '__main__':
    
    
    fileName = 'ToPlot'+'Profile='+str(1000)+'n='+str(n)+'Groups='+str(Groups)+'Randomized4.txt'
    f = open(fileName, 'w')
    f.close()
    datafile=open('data_Profile='+str(1000)+'n='+str(n)+'Groups='+str(Groups)+'Randomized4.csv', 'w')
    datafile.write('Profile(Id),[votingRule,kd,DefendedOrNot,GreedyIsOptimalOrNot, RandomGreen],proflie in form of groups \n\n')
    datafile.close()
    num_cores = multiprocessing.cpu_count()
    print 'number of cores:  '+str(num_cores)


#    
#    for i in range(0,noOfIterations):
#        candidates, profile = generate_profile();
#        results  = forNoOfProfiles(candidates,profile)
    
    results = Parallel(n_jobs=num_cores-2)(delayed(forNoOfProfiles)() for i in range(0,noOfIterations))
#    print results

#    for j in range(0, len(votingRuleList)):
#        print votingRuleList[j]
#        for k in range(0,len(kdAll)):
#            timesDefended=0
#            timesGreedyIsOptimal=0
#            RandomRed=0
#            RandomGreen=0
    for l in range(0,len(votingRuleList)):
        votingRule=RuleList[l]
        
        for p in range(0,len(kdAll)):
            kd=kdAll[p]
            ka=kaAll[p]
            timesDefended=0
            timesGreedyIsOptimal=0
            RandomRed=0
            RandomGreen=0
            for i in range(0,noOfIterations):
#                print results[i]
                tempList1=results[i]

                for j in range(0, len(tempList1)):
#                    print tempList1[j]
                    if(tempList1[j][0]==votingRule and tempList1[j][1]==kd):
#                        print 'mathched ---'
                        timesDefended=timesDefended+tempList1[j][2]
        #                timesNotDefended=timesNotDefended+results[i][1]
        #                timesAtackedGroupsChanged=timesAtackedGroupsChanged+results[i][2]
        #                timesGreedyIsNotOptimal=timesGreedyIsNotOptimal+results[i][3]
                        timesGreedyIsOptimal=timesGreedyIsOptimal+tempList1[j][3]
                        RandomRed=RandomRed + tempList1[j][4]
                        RandomGreen=RandomGreen + tempList1[j][5]
            FinalResult.append([votingRule,kd,ka,timesDefended, timesGreedyIsOptimal, timesGreedyIsOptimal-timesDefended, round(RandomRed,2), round(RandomGreen,2) ])
#    print FinalResult      
    
    
    fh = open(fileName, 'a')
    for i in range(0,len(FinalResult)):
        TempFinalResult=FinalResult[i]
        print TempFinalResult
        fh.write(str(TempFinalResult[0]) + '_'+str(TempFinalResult[1])+'_'+str(TempFinalResult[2])+ '= [' +str(TempFinalResult[3]) + ' , ' + str(TempFinalResult[5]) + ' , ' + str(noOfIterations-TempFinalResult[4]) + ' , ' + str(TempFinalResult[6]) + ' , ' + str(TempFinalResult[7]) +' ]\n')
        print str(TempFinalResult[0]) + '_'+str(TempFinalResult[1])+'_'+str(TempFinalResult[2])+ '= [' +str(TempFinalResult[3]) + ' , ' + str(TempFinalResult[5]) + ' , ' + str(noOfIterations-TempFinalResult[4]) + ' , ' + str(TempFinalResult[6]) + ' , ' + str(TempFinalResult[7]) +' ]\n'
    fh.close()   


