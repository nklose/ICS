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
from django.db import models
from django.contrib.auth.models import User


def generate_image_path(instance, filename):
    id = instance.batch.id
    number = instance.number
    path = '/'.join([unicode(id), unicode(number), filename])
    return path


def generate_result_path(instance, filename):
    id = instance.job.batch.id
    number = instance.job.number
    color = instance.correlation.color
    path = '/'.join([unicode(id), unicode(number), 'results', color, filename])
    return path


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.date.__str__())


class Job(models.Model):
    UPLOADING, RUNNING, COMPLETE = u'u', u'r', u'c'
    JOB_STATES = (
        (UPLOADING, u'Uploading'),
        (RUNNING, u'Running'),
        (COMPLETE, u'Complete')
    )

    number = models.IntegerField()
    state = models.CharField(max_length=1, choices=JOB_STATES)
    red_image = models.ImageField(upload_to=generate_image_path)
    green_image = models.ImageField(upload_to=generate_image_path)
    blue_image = models.ImageField(upload_to=generate_image_path)
    rgb_image = models.ImageField(upload_to=generate_image_path)
    batch = models.ForeignKey(Batch)

    def __unicode__(self):
        return unicode(self.number)


class Correlation(models.Model):
    R, G, B, RG, RB, GB, RGB = 'r', 'g', 'b', 'rg', 'rb', 'gb', 'rgb'
    COLORS = (
        (R, u'Red'),
        (G, u'Green'),
        (B, u'Blue'),
        (RG, u'Red/Green'),
        (RB, u'Red/Blue'),
        (GB, u'Green/Blue'),
        (RGB, u'Red/Green/Blue')
    )

    color = models.CharField(max_length=3, choices=COLORS)
    batch = models.ForeignKey(Batch)


class DualParameters(models.Model):
    range_val = models.FloatField(null=True, blank=True)
    g0 = models.FloatField(null=True, blank=True)
    w = models.FloatField(null=True, blank=True)
    ginf = models.FloatField(null=True, blank=True)
    use_deltas = models.BooleanField(blank=True)
    batch = models.ForeignKey(Batch)


class TripleParameters(DualParameters):
    limit = models.IntegerField()


class Result(models.Model):
    data_file = models.FileField(upload_to=generate_result_path)
    fit_file = models.FileField(upload_to=generate_result_path)
    graph_image = models.ImageField(upload_to=generate_result_path)
    correlation = models.ForeignKey(Correlation)
    job = models.ForeignKey(Job)
