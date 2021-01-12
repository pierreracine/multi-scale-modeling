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
data_deaths=[1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,4,4,7,9,16,19,30,33,48,61,79,91,127,148,175,264,372,450,562,674,860,1100,1331,1696,1995,2314,2606,3024,3522,4030,5384,6503,7555,8072,8904,10320,10860,12199,13185,13819,14380,14954,15715,17152,17904,18664,19305,19700,20246,20776,21319,21834,22223,22592,22834,23270,23637,24063,24352,24570,24736,24871,25177,25507,25785,25963,26206,26286,26356,26619,26967,27050,27401,27505,27601]


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

# Function to simulate a lockdown on the entire country
# Return a real between 0 and 1 to modulate beta parameter
    
def lockdown(c,t,t_lock,t_end):
    if t<t_lock:
        return(1)
    if t>t_end:
        return(1)
    else:
        return(c)

#Function to simulate the dynamic of the epidemic in France
#Return the total number of deads for each day
    
def evolution(c_lock,tf):
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
        
        lock=lockdown(c_lock,k,31,86)
        l=L(beta,h0,p0,ai0,si0,c0)*lock
    
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

list_c_lock=[]
list_error=[]

for k in range(1000):
    c_lock=0.0001*k
    e=evolution(c_lock,86)
    E=error(e,data_deaths)
    list_c_lock.append(c_lock)
    list_error.append(E)
    
m=min(list_error)
i=list_error.index(m)
print(list_c_lock[i])

graphe_error=interpolate.interp1d(list_c_lock,list_error,kind="quadratic")
plt.plot(list_c_lock,graphe_error(list_c_lock),label='Erreur')

plt.xlabel("valeur de c_confinement")
plt.ylabel("erreur")
plt.title("Evolution de l'erreur avec c_confinement")
plt.legend()
plt.savefig('error_lock.pdf')
plt.show()
    