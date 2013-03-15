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
import os


def generate_file_path(instance, filename):
    # TODO: Depends on file extension
    id = instance.job.batch.id
    number = instance.job.number
    image_type = instance.image_type
    extension = filename.split('.')[-1]

    if image_type == Image.RED:
        new_filename = 'r.'
    elif image_type == Image.GREEN:
        new_filename = 'g.'
    elif image_type == Image.BLUE:
        new_filename = 'b.'
    else:
        new_filename = 'rgb.'

    new_filename += extension
    path = '/'.join([id, number, new_filename])
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
    red = models.TextField()
    green = models.TextField()
    blue = models.TextField()
    batch = models.ForeignKey(Batch)

    def __unicode__(self):
        return unicode(self.number)


class Images(models.Model):
    red = models.ImageField(upload_to=generate_file_path)
    green = models.ImageField(upload_to=generate_file_path)
    blue = models.ImageField(upload_to=generate_file_path)
    rgb = models.ImageField(upload_to=generate_file_path)
    job = models.ForeignKey(Job)


class Parameters(models.Model):
    AUTO, CROSS, TRIPLE = u'a', u'c', u't'
    CORRELATION_TYPES = (
        (AUTO, u'Auto'),
        (CROSS, u'Cross'),
        (TRIPLE, u'Triple')
    )

    correlationType = models.CharField(max_length=1, choices=CORRELATION_TYPES)
    red = models.BooleanField()
    green = models.BooleanField()
    blue = models.BooleanField()
    range_val = models.FloatField()
    g0 = models.FloatField()
    w = models.FloatField()
    ginf = models.FloatField()
    limit = models.FloatField()
    use_deltas = models.BooleanField()
    batch = models.ForeignKey(Batch)

    def __unicode__(self):
        return self.correlationType


class Results(models.Model):
    par = models.TextField()
    out = models.TextField()
    fit = models.TextField()
    fit_before_reshape = models.TextField()
    res_norm = models.TextField()
    used_deltas = models.TextField()
    params = models.ForeignKey(Parameters)
    job = models.ForeignKey(Job)
