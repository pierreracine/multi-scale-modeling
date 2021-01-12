# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:55:32 2020
@author: Pierre
"""

# This programm has been made to simulate the propagation of the COVID-19 pandemic throught time.
# We use a compartmental model.
# The compartments used are healthy (H), rpesymptomatic (P), asymptomatically infected (AI),
# symptomatically infected (SI), cured (C), severe (S) and dead (D)
# We suppose that the induced immunity is 100%.
# The goal of this script is to optimize the impact of lockdown, based on data available about
# the number of total death.

"""Classical imports"""

import matplotlib.pyplot as plt
from scipy import interpolate


"""Parameters list"""

beta=0.421
t=0.15/5
x=0.85/5
y=1/10
z=0.92/7
u=0.08/7
v=0.7/15
w=0.3/15
v_no_icu=0.4/15
w_no_icu=0.6/15
max_capacity=14000
data_deaths=[1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,4,4,7,9,16,19,30,33,48,61,79,91,127,148,175,264,372,450,562,674,860,1100,1331,1696,1995,2314,2606,3024,3522,4030,5384,6503,7555,8072,8904,10320,10860,12199,13185,13819,14380,14954,15715,17152,17904,18664,19305,19700,20246,20776,21319,21834,22223,22592,22834,23270,23637,24063,24352,24570,24736,24871,25177,25507,25785,25963,26206,26286,26356,26619,26967,27050,27401,27505,27601,28083,28214,27997,28107,28190,28264,28307,28342,28407,28505,28571,28637,28689,28746,28777,28808,28915,28996,29040,29086,29117,29130,29184,29271,29294,29321,29349,29373,29382,29411,29522,29550,29578,29592,29608,29615,29638,29695,29706,29727,29753,29761,29770,29788,29818,29836,29850,29868,29875,29882,29895,29908,29940,29954,29979,29983,29986,30004,30075,30095,30113,30127,30136,30144,30152,30165,30172,30182,30192,30196,30200,30209,30223,30238,30254,30265,30268,30272,30294,30296,30305,30312,30324,30325,30326,30340,30354,30371,30388,30405,30409,30410,30434,30451,30468,30480,30503,30512,30513,30528,30544,30544,30576,30596,30602,30606,30635,30661,30686,30686,30686,30698,30701,30726,30764,30794,30813,30893,30910,30916,30950,30999,31045,31095,31248,31274,31285,31338,31416,31459,31511,31661,31700,31727,31808,31893,31956,32019,32149,32198,32230,32299,32365,32445,32521,32630,32684,32730,32825,32933,33037,33125,33303,33392,33477,33623,33885,34048,34210,34508,34645,34761,35018,35541,35785,36020,36565,36788,37019,37486,38392,38829,39244,40124,40480,40802,41350,42207]

"""Functions list"""

#The next 6 functions compute the evolution of the population for each compartment

def H(l,h):
        return(h-l*h)

def P(l,p,h):
    return(p+l*h-(t+x)*p)

def AI(l,p,ai):
    return(ai+t*p-y*ai)

def SI(ai,p,si):
    return(si+x*p-(z+u)*si)

def C(c,ai,si,s):
    if s<max_capacity:
        return(c+y*ai+z*si+v*s)
    else :  
        dif=s-max_capacity          #number of people who can't be taken in ICU
        return(c+y*ai+z*si+v*max_capacity+v_no_icu*dif)

def S(s,si):
    if s<max_capacity:
        return(s+u*si-(v+w)*s)
    else :
        dif=s-max_capacity
        return(s+u*si-(v+w)*max_capacity-(v_no_icu+w_no_icu)*dif)

def D(d,s):
    if s<max_capacity:
        return(d+w*s)
    else :
        dif=s-max_capacity
        return(d+w*max_capacity+w_no_icu*dif)

def L(beta,h,p,ai,si,c):
    return(beta*(p+ai+si)/(p+ai+si+c+h))
    
# Function to simulate the behaviour of people 
# Return a real between 0 and 1 to modulate beta parameter
        
def lockdown(c,t,t_lock,t_end):
    if t<t_lock:
        return(1)
    if t>t_end:
        return(1)
    else:
        return(c)
    
def behaviour(c,t,t_begining):
    if t<t_begining:
        return(1)
    else:
        return(c)

#Function to simulate the dynamic of the epidemic in France
#Return the total number of deads for each day
    
def evolution(c_behav,tf):
    h=64900000
    p=20
    ai=2
    si=12
    c=0
    s=0
    d=1
    list_h=[]
    list_p=[]
    list_ai=[]
    list_si=[]
    list_c=[]
    list_s=[]
    list_d=[]
    
    for k in range(tf):
        h0=h
        p0=p
        ai0=ai
        si0=si
        c0=c
        s0=s
        d0=d
        
        lock=lockdown(0.04,k,31,86)
        behav=behaviour(c_behav,k,87)
        l=L(beta,h0,p0,ai0,si0,c0)*behav*lock
    
        h=H(l,h0)
        p=P(l,p0,h0)
        ai=AI(l,p0,ai0)
        si=SI(ai0,p0,si0)
        c=C(c0,ai0,si0,s0)
        s=S(s0,si0)
        d=D(d0,s0)
        
        list_h.append(h)
        list_p.append(p)
        list_ai.append(ai)
        list_si.append(si)
        list_c.append(c)
        list_s.append(s)
        list_d.append(d)

    return(list_d)

def error(list_1,list_2):
    s=0
    for k in range(len(list_1)):
        s=s+abs(list_1[k]-list_2[k])
    return (s)

list_c_behav=[]
list_error=[]

for k in range(100):
    c_behav=0.2+0.001*k
    e=evolution(c_behav,200)
    E=error(e,data_deaths)
    list_c_behav.append(c_behav)
    list_error.append(E)
    
m=min(list_error)
i=list_error.index(m)
print(list_c_behav[i])

graphe_error=interpolate.interp1d(list_c_behav,list_error,kind="quadratic")
plt.plot(list_c_behav,graphe_error(list_c_behav),label='Erreur')

plt.xlabel("valeur de c_gestes_barrières")
plt.ylabel("erreur")
plt.title("Evolution de l'erreur avec c_gestes_barrières")
plt.legend()
plt.savefig('error_behav.pdf')
plt.show()
    