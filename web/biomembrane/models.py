from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
	JOB_STATES = (
		(u'u', u'Uploading'),
		(u'r', u'Running'),
		(u'c', u'Complete')
	)

	state = models.CharField(max_length=1, choices=JOB_STATES)
	outputDir = models.CharField(max_length=255)
	user = models.ForeignKey(User)

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
