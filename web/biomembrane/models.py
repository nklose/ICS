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

class Batch(models.Model):
   user = models.ForeignKey(User)

   def __unicode__(self):
       return u'<placeholder>'

class Job(models.Model):
    JOB_STATES = (
        (u'u', u'Uploading'),
        (u'r', u'Running'),
        (u'c', u'Complete')
    )

    state = models.CharField(max_length=1, choices=JOB_STATES)
    outputDir = models.CharField(max_length=255)
    batch = models.ForeignKey(Batch)

    def __unicode__(self):
        return u'<placeholder>'

class Image(models.Model):
    IMAGE_TYPES = (
        (u'r', u'Red'),
        (u'g', u'Green'),
        (u'b', u'Blue'),
        (u'rgb', u'Red/Green/Blue')
    )

    path = models.CharField(max_length=255)
    imageType = models.CharField(max_length=3, choices=IMAGE_TYPES)
    job = models.ForeignKey(Job)

    def __unicode__(self):
        return self.imageType
