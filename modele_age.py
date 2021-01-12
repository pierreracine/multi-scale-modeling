# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:45:47 2020

@author: Pierre
"""


# This programm has been made to simulate the propagation of the COVID-19 epidemic
# in France, with account of the age.
# We use a compartmental model.
# The compartments used are healthy (H), presymptomatic (P), asymptomatically infected (AI),
# symptomatically infected (SI), cured (C), severe (S) and dead (D)
# We suppose that the induced immunity is 100%.
# There are 4 classes of age for the comparaison with the available data : 
# [0-14], [15-44], [45-64], [65-].

"""Classical imports"""

import matplotlib.pyplot as plt
from scipy import interpolate

"""Parameters list"""

t=[]
x=[]
y=
z=[]
u=[]
v=[]
w=[]
c=[[]]
tf=300

"""Functions list"""

def l(q,ai,si,pi):
    l=[]
    for i in range (len(c)):
        for k in range (len(c)):
            li=q*(c[k][i]*(ai[i]+si[i]+pi[i]))
            l.append(li)
    return(l)

def H(l,h):
    H1=[]
    H_0=-l[0]*h[0]-(1/365)*(h[1]-h[0])+h[0]
    H1.append(H_0)
    for i in range(len(h)-1):
        Hi=-l[i]*h[i]-(1/365)*(h[i]-h[i-1])+h[i]
        H1.append(Hi)
    return(H1)

def PI(l,h,pi):
    P1=[]
    Pi_0=p[0]*(1-t[0]-x[0])+l[0]*h[0]-(1/365)*(pi[1]-pi[0])
    PI1.append(Pi_0)
    for i in range (len(p)-1):
        Pi=pi[i]*(1-t[i]-x[i])+l[i]*h[i]-(1/365])*(pi[i]-pi[i-1])
        P1.append(Pi)
    return(P1)

def AI(pi,ai):
    AI1=[]
    AI_0=ai[0]*(1-y)+t[0]*pi[0]-(1/365)*(ai[1]-ai[0])
    AI1.append(AI_0)
    for i in range (len(ai)-1):
        AIi=ai[i]*(1-y)+t[i]*pi[i]-(1/365)*(ai[i]-ai[i-1])
        AI1.append(AIi)
    return(AI1)

def SI(pi,si):
    SI1=[]
    SI_0=si[0]*(1-z[0]-u[0])+x[0]*pi[0]-(1/365)*(si[1]-si[0])
    SI1.append(SI_0)
    for i in range (len(si)-1):
        SIi=si[i]*(1-z[i]-u[i])+x[i]*pi[i]-(1/365)*(si[i]-si[i-1])
        SI1.append(SIi)
    return(SI1)

def S(si,s):
    S1=[]
    S_0=s[0]*(1-v[0]-w[0])+u[0]*SI[0]-(1/365)*(s[1]-s[0])
    S1.append(S_0)
    for i in range(len(s)-1):
        Si=s[i]*(1-v[i]-w[i])+u[i]*SI[i]-(1/365)*(s[i]-s[i-1])
        S1.append(Si)
    return(S1)

def C(ai,si,s,c):
    C1=[]
    C_0=c[0]+y*ai[0]+z[0]*si[0]+v[0]*s[0]-(1/365)*(c[1]-c[0])
    C1.append(C_0)
    for i in range (len(c)-1):
        Ci=c[i]+y*ai[i]+z[i]*si[i]+v[i]*s[i]-(1/365)*(c[i]-c[i-1])
        C1.append(Ci)
    return(C1)

def D(s,d):
    D1=[]
    D_0=d[0]+w[0]*s[0]-(1/365)*(d[1]-d[0])
    D1.append(D_0)
    for i in range(len(d)-1):
        Di=d[i]+w[0]*s[i]-(1/365)*(d[i]-d[i-1])
        D1.append(Di)
    return(D1)

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
    pi=PI(l,h0,pi0)
    ai=AI(pi0,ai0)
    si=SI(pi0,si0)
    s=S(si0,s0)
    c=C(ai0,si0,s0,c0)
    d=D(s0,d0)
    
    list_h.append(h)
    list_pi.append(pi)
    list_ai.append(ai)
    list_si.append(si)
    list_s.append(s)
    list_c.append(c)
    list_d.append(d)
       
# Function to sum over all age classes in the above lists :
    
def suml(l):
    L=[]
    for k in range(len(l)):
        sl=sum(l[k])
        L.append(sl)
    return(L)

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
plt.savefig('populations_structure_age.pdf')
plt.show()