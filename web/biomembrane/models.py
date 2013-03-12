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
import pickle
import image_reader


def generate_file_path(instance, filename):
	""" Return something useful here """


class Batch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(date.__str__())


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
        return unicode(number)


class Image(models.Model):
    RED, GREEN, BLUE, RGB = u'r', u'g', u'b', u'rgb'
    IMAGE_TYPES = (
        (RED, u'Red'),
        (GREEN, u'Green'),
        (BLUE, u'Blue'),
        (RGB, u'Red/Green/Blue')
    )

    data = models.ImageField(upload_to=generate_file_path)
    image_type = models.CharField(max_length=3, choices=IMAGE_TYPES)
    job = models.ForeignKey(Job)

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        if image_type == RED:
            job.red = pickle.dumps(image_reader.get_channel(data.name))
        elif image_type == GREEN:
            job.green = pickle.dumps(image_reader.get_channel(data.name))
        elif image_type == BLUE:
            job.blue = pickle.dumps(image_reader.get_channel(data.name))
        else:
            r, g, b = image_reader.get_channels(data.name)
            job.red = pickle.dumps(r)
            job.green = pickle.dumps(g)
            job.blue = pickle.dumps(b)
        job.save()

    def __unicode__(self):
        return self.imageType


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
    g = models.FloatField()
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
    res_norm = models.TextField()
    used_deltas = models.TextField()
    params = models.ForeignKey(Parameters)
    job = models.ForeignKey(Job)
