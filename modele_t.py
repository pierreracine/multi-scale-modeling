# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:55:32 2020
@author: Pierre
"""

# This programm has been made to simulate the propagation of the COVID-19 pandemic throught time.
# We use a compartmental model.
# The compartments used are healthy (H), asymptomatically infected (AI),
# symptomatically infected (SI), cured (C), severe (S) and dead (D)
# We suppose that the induced immunity is 100%.

"""Classical imports"""

import matplotlib.pyplot as plt
from scipy import interpolate

"""Parameters list"""

beta=0.35
x=0.03
y=0.05
z=0.05
u=0.01
v=0.03
w=0.01

tf=365     #number of days for the simulation

max_capacity=3000

"""Functions list"""

#The next 6 functions compute the evolution of the population for each compartment

def H(l,h):
        return(h-l*h)

def AI(l,h,ai):
    return(ai+l*h-(x+y)*ai)

def SI(ai,si):
    return(si+x*ai-(z+u)*si)

def C(c,ai,si,s):
    return(c+y*ai+z*si+v*s)

def S(s,si):
    return(s+u*si-(v+w)*s)

def D(d,s):
    return(d+w*s)

def L(h,ai,si,c):
    return(beta*(ai+si)/(ai+si+c+h))

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
        return(0.1)

#Function to determine if the limit of hospitalisation in intensive care is reached
        
def capacity(s,limit):
    if s<limit:
        return(False)
    else:
        return(True)
    
"""Initial conditions"""

h=63000000
ai=20
si=0
c=0
s=0
d=0

"""List initialisation"""

list_h=[h]
list_ai=[ai]
list_si=[si]
list_c=[c]
list_s=[s]
list_d=[d]

list_capacity=[]        #list of days when the full capacity of intensive care is reached

"""Population's evolution"""

for k in range(1,tf):
    
    h0=h
    ai0=ai
    si0=si
    c0=c
    s0=s
    d0=d
    
    lock=lockdown(k,55,115)
    behav=behaviour(k,85)
    
    l=L(h0,ai0,si0,c0)
    
    h=H(l,h0)
    list_h.append(h)
    
    ai=AI(l,h0,ai0)
    list_ai.append(ai)
    
    si=SI(ai0,si0)
    list_si.append(si)
    
    c=C(c0,ai0,si0,s0)
    list_c.append(c)
    
    s=S(s0,si0)
    list_s.append(s)
    
    d=D(d0,s0)
    list_d.append(d)
    
    if capacity(s,max_capacity)==True:
        list_capacity.append(k)

list_tot=[]
for k in range(tf):
    tot=list_h[k]+list_si[k]+list_ai[k]+list_c[k]+list_s[k]+list_d[k]
    list_tot.append(tot)
    
"""Graphs"""

time=list(range(tf))

graphe_h=interpolate.interp1d(time,list_h,kind="quadratic")
plt.plot(time,graphe_h(time),label='H')
graphe_ai=interpolate.interp1d(time,list_ai,kind="quadratic")
plt.plot(time,graphe_ai(time),label='AI')
graphe_si=interpolate.interp1d(time,list_si,kind="quadratic")
plt.plot(time,graphe_si(time),label='SI')
graphe_c=interpolate.interp1d(time,list_c,kind="quadratic")
plt.plot(time,graphe_c(time),label='C')
graphe_s=interpolate.interp1d(time,list_s,kind="quadratic")
plt.plot(time,graphe_s(time),label='S')
graphe_d=interpolate.interp1d(time,list_d,kind="quadratic")
plt.plot(time,graphe_d(time),label='D')

plt.xlabel("Time(D)")
plt.ylabel("Population (number of individuals)")
plt.title("Evolution of each compartment")
plt.legend()
plt.savefig('populations.pdf')
plt.show()
