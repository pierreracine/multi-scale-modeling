# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:55:32 2020
@author: Pierre
"""

# This programm has been made to simulate the propagation of the COVID-19 pandemic throught time.
# We use a compartmental model.
# The compartments used are healthy (H), presymptomatic (P), asymptomatically infected (AI),
# symptomatically infected (SI), cured (C), severe (S) and dead (D)
# We suppose that the induced immunity is 100%.

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
total_data_death=[1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,4,4,7,9,16,19,30,33,48,61,79,91,127,148,175,264,372,450,562,674,860,1100,1331,1696,1995,2314,2606,3024,3522,4030,5384,6503,7555,8072,8904,10320,10860,12199,13185,13819,14380,14954,15715,17152,17904,18664,19305,19700,20246,20776,21319,21834,22223,22592,22834,23270,23637,24063,24352,24570,24736,24871,25177,25507,25785,25963,26206,26286,26356,26619,26967,27050,27401,27505,27601,28083,28214,27997,28107,28190,28264,28307,28342,28407,28505,28571,28637,28689,28746,28777,28808,28915,28996,29040,29086,29117,29130,29184,29271,29294,29321,29349,29373,29382,29411,29522,29550,29578,29592,29608,29615,29638,29695,29706,29727,29753,29761,29770,29788,29818,29836,29850,29868,29875,29882,29895,29908,29940,29954,29979,29983,29986,30004,30075,30095,30113,30127,30136,30144,30152,30165,30172,30182,30192,30196,30200,30209,30223,30238,30254,30265,30268,30272,30294,30296,30305,30312,30324,30325,30326,30340,30354,30371,30388,30405,30409,30410,30434,30451,30468,30480,30503,30512,30513,30528,30544,30544,30576,30596,30602,30606,30635,30661,30686,30686,30686,30698,30701,30726,30764,30794,30813,30893,30910,30916,30950,30999,31045,31095,31248,31274,31285,31338,31416,31459,31511,31661,31700,31727,31808,31893,31956,32019,32149,32198,32230,32299,32365,32445,32521,32630,32684,32730,32825,32933,33037,33125,33303,33392,33477,33623,33885,34048,34210,34508,34645,34761,35018,35541,35785,36020,36565,36788,37019,37486,38392,38829,39244,40124,40480,40802,41350,42207]
tf=360     #number of days for the simulation

max_capacity=14000

"""Functions list"""

#The next 6 functions compute the evolution of the population for each compartment

def H(l,h,vax):
        return(h-l*h-vax)

def P(l,p,h):
    return(p+l*h-(t+x)*p)

def AI(p,ai):
    return(ai+t*p-y*ai)

def SI(p,si):
    return(si+x*p-(z+u)*si)

def C(c,ai,si,s,vax):
    if s<max_capacity:
        return(c+y*ai+z*si+v*s+vax)
    else :  
        dif=s-max_capacity          #number of people who can't be taken in ICU
        return(c+y*ai+z*si+v*max_capacity+v_no_icu*dif+vax)

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

def L(h,p,ai,si,c):
    return(beta*(p+ai+si)/(p+ai+si+c+h))

# Function to simulate a lockdown on the entire country
# Return a real between 0 and 1 to modulate beta parameter
    
def lockdown(t,t_lock,t_end):
    if t<t_lock:
        return(1)
    if t>t_end:
        return(1)
    else:
        return(0.04)

# Function to simulate the behaviour of people 
# Return a real between 0 and 1 to modulate beta parameter
        
def behaviour(t,t_begining):
    if t<t_begining:
        return(1)
    else:
        return(0.262)

# Function to simulate a vaccination campaign in the population
# 0.95 represents the effectiveness of the vaccine and 300000 the number of people vaccinated each day

def vax(t,t_vax,t_end):
    if t>=t_vax and t<=t_end:
        return(0.95*300000)
    else:
        return(0)

#Function to determine if the limit of hospitalisation in intensive care is reached
        
def capacity(s,limit):
    if s<limit:
        return(False)
    else:
        return(True)

"""Initial conditions"""

h=64900000
p=20
ai=2
si=12
c=0
s=0
d=1

"""List initialisation"""

list_h=[h]
list_p=[p]
list_ai=[ai]
list_si=[si]
list_c=[c]
list_s=[s]
list_d=[d]

list_tot=[]
list_capacity=[]        #list of days when the full capacity of intensive care is reached
days=["Feb 15","Feb 16","Feb 17","Feb 18","Feb 19","Feb 20","Feb 21","Feb 22","Feb 23","Feb 24","Feb 25","Feb 26","Feb 27","Feb 28","Feb 29","Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06","Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27","Mar 28","Mar 29","Mar 30","Mar 31","Apr 01","Apr 02","Apr 03","Apr 04","Apr 05","Apr 06","Apr 07","Apr 08","Apr 09","Apr 10","Apr 11","Apr 12","Apr 13","Apr 14","Apr 15","Apr 16","Apr 17","Apr 18","Apr 19","Apr 20","Apr 21","Apr 22","Apr 23","Apr 24","Apr 25","Apr 26","Apr 27","Apr 28","Apr 29","Apr 30","May 01","May 02","May 03","May 04","May 05","May 06","May 07","May 08","May 09","May 10","May 11","May 12","May 13","May 14","May 15","May 16","May 17","May 18","May 19","May 20","May 21","May 22","May 23","May 24","May 25","May 26","May 27","May 28","May 29","May 30","May 31","Jun 01","Jun 02","Jun 03","Jun 04","Jun 05","Jun 06","Jun 07","Jun 08","Jun 09","Jun 10","Jun 11","Jun 12","Jun 13","Jun 14","Jun 15","Jun 16","Jun 17","Jun 18","Jun 19","Jun 20","Jun 21","Jun 22","Jun 23","Jun 24","Jun 25","Jun 26","Jun 27","Jun 28","Jun 29","Jun 30","Jul 01","Jul 02","Jul 03","Jul 04","Jul 05","Jul 06","Jul 07","Jul 08","Jul 09","Jul 10","Jul 11","Jul 12","Jul 13","Jul 14","Jul 15","Jul 16","Jul 17","Jul 18","Jul 19","Jul 20","Jul 21","Jul 22","Jul 23","Jul 24","Jul 25","Jul 26","Jul 27","Jul 28","Jul 29","Jul 30","Jul 31","Aug 01","Aug 02","Aug 03","Aug 04","Aug 05","Aug 06","Aug 07","Aug 08","Aug 09","Aug 10","Aug 11","Aug 12","Aug 13","Aug 14","Aug 15","Aug 16","Aug 17","Aug 18","Aug 19","Aug 20","Aug 21","Aug 22","Aug 23","Aug 24","Aug 25","Aug 26","Aug 27","Aug 28","Aug 29","Aug 30","Aug 31","Sep 01","Sep 02","Sep 03","Sep 04","Sep 05","Sep 06","Sep 07","Sep 08","Sep 09","Sep 10","Sep 11","Sep 12","Sep 13","Sep 14","Sep 15","Sep 16","Sep 17","Sep 18","Sep 19","Sep 20","Sep 21","Sep 22","Sep 23","Sep 24","Sep 25","Sep 26","Sep 27","Sep 28","Sep 29","Sep 30","Oct 01","Oct 02","Oct 03","Oct 04","Oct 05","Oct 06","Oct 07","Oct 08","Oct 09","Oct 10","Oct 11","Oct 12","Oct 13","Oct 14","Oct 15","Oct 16","Oct 17","Oct 18","Oct 19","Oct 20","Oct 21","Oct 22","Oct 23","Oct 24","Oct 25","Oct 26","Oct 27","Oct 28","Oct 29","Oct 30","Oct 31","Nov 01","Nov 02","Nov 03","Nov 04","Nov 05","Nov 06","Nov 07","Nov 08","Nov 09","Nov 10","Nov 11","Nov 12","Nov 13","Nov 14","Nov 15","Nov 16","Nov 17","Nov 18","Nov 19","Nov 20","Nov 21","Nov 22","Nov 23","Nov 24","Nov 25","Nov 26","Nov 27","Nov 28","Nov 29","Nov 30","Dec 01","Dec 02","Dec 03","Dec 04"]

"""Population's evolution"""

for k in range(1,tf):
    
    h0=h
    p0=p
    ai0=ai
    si0=si
    c0=c
    s0=s
    d0=d
    
    lock1=lockdown(k,32,86)
    behav=behaviour(k,87)
    vax1=vax(k,120,180)
    
    l=L(h0,p0,ai0,si0,c0)*lock1*behav
    
    h=H(l,h0,vax1)
    list_h.append(h)
    
    p=P(l,p0,h0)
    list_p.append(p)
    
    ai=AI(p0,ai0)
    list_ai.append(ai)
    
    si=SI(p0,si0)
    list_si.append(si)
    
    c=C(c0,ai0,si0,s0,vax1)
    list_c.append(c)
    
    s=S(s0,si0)
    list_s.append(s)
    
    d=D(d0,s0)
    list_d.append(d)
    
    tot=h+p+ai+si+c+s+d
    
    if capacity(s,max_capacity)==True:
        list_capacity.append(k)

for k in range(tf):
    tot=list_h[k]+list_p[k]+list_si[k]+list_ai[k]+list_c[k]+list_s[k]+list_d[k]
    list_tot.append(tot)
    
"""Graphs"""

time=list(range(tf))

graphe_h=interpolate.interp1d(time,list_h,kind="quadratic")
#plt.plot(time,graphe_h(time),label='Sains')
graphe_p=interpolate.interp1d(time,list_p,kind="quadratic")
plt.plot(time,graphe_p(time),label='IP')
graphe_ai=interpolate.interp1d(time,list_ai,kind="quadratic")
plt.plot(time,graphe_ai(time),label='IA')
graphe_si=interpolate.interp1d(time,list_si,kind="quadratic")
plt.plot(time,graphe_si(time),label='IS')
graphe_c=interpolate.interp1d(time,list_c,kind="quadratic")
#plt.plot(time,graphe_c(time),label='Guéris')
graphe_s=interpolate.interp1d(time,list_s,kind="quadratic")
plt.plot(time,graphe_s(time),label='S')
graphe_d=interpolate.interp1d(time,list_d,kind="quadratic")
plt.plot(time,graphe_d(time),label='M')
graphe_tot=interpolate.interp1d(time,list_tot,kind="quadratic")
#plt.plot(time,graphe_tot(time),label='Tot')

plt.xlabel("Temps(jours)")
plt.ylabel("Population (nombre d'individus)")
plt.title("Evolution des populations (360 jours)")
plt.legend()
plt.savefig('vaccination.pdf')
plt.show()