#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[1]:


## build deck


# In[2]:


ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['H', 'C', 'D', 'S']


# In[3]:


deck = []
for x in ranks:
    for y in suits:
        deck.append(f"{x}{y}")


# In[4]:


def shuffle(*args):
    a = deck.copy()
    for x in args:
        a.remove(x)
    return a


# In[2]:


## assign values to cards


# In[5]:


vals = {}
for x in deck:
    a = x[:-1]
    if a not in ['J', 'Q', 'K', 'A']:
        vals[x] = int(a)
    elif a == 'J':
        vals[x] = 11
    elif a == 'Q':
        vals[x] = 12
    elif a == 'K':
        vals[x] = 13
    else:
        vals[x] = [1,14]


# In[6]:


vals2 = {}
for x in ranks:
    if x not in ['J', 'Q', 'K', 'A']:
        vals2[x] = int(x)
    elif x == 'J':
        vals2[x] = 11
    elif x == 'Q':
        vals2[x] = 12
    elif x == 'K':
        vals2[x] = 13
    else:
        vals2[x] = [1,14]


# In[3]:


### build evaluating functions for each possible hand result


# In[7]:


def HighCard(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    return 1, sorted(value, reverse = True)


# In[8]:


def Pair(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    found = False
    pr = 0
    for x in value:
        foundpair = value.count(x)
        if foundpair > 1:
            found = True
            pr += x
            break
    if found == True:
        for i in range(2):
            value.remove(pr)
        return 2, pr, sorted(value, reverse = True)


# In[9]:


def TwoPair(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    found = False
    pr = []
    for x in value:
        foundpair = value.count(x)
        if (foundpair > 1) & (x not in pr):
            pr.append(x)
        elif (foundpair > 1) & (x not in pr) & (len(pr) > 0):
            pr.append(x)
    if len(pr) > 1:
        found = True
    if found == True:
        for i in range(2):
            for y in pr:
                value.remove(y)
        return 3, sorted(pr, reverse = True), sorted(value, reverse = True)


# In[10]:


def ThreeOAK(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    found = False
    pr = 0
    for x in value:
        foundpair = value.count(x)
        if foundpair == 3:
            pr += x
            found = True
            break
    if found == True:
        for i in range(3):
            value.remove(pr)
        return 4, pr, sorted(value, reverse = True)


# In[11]:


def Straight(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            if ('2' in hold) & ('3' in hold) & ('4' in hold):
                value.append(vals2[x][0])
            else:
                value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    sortval = sorted(value)
    straight = True
    for i in range(len(sortval) - 1):
        if sortval[i] + 1 != sortval[i+1]:
            straight = False
            break
    if straight == True:
        return 5, sorted(sortval, reverse = True)


# In[12]:


def Flush(hand):
    hold = []
    holds = []
    for x in hand:
        hold.append(x[:-1])
        holds.append(x[-1:])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    if len(set(holds)) == 1:
        return 6, sorted(value, reverse = True)


# In[13]:


def FullHouse(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    pair = False
    pr = 0
    toak = False
    tk = 0
    for x in value:
        found = value.count(x)
        if found == 2:
            pr += x
            pair = True
        elif found == 3:
            tk += x
            toak = True
    if (pair == True) and (toak == True):
        return 7, [int(tk/3), int(pr/2)]


# In[14]:


def FourOAK(hand):
    hold = []
    for x in hand:
        hold.append(x[:-1])
    value = []
    for x in hold:
        if x == 'A':
            value.append(vals2[x][1])
        else:
            value.append(vals2[x])
    foak = False
    fk = 0
    for x in value:
        found = value.count(x)
        if found == 4:
            fk += x
            foak = True
            break
    if foak == True:
        for i in range(4):
            value.remove(fk)
        return 8, fk, value[0]


# In[15]:


def StraightFlush(hand):
    st = Straight(hand)
    fl = Flush(hand)
    if (st != None) and (fl != None):
        return 9, st[1]


# In[16]:


def RoyalFlush(hand):
    sf = StraightFlush(hand)
    if sf != None:
        if (14 in sf[1]) & (13 in sf[1]):
            return 10, sf[1]


# In[4]:


### combine all evaluative functions into one singular result function


# In[17]:


def result(hand):
    functions = [RoyalFlush, StraightFlush, FourOAK, FullHouse, Flush, Straight, ThreeOAK, TwoPair, Pair, HighCard]
    res = []
    for func in functions:
        if func(hand) != None:
            res.append(func(hand))
            break
    return res[0]


# In[5]:


### evaluate all combinations


# In[19]:


from itertools import combinations
from itertools import permutations


# In[20]:


allhands = list(combinations(deck, 5))


# In[21]:


ah = []
for x in allhands:
    ah.append(sorted(list(x)))


# In[6]:


### dicitonary of hand result


# In[22]:


ahdic = {}


# In[23]:


for x in ah:
    r = result(x)
    ahdic[str(x)] = r


# In[24]:


df = pd.DataFrame(list(ahdic.values()))


# In[25]:


l = np.arange(1,11).tolist()


# In[7]:


### add results to pandas dataframe and sort columns to get hand rank


# In[26]:


newdf = []
for x in l:
    new = df[df[0] == x]
    try:
        new = new.sort_values([1,2])
    except TypeError:
        new = new.sort_values(1)
    newdf.append(new)


# In[27]:


newdf = pd.concat(newdf)


# In[28]:


masterlist = sorted(list(ahdic.values()))
vals = []
num = 0
for x in range(len(masterlist)):
    if masterlist[x] == masterlist[0]:
        num = 0
    elif masterlist[x] != masterlist[x-1]:
        num += 1
    vals.append(num)


# In[8]:


### dictionary of hand result rank among all possible results


# In[29]:


valdic = {}
for x in range(len(masterlist)):
    valdic[str(masterlist[x])] = vals[x]


# In[9]:


### side note (not relevant for this tool)
### evaluate player's best possible hand from 7 total cards


# In[30]:


def BestHand(*args):
    combos = list(combinations(args,5))
    co = []
    for x in combos:
        co.append(sorted(list(x)))
    vals = []
    for x in co:
        r = result(x)
        vals.append(valdic[str(r)])
    besthand = co[vals.index(max(vals))]
    val = max(vals)
    return besthand, val


# In[402]:


def SolveSeven(river):
    ss = BestHand(river[0], river[1], river[2], river[3], river[4], river[5], river[6])
    return ss[0], ss[1]


# In[10]:


### evaluate deal strength
### take all possible combinations of deals of 2, and create a dictinary with all remaining combinations of 3
### get the mean of all result ranks and that is the expected value of the deal


# In[37]:


deals = list(combinations(shuffle(),2))


# In[39]:


clas = []
va = []
ss = []
for x in deals:
    if x[0][0] == x[1][0]:
        clas.append(True)
        va.append(str(sorted([x[0][0], x[1][0]])))
    else:
        clas.append(False)
        va.append(str(sorted([x[0][0], x[1][0]])))
    if x[0][1] == x[1][1]:
        ss.append(True)
    else:
        ss.append(False)


# In[40]:


dealdf = pd.DataFrame({'Deal': deals, 'Pair': clas, 'Val': va, 'SS': ss})


# In[41]:


dealdf2 = dealdf.drop_duplicates(subset = ['Pair', 'Val', 'SS'])


# In[62]:


handdic = {}
for x in deals:
    xx = x[0]
    xxx = x[1]
    app = []
    for y in list(ahdic):
        if (xx in y) and (xxx in y):
            app.append(y)
    handdic[x] = app
    print(f"{int(len(handdic)*100/len(deals))}%", end = '\r')


# In[83]:


newvals = []
for x in handdic:
    meanval = []
    for y in handdic[x]:
        xx = str(y)
        rr = valdic[str(ahdic[xx])]
        meanval.append(rr)
    newvals.append(sum(meanval)/len(meanval))
    print(f"{list(handdic).index(x)} out of {len(list(handdic))}", end = '\r')


# In[90]:


dealvals = pd.DataFrame({'Deal': list(handdic), 'Value': newvals})


# In[121]:


dealvals['adjVal'] = ((dealvals['Value'] - dealvals['Value'].min()) / (dealvals['Value'].max() - dealvals['Value'].min()))


# In[148]:


vallist = sorted(dealvals['adjVal'].unique().tolist())


# In[151]:


handrank = []
number = 0
for x in vallist:
    handrank.append(number)
    number += 1


# In[154]:


newvaldf = pd.DataFrame({'adjVal': vallist, 'Rank': handrank})


# In[157]:


dealvals = dealvals.merge(newvaldf, on = 'adjVal', how = 'left')


# In[12]:


### build deal function
### account for players in the hand, the players yet to bet, the total pot, the amount to call, and the cards dealt to player and table


# In[314]:


def FindDeal(notyet, pot, bet, num, *args):
    a = args[0]
    b = args[1]
    new = dealvals[(dealvals['Deal'].astype(str).str.contains(a)) & (dealvals['Deal'].astype(str).str.contains(b))]['Rank'].iloc[0]
    nextval = new-1
    mx = dealvals['Rank'].max()
    med = int(dealvals['Rank'].mean())
    prob = (nextval/mx)**(num + .5*notyet)
    xpot = (bet*notyet)*.5
    if prob*(pot+xpot+bet) > bet:
        return 'Bet', prob
    else:
        return 'Fold', prob


# In[ ]:


### plug in values


# In[375]:


notyet = 2 ## number of players who haven't bet yet


# In[376]:


pot = 27 ## amount in the pot
bet = 12 ## amount to call


# In[ ]:


numplay = 5 ## number of players who have already bet or called


# In[381]:


card1 = '6D'
card2 = '3D'


# In[378]:


FindDeal(notyet, pot, bet, numplay, card1, card2)

