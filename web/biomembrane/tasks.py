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
from models import Correlation, DualParameters, Result
from django.core.files.base import ContentFile
from midend import adaptor
import PIL.Image
import StringIO


@task()
def run_dual(job):
    params = DualParameters.ojects.get(batch=job.batch)
    correlations = Correlation.objects.filter(batch=job.batch).exclude(color=Correlation.RGB)
    image = PIL.Image.open(job.rgb_image.open())

    for c in correlations:
       r = adaptor.run_dual_mixed_image(image, c.color, params.g0, params.w, params.ginf, params.range_val, params.use_deltas)
       data = StringIO()
       fit = StringIO()
       r.saveDataFileLike(data, fit)
       data.seek(0)
       fit.seek(0)
       graph = r.plotToStringIO()
       result = Result(correlation=c, job=job)
       result.data_file.save('data.txt', ContentFile(data.read()))
       result.fit_file.save('fit.txt', ContentFile(fit.read()))
       result.graph_image.save('graph.png', ContentFile(graph.read()))
       result.save()
