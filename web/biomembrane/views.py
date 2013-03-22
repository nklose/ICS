""" Contains all views for the webservice version of ICS.

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
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, Http404, HttpResponse
from pickle import dumps
from icsform import RgbSettingsForm, BatchSettingsForm;
import scipy.misc
import StringIO
import icsform
import models
import image_utils

def program(request):

    """ Renders a test view.
         Template: /web/web/templates/layout.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
        - copyrightdate: The Year of copyright
    """
    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST)
        if form.is_valid():
        # proccess the data in form.cleaned_data
        # ...
          return HttpResponseRedirect('/proccess/') # redirect after post
    else:
        form = RgbSettingsForm()
    temp = {"sec_title": "Image Correlation Spectroscopy Program", "copyrightdate": 2013, "form": form}
    return render(request, 'icslayout.html', temp)


def home(request):
    """ Renders a home  view.
         Template: /web/web/templates/homepage.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
        - copyrightdate: The year of copyright.
    """
    temp = {"sec_title": "Welcome to the Homepage", "copyrightdate": 2013,}
    return render(request, 'homepage.html', temp)

def rgb_upload(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = icsform.SampleImageForm(request.POST, request.FILES)
        if form.is_valid():
            # All validation rules pass
            print form.isSingleUpload()
            if form.isSingleUpload():
                batch = models.Batch(user=None) # create a new batch
                batch.save()

                # Process the data in form.cleaned_data
                rgbImage = form.cleaned_data['mixedImg']
                # Change to scipy image:
                rgb = scipy.misc.fromimage(rgbImage)
                r, g, b = image_utils.get_channels(rgb) # generate the three channels
                redImage, greenImage, blueImage = image_utils.create_images(r, g, b) #create the images
                
                singleJob = models.Job(batch=batch,
                                       state=models.Job.UPLOADING,
                                       red=dumps(r),
                                       green=dumps(g),
                                       blue=dumps(b))
                io = StringIO.StringIO()
                redImage.save(io, format='PNG')
                singleJob.red_image.save('r.png', io)
                greenImage.save(io, format='PNG')
                singleJob.green_image.save('g.png', io)
                blueImage.save(io, format='PNG')
                singleJob.blue_image.save('b.png', io)
                rgbImage.save(io, format='PNG')
                singleJob.rgb_image.save('rgb.png', io)
                singleJob.save()

                return HttpResponseRedirect('/program/')
            elif form.isMultipleUpload():
                batch = models.Batch(user=None) # create a new batch
                batch.save()

                # Proccess the three image data in form.cleaned_data
                redImage = form.cleaned_data['redImg']
                greenImage = form.cleaned_data['greenImg']
                blueImage = form.cleaned_data['blueImg']
                r = scipy.misc.fromimage(redImage)
                g = scipy.misc.fromimage(greenImage)
                b = scipy.misc.fromimage(blueImage)
                rgbImage = image_utils.create_image(r, g, b)

                singleJob = models.Job(batch=batch,
                                       state=models.Job.UPLOADING, 
                                       red=dumps(r),
                                       green=dumps(g),
                                       blue=dumps(b))
                io = StringIO.StringIO()
                redImage.save(io, format='PNG')
                singleJob.red_image.save('r.png', io)
                greenImage.save(io, format='PNG')
                singleJob.green_image.save('g.png', io)
                blueImage.save(io, format='PNG')
                singleJob.blue_image.save('b.png', io)
                rgbImage.save(io, format='PNG')
                singleJob.rgb_image.save('rgb.png', io)
                singleJob.save()

                return HttpResponseRedirect('/program/')
            else:
                image = None
        else:
            image = None
    else:
        form = icsform.SampleImageForm()  # An unbound form
        #sciImg = None

    temp = {"sec_title": "Image Upload", "copyrightdate": 2013,
            "form": form}
    return render(request, 'rgb_upload.html', temp)

def results(request):
    """ Renders a home  view.
         Template: /web/web/templates/results.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
        - copyrightdate: The year of copyright.
    """
    temp = {"sec_title": "Results", "copyrightdate": 2013,}
    return render(request, 'results.html', temp)

def batch(request):
    """ Renders a home  view.
         Template: /web/web/templates/results.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
        - copyrightdate: The year of copyright.
    """
    if request.method == 'POST':  #form has been submitted
        form = BatchSettingsForm(request.POST)
        if form.is_valid():
        # proccess the data in form.cleaned_data
        # ...
          return HttpResponseRedirect('/proccess/') # redirect after post
    else:
        form = BatchSettingsForm()

    temp = {"sec_title": "Batch Mode", "copyrightdate": 2013, "form": form}
    return render(request, 'batch.html', temp)
