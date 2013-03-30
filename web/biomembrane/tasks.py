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
from models import Batch, Correlation, DualParameters, TripleParameters, Result
from django.core.files.base import ContentFile
from StringIO import StringIO
from midend import adaptor, batchRunner
import PIL.Image
import numpy


class Config:
    side = None
    input_directory = None
    output_directory = None
    name_min = None
    name_max = None
    name_format = None
    dual_range = None
    triple_range = None
    auto_consider_deltas = None
    cross_consider_deltas = None
    dual_initial = None 
    triple_initial = None 
    triple_lim = None
    input_type = None
    output_type = 'full'
    output_numbering = '{:03d}'


def _save_result(correlation, job, ics_result):
    color = correlation.color
    data = StringIO()
    fit = StringIO()
    ics_result.saveDataFileLike(data, fit)
    data.seek(0)
    fit.seek(0)
    graph = ics_result.plotToStringIO()
    result = Result(correlation=correlation, job=job)
    result.data_file.save(color+'.txt', ContentFile(data.read()))
    result.fit_file.save(color+'_fit.txt', ContentFile(fit.read()))
    result.graph_image.save(color+'_graph.png', ContentFile(graph.read()))
    result.save()


@task()
def run_dual(job):
    params = DualParameters.objects.get(batch=job.batch)
    correlations = Correlation.objects.filter(batch=job.batch).exclude(color=Correlation.RGB)
    image = PIL.Image.open(job.rgb_image.path)

    for correlation in correlations:
        if len(correlation.color) == 1:
            use_deltas = params.auto_deltas
        else:
            use_deltas = params.cross_deltas
        result = adaptor.run_dual_mixed_image(image, [correlation.color], params.g0, params.w, params.ginf, params.range_val, use_deltas)[0]
        _save_result(correlation, job, result)


def run_triple1(job):
    image = PIL.Image.open(job.rgb_image.path)
    result = adaptor.run_triple_mixed_image_part1(image)
    return result


def run_triple2(job, part1_result):
    params = TripleParameters.objects.get(batch=job.batch)
    result = adaptor.run_triple_part2(part1_result, params.limit)
    return result


@task()
def run_triple3(job, part2_result):
    params = TripleParameters.objects.get(batch=job.batch)
    correlation = Correlation.objects.get(batch=job.batch, color=Correlation.RGB)
    result = adaptor.run_triple_part3(part2_result, params.range_val, params.g0, params.w, params.ginf)
    _save_result(correlation, job, result)


@task()
def run_batch(batch):
    dual_params = DualParameters.objects.get(batch=batch)
    triple_params = TripleParameters.objects.get(batch=batch)
    config = Config()
    config.side = batch.image_size
    config.input_directory = batch.get_inputs_path()
    config.output_directory = batch.get_results_path()
    config.name_min = batch.start
    config.name_max = batch.stop
    config.name_format = batch.name_format
    config.dual_range = dual_params.range_val
    config.triple_range = triple_params.range_val
    config.auto_consider_deltas = dual_params.auto_deltas
    config.cross_consider_deltas = dual_params.cross_deltas
    config.dual_initial = numpy.array([dual_params.g0, dual_params.w, dual_params.ginf, 0, 0], dtype=numpy.float)
    config.triple_initial = numpy.array([triple_params.g0, triple_params.w, triple_params.ginf], dtype=numpy.float)
    config.triple_lim = triple_params.limit
    config.input_type = batch.image_type

    batch.state = Batch.RUNNING
    batch.save()

    batch_runner = batchRunner.BatchRunner(config)
    batch_runner.runAll()

    batch.state =  Batch.COMPLETE
    batch.save()
