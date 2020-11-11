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

beta=0.46
t=0.15/5
x=0.85/5
y=1/10
z=0.92/7
u=0.08/7
v=0.7/10
w=0.3/10

tf=340     #number of days for the simulation

max_capacity=3000

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
    return(c+y*ai+z*si+v*s)

def S(s,si):
    return(s+u*si-(v+w)*s)

def D(d,s):
    return(d+w*s)

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
        return(0.05)

# Function to simulate the behaviour of people 
# Return a real between 0 and 1 to modulate beta parameter
        
def behaviour(t,t_begining):
    if t<t_begining:
        return(1)
    else:
        return(0.3)

#Function to determine if the limit of hospitalisation in intensive care is reached
        
def capacity(s,limit):
    if s<limit:
        return(False)
    else:
        return(True)
    
"""Initial conditions"""

h=67000000
p=12
ai=0
si=0
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

"""Population's evolution"""

for k in range(1,tf):
    
    h0=h
    p0=p
    ai0=ai
    si0=si
    c0=c
    s0=s
    d0=d
    
    lock1=lockdown(k,32,87)
    behav=behaviour(k,55)
    
    l=L(h0,p0,ai0,si0,c0)*lock1
    
    h=H(l,h0)
    list_h.append(h)
    
    p=P(l,p0,h0)
    list_p.append(p)
    
    ai=AI(l,p0,ai0)
    list_ai.append(ai)
    
    si=SI(ai0,p0,si0)
    list_si.append(si)
    
    c=C(c0,ai0,si0,s0)
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
plt.plot(time,graphe_h(time),label='S')
graphe_p=interpolate.interp1d(time,list_p,kind="quadratic")
plt.plot(time,graphe_p(time),label='IP')
graphe_ai=interpolate.interp1d(time,list_ai,kind="quadratic")
plt.plot(time,graphe_ai(time),label='IA')
graphe_si=interpolate.interp1d(time,list_si,kind="quadratic")
plt.plot(time,graphe_si(time),label='IS')
graphe_c=interpolate.interp1d(time,list_c,kind="quadratic")
plt.plot(time,graphe_c(time),label='G')
graphe_s=interpolate.interp1d(time,list_s,kind="quadratic")
plt.plot(time,graphe_s(time),label='R')
graphe_d=interpolate.interp1d(time,list_d,kind="quadratic")
plt.plot(time,graphe_d(time),label='M')
graphe_tot=interpolate.interp1d(time,list_tot,kind="quadratic")
#plt.plot(time,graphe_tot(time),label='Tot')

plt.xlabel("Temps(J)")
plt.ylabel("Population (nombre d'individus)")
plt.title("Evolution de chaque compartiments (340 J)")
plt.legend()
plt.savefig('populations.pdf')
plt.show()
