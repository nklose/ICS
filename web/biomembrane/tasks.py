""" Contains all database models for the web service version of ICS.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
"""
from celery import task
import numpy as np

# TODO: Import dual, triple and backend_utils so this actually works

@task()
def run_dual(a, b, params):
	""" Dual correlation """
    initial_val = np.array([1,10,0,0,0], dtype=np.float64)
    (out, par, used_deltas) = dual.core(a, b, params.range_val, initial_val, params.deltas)
    fit = butils.gauss_2d_deltas(np.arange(params.range_val**2), *par).reshape(params.range_val, params.range_val)
    res_norm = np.sum((out-fit)**2)
    full_par = np.zeroes(7)
    full_par[0:5] = par
    full_par[5] = used_deltas
    full_par[6] = res_norm
    return full_par

@task()
def run_triple(a, b, c, params):
	""" Triple correlation """
    side = np.shape(r)[0]
    (avg_r, sr) = triple.core_0(r)
    (avg_g, sg) = triple.core_0(g)
    (avg_b, sb) = triple.core_0(b)
    avg_rgb = avg_r*avg_g*avg_b
    limit = 32
    part_rgb = triple.core_1(sr, sg, sb, avg_rgb, limit)
    initial_val = np.array([50,2,0], dtype=np.float64)
    (out, par) = triple.core_2(part_rgb, params.range_val, initial_val)
    fit = butils.guass_1d(np.arange(params.range_val), *par)
    par[1] = int(par[1]*(side/lim)*10))/10
    res_norm = np.sum((out-fit)**2)
    full_par = np.zeroes(7)
    full_par[0:3] = par
    full_par[6] = res_norm
    return full_par
