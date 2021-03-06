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
# The goal of this script is to optimize the parameter beta, based on data available about
# the number of total death.

"""Classical imports"""

import matplotlib.pyplot as plt
from scipy import interpolate


"""Parameters list"""

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
data_deaths=[1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,4,4,7,9,16,19,30,33,48,61,79,91,127,148,175,264,372,450,562,674]

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

#Function to simulate the dynamic of the epidemic in France
#Return the total number of deads for each day
    
def evolution(beta,tf):
    h=64900000
    p=20
    ai=2
    si=12
    c=0
    s=0
    d=1
    list_h=[h]
    list_p=[p]
    list_ai=[ai]
    list_si=[si]
    list_c=[c]
    list_s=[s]
    list_d=[d]

    list_tot=[]
    
    for k in range(1,tf):
        h0=h
        p0=p
        ai0=ai
        si0=si
        c0=c
        s0=s
        d0=d
    
        l=L(beta,h0,p0,ai0,si0,c0)
    
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
    
    for k in range(tf):
        tot=list_h[k]+list_p[k]+list_si[k]+list_ai[k]+list_c[k]+list_s[k]+list_d[k]
        list_tot.append(tot)

    return(list_d)

def error(list_1,list_2):
    s=0
    for k in range(len(list_1)):
        s=s+abs(list_1[k]-list_2[k])
    return (s)

list_beta=[]
list_error=[]

for k in range(200):
    beta=0.3+0.001*k
    e=evolution(beta,31)
    E=error(e,data_deaths)
    list_beta.append(beta)
    list_error.append(E)
    
m=min(list_error)
i=list_error.index(m)
print(list_beta[i])

graphe_error=interpolate.interp1d(list_beta,list_error,kind="quadratic")
plt.plot(list_beta,graphe_error(list_beta),label='Erreur')

plt.xlabel("valeur de beta")
plt.ylabel("erreur (nombre de morts)")
plt.title("Evolution de l'erreur avec beta")
plt.legend()
plt.savefig('error_beta.pdf')
plt.show()
    