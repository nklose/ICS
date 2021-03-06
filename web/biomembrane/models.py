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
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from celery.task.control import revoke
import shutil
import os
import os.path
import zipfile


def _generate_image_path(instance, filename):
    batch = instance.batch
    path = os.path.join(batch.get_inputs_path(), filename)
    return path


def _generate_temp_path(instance, filename):
    batch = instance.job.batch
    path = os.path.join(batch.get_temp_path(), filename)
    return path 


def _generate_result_path(instance, filename):
    batch = instance.job.batch
    path = os.path.join(batch.get_results_path(), filename)
    return path


class Batch(models.Model):
    UPLOADING, RUNNING, COMPLETE = u'u', u'r', u'c'
    JOB_STATES = (
        (UPLOADING, u'Uploaded'),
        (RUNNING, u'Running'),
        (COMPLETE, u'Complete')
    )

    MIXED, SPLIT = u'mixed', u'split'
    IMAGE_TYPES = (
        (MIXED, MIXED),
        (SPLIT, SPLIT)
    )

    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=1, choices=JOB_STATES, blank=True)
    image_type = models.CharField(max_length=5, choices=IMAGE_TYPES, blank=True)
    image_size = models.IntegerField(null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    stop = models.IntegerField(null=True, blank=True)
    name_format = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey(User)

    def generate_zip(self):
        results_path = os.path.join(settings.MEDIA_ROOT, self.get_results_path())
        path_len = len(results_path) + 1
        zip_path = os.path.join(settings.MEDIA_ROOT, self.get_zip_path())
        with zipfile.ZipFile(zip_path, 'w') as zip:
            for base, dirs, files in os.walk(results_path):
                for file in files:
                    filename = os.path.join(base, file)
                    zip.write(filename, filename[path_len:])

    def get_inputs_path(self):
        return os.path.join(self.get_path(), 'inputs')

    def get_results_path(self):
        return os.path.join(self.get_path(), 'results')

    def get_temp_path(self):
        return os.path.join(self.get_path(), 'temp')

    def get_zip_path(self):
        return os.path.join(self.get_path(), 'results.zip')

    def get_path(self):
        return str(self.id)

    def __unicode__(self):
        return unicode(self.date.__str__())


@receiver(pre_delete, sender=Batch)
def on_batch_delete(sender, instance, **kwargs):
    if instance.state == Batch.RUNNING:
        revoke(instance.task_id, terminate=True)
    path = os.path.join(settings.MEDIA_ROOT, str(instance.id))
    shutil.rmtree(path)


class Job(models.Model):
    number = models.IntegerField()
    red_image = models.ImageField(upload_to=_generate_image_path)
    green_image = models.ImageField(upload_to=_generate_image_path)
    blue_image = models.ImageField(upload_to=_generate_image_path)
    rgb_image = models.ImageField(upload_to=_generate_image_path)
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


class Parameters(models.Model):
    range_val = models.FloatField(null=True, blank=True)
    g0 = models.FloatField(null=True, blank=True)
    w = models.FloatField(null=True, blank=True)
    ginf = models.FloatField(null=True, blank=True)
    batch = models.ForeignKey(Batch)

    class Meta:
        abstract = True


class DualParameters(Parameters):
    auto_deltas = models.BooleanField(blank=True)
    cross_deltas = models.BooleanField(blank=True)


class TripleParameters(Parameters):
    limit = models.IntegerField()


class TempResult(models.Model):
    first_graph = models.ImageField(upload_to=_generate_temp_path)
    second_graph = models.ImageField(upload_to=_generate_temp_path)
    job = models.ForeignKey(Job)


class Result(models.Model):
    data_file = models.FileField(upload_to=_generate_result_path)
    fit_file = models.FileField(upload_to=_generate_result_path)
    graph_image = models.ImageField(upload_to=_generate_result_path)
    correlation = models.ForeignKey(Correlation)
    job = models.ForeignKey(Job)
