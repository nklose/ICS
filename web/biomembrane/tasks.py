"""
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
from models import Job, Parameters, Results
from backend import dual
from backend import triple
from backend import backend_utils as butils
import numpy as np
import pickle


def run_dual(job, params):
    if params.correlationType == Parameters.AUTO:
        if params.red == True:
            a = b = pickle.loads(job.red)
        elif params.green == True:
            a = b = pickle.loads(job.green)
        else:
            a = b = pickle.loads(job.blue)

    if params.correlationType == Parameters.CROSS:
        if params.red == True:
            a = pickle.loads(job.red)
            if params.green == True:
                b = pickle.loads(job.green)
            else:
                b = pickle.loads(job.blue)
        else:
            a = pickle.loads(job.green)
            b = pickle.loads(job.blue)

    initial_val = np.array([params.g0, params.w, params.ginf, 0, 0], dtype=np.float64)
    out, par, used_deltas = dual.core(a, b, params.range_val, initial_val, params.use_deltas)
    fit_before_reshape = butils.gauss_2d_deltas(np.arange(params.range_val**2), *par)
    fit = fit_before_reshape.reshape(params.range_val, params.range_val)
    res_norm = np.sum((out-fit)**2)

    results = Results(job=job, params=params)
    results.par = pickle.dumps(par)
    results.out = pickle.dumps(out)
    results.res_norm = pickle.dumps(res_norm)
    results.fit = pickle.dumps(fit)
    results.fit_before_reshape = pickle.dumps(fit_before_reshape)
    results.used_deltas = pickle.dumps(used_deltas)
    results.save()


def run_triple(job, params):
    r = pickle.loads(job.red)
    g = pickle.loads(job.green)
    b = pickle.loads(job.blue)
    side = np.shape(r)[0]
    avg_r, sr = triple.core_0(r)
    avg_g, sg = triple.core_0(g)
    avg_b, sb = triple.core_0(b)
    avg_rgb = avg_r*avg_g*avg_b
    part_rgb = triple.core_1(sr, sg, sb, avg_rgb, params.limit)
    initial_val = np.array([params.g0, params.w, params.ginf], dtype=np.float64)
    out, par = triple.core_2(part_rgb, params.range_val, initial_val)
    fit = butils.guass_1d(np.arange(params.range_val), *par)
    par[1] = int(par[1]*(side/params.limit)*10)/10
    res_norm = np.sum((out-fit)**2)

    results = Results(job=job, params=params)
    results.par = pickle.dumps(par)
    results.out = pickle.dumps(out)
    results.res_norm = pickle.dumps(res_norm)
    results.fit = pickle.dumps(fit)
    results.save()


def run_triple1(job):
    r = pickle.loads(job.red)
    g = pickle.loads(job.green)
    b = pickle.loads(job.blue)
    avg_r, sr = triple.core_0(r)
    avg_g, sg = triple.core_0(g)
    avg_b, sb = triple.core_0(b)
    return (avg_r, sr, avg_g, sg, avg_b, sb)


def run_triple2(job, params, avg_r, sr, avg_g, sg, avg_b, sb):
    avg_rgb = avg_r*avg_g*avg_b
    part_rgb = triple.core_1(sr, sg, sb, avg_rgb, params.limit)
    return part_rgb


def run_triple3(job, params, part_rgb):
    r = pickle.loads(job.red)
    side = np.shape(r)[0]
    initial_val = np.array([params.g0, params.w, params.ginf], dtype=np.float64)
    out, par = triple.core_2(part_rgb, params.range_val, initial_val)
    fit = butils.guass_1d(np.arange(params.range_val), *par)
    par[1] = int(par[1]*(side/params.limit)*10)/10
    res_norm = np.sum((out-fit)**2)

    results = Results(job=job, params=params)
    results.par = pickle.dumps(par)
    results.out = pickle.dumps(out)
    results.res_norm = pickle.dumps(res_norm)
    results.fit = pickle.dumps(fit)
    results.save()


@task()
def run_batch(job):
    # TODO: Use actual batch interface
    job.state = Job.RUNNING
    job.save()

    all_params = Parameters.objects.filter(batch=job.batch)
    for params in all_params:
        if params.correlationType == Parameters.TRIPLE:
            run_triple(job, params)
        else:
            run_dual(job, params)
        
    job.state = Job.COMPLETE
    job.save()
