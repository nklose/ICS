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
from ics import dual, triple
from ics import backend_utils as butils
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

    initial_val = np.array([1,10,0,0,0], dtype=np.float64)
    (out, par, used_deltas) = dual.core(a, b, params.range_val, initial_val, params.use_deltas)
    fit = butils.gauss_2d_deltas(np.arange(params.range_val**2), *par).reshape(params.range_val, params.range_val)
    res_norm = np.sum((out-fit)**2)
    return (out, par, used_deltas, res_norm)


def run_triple(job, params):
    r = pickle.loads(job.red)
    g = pickle.loads(job.green)
    b = pickle.loads(job.blue)
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
    return (out, par, res_norm)


@task()
def run(job):
    job.state = Job.RUNNING
    job.save()

    all_params = Parameters.objects.filter(batch=job.batch)
    for params in all_params:
        results = Results(job=job, params=params)
        if params.correlationType == Parameters.TRIPLE:
            out, par, res_norm = run_triple(job, params)
        else:
            out, par, used_deltas, res_norm = run_dual(job, params)
            results.used_deltas = pickle.dumps(used_deltas)
        results.par = pickle.dumps(par)
        results.out = pickle.dumps(out)
        results.res_norm = pickle.dumps(res_norm)
        results.save()
        
    job.state = Job.COMPLETE
    job.save()

