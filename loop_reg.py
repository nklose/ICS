"""Regular loop

This file contains the loop needed in the core_1 function in
the triple.py file. This is a straightforward implementation,
focusing on simplicity and correctness. It is probably fast
enough for interactive use.
"""

from __future__ import division
import numpy as np

def core(r1,sr,sg,tb,side,lim):
    na = int(side/2)
    nb = int(lim/2)
    lowlim = na-nb
    low = lowlim-na
    high = na-lowlim
    for v1 in xrange(low,high):
        for u1 in xrange(low-min(v1-1,0),high-max(v1,0)):
            for v2 in xrange(low,high):
                for u2 in xrange(low,high):
                    if abs(u2+v2) < na:
                        r1[nb+v1,nb+u1,nb+v2,nb+u2] = \
                          sr[na+u1,na+u2] * \
                          sg[na+v1,na+v2] * \
                          tb[na+u1+v1,na+u2+v2]
