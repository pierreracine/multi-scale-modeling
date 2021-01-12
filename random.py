# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 20:27:26 2020

@author: Pierre
"""

# This programm has been made to simulate the propagation of the COVID-19 pandemic throught time.
# We use a stochstic compartmental model, with age classes.
# The compartments used are healthy (H), presymptomatic (P), asymptomatically infected (AI),
# symptomatically infected (SI), cured (C), severe (S) and dead (D)
# We suppose that the induced immunity is 100%.
# The number of people entering a class througth a path between 2 compartments is computed stochasticaly
# For example the number of new cured people from severe cases is noted C_s_new.
# When there is only one way to go to a compartment the compartment of origin is not written
# For exemple P_new and not P_h_new.

"""Classical imports"""

from math import exp
from random import random
from random import expovariate

"""Parameters list"""

t=[]
x=[]
y=
z=[]
u=[]
v=[]
w=[]
q=
c=[[]]
tf=300

"""Functions"""

# Some usefull functions to give a number with a defined probability law :

def bernouilli(p):
    if random()<p:
        return (1)
    else:
        return (0)
    
def binomial(n,p):
    s=0
    for k in range(n):
        s+=bernouilli(p)
    return(s)

def poisson(l):
    t=1/expovariate(l)
    return(int(t))

# Functions to compute the number of new people changing of compartement :
    
def l(q,ai,si,pi):
    l=[]
    for i in range (len(c)):
        for k in range (len(c)):
            li=q*(c[k][i]*(ai[i]+si[i]+pi[i]))
            l.append(li)
    return(l)

def PI_new(l,h):
    PI=[]
    for k in range(l):
       pi=binomial(h[k],1-exp(-l[k]))
       PI.append(pi)
    return(PI)

def AI_new(pi):
    AI=[]
    for k in range(len(pi)):
        ai=binomial(pi[k],1-exp(-t[k]))
        AI.append(ai)
    return(AI)

def SI_new(pi):
    SI=[]
    for k in range(len(pi)):
        si=binomial(pi[k],1-exp(-x[k]))
        SI.append(si)
    return(SI)

def C_ai_new(ai):
    C=[]
    for k in range(len(ai)):
        c=binomial(ai[k],1-exp(-y))
        C.append(c)
    return(C)

def C_si_new(si):
    C=[]
    for k in range(len(si)):
        c=binomial(si[k],1-exp(-z[k]))
        C.append(c)
    return(C)

def C_s_new(s):
    C=[]
    for k in range(len(s)):
        c=binomial(s[k],1-exp(-v[k]))
        C.append(c)
    return(C)

def S_new(si):
    S=[]
    for k in range(len(si)):
        s=binomial(si[k],1-exp(-u[k]))
        S.append(s)
    return(S)

def D_new(s):
    D=[]
    for k in range(len(s)):
        d=binomial(s[k],1-exp(-w[k]))
        D.append(d)
    return(D)

def H(l,h):
    H=[]
    pi_new=PI_new(l, h)
    for k in range(len(h)):
        h0=h[k]-pi_new[k]
        H.append(h0)
    return(H)

def PI(l,h,pi,ai,si):
    PI=[]
    pi_new=PI_new(l,h)
    ai_new=AI_new(pi)
    si_new=SI_new(pi)
    for k in range(len(pi)):
        pi0=pi[k]+pi_new[k]-si_new[k]-ai_new[k]
        PI.append(pi0)
    return(PI)

def AI(ai,pi):
    AI=[]
    ai_new=AI_new(pi)
    c_ai_new=C_ai_new(ai)
    for k in range(len(ai)):
        ai0=ai[k]+ai_new[k]-c_ai_new[k]
        AI.append(ai0)
    return(AI)

def SI(si,pi):
    SI=[]
    si_new=SI_new(pi)
    c_si_new=C_si_new(si)
    s_si_new=S_si_new(si)
    for k in range(len(si)):
        si0=si[k]+si_new[k]-c_si_new[k]-s_si_new[k]
        SI.append(si0)
    return(SI)

def C(c,ai,si,s):
    C=[]
    c_ai_new=C_ai_new(ai)
    c_si_new=C_si_new(si)
    c_s_new=C_s_new(s)
    for k in range(len(c)):
        c0=c[k]+c_ai_new[k]-c_si_new[k]-c_s_new[k]
        C.append(c0)
    return(C)

def S(s,si):
    S=[]
    s_new=S_new(si)
    c_s_new=C_s_new(s)
    d_new=D_new(s)
    for k in range(len(s)):
        s0=s[k]+s_new[k]-c_s_new[k]-d_new[k]
        S.append(s0)
    return(S)

def D(d,si):
    D=[]
    s_new=S_new(si)
    for k in range(d):
        d0=d[k]+s_new[k]
        D.append(d0)
    return(D)

# Function to sum over all age classes in the above lists :
    
def suml(l):
    L=[]
    for k in range(len(l)):
        sl=sum(l[k])
        L.append(sl)
    return(L)

# Initial conditions :
    
h=
pi=
ai=
si=
s=
c=
d=
    
# List initialisation :

list_h=[h]
list_pi=[pi]
list_ai=[ai]
list_si=[si]
list_c=[c]
list_s=[s]
list_d=[d]
    
for k in range (tf):
        
    h0=h
    pi0=pi
    ai0=ai
    si0=si
    s0=s
    c0=c
    d0=d
        
    l=l(q,ai0,si0,pi0)
    h=H(l,h0)
    pi=PI(l,h0,pi0,ai0,si0)
    ai=AI(ai0,pi0)
    si=SI(si0,pi0)
    c=C(c0,ai0,si0,s0)
    d=D(d0,si0)
    
    list_h.append(h)
    list_pi.append(pi)
    list_ai.append(ai)
    list_si.append(si)
    list_s.append(s)
    list_c.append(c)
    list_d.append(d)
    
list_h_tot=suml(list_h)
list_pi_tot=suml(list_pi)
list_ai_tot=suml(list_ai)
list_si_tot=suml(list_si)
list_s_tot=suml(list_s)
list_c_tot=suml(list_c)
list_d_tot=suml(list_d)

"""Graphs"""

time=list(range(tf))

graphe_h=interpolate.interp1d(time,list_h_tot,kind="quadratic")
plt.plot(time,graphe_h(time),label='H')
graphe_p=interpolate.interp1d(time,list_p_tot,kind="quadratic")
plt.plot(time,graphe_p(time),label='PI')
graphe_ai=interpolate.interp1d(time,list_ai_tot,kind="quadratic")
plt.plot(time,graphe_ai(time),label='AI')
graphe_si=interpolate.interp1d(time,list_si_tot,kind="quadratic")
plt.plot(time,graphe_si(time),label='SI')
graphe_c=interpolate.interp1d(time,list_c_tot,kind="quadratic")
plt.plot(time,graphe_c(time),label='C')
graphe_s=interpolate.interp1d(time,list_s_tot,kind="quadratic")
plt.plot(time,graphe_s(time),label='S')
graphe_d=interpolate.interp1d(time,list_d_tot,kind="quadratic")
plt.plot(time,graphe_d(time),label='D')

plt.xlabel("Temps(jours)")
plt.ylabel("Population (nombre d'individus)")
plt.title("Evolution des populations (300 jours)")
plt.legend()
plt.savefig('populations_stochastic.pdf')
plt.show()