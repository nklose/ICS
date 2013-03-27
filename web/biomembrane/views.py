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
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from pickle import dumps
from icsform import RgbSettingsForm, BatchSettingsForm;
from models import Batch, Job, Parameters
import scipy.misc
import icsform
import models
import image_utils
import model_utils


@login_required(login_url='/accounts/login/')
def program(request):

    """ Renders the ICS Program view.
         Template: /web/web/templates/layout.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
    """
    batch = Batch.objects.get(id=request.session['batch_id'])

    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST)
        if form.is_valid():
        # proccess the data in form.cleaned_data
            if form.isAuto():
                #Auto correlations only forms
                redChecked = form.cleaned_data['red'];
                blueChecked = form.cleaned_data['blue']
                greenChecked = form.cleaned_data['green']
                considerDeltas = form.cleaned_data['deltaAuto']

                rangeValue = form.cleaned_data['rangeAuto']
                gzeroValue = form.cleaned_data['gzeroAuto']
                wValue = form.cleaned_data['wAuto']
                ginfValue = form.cleaned_data['ginfAuto']

                if redChecked:
                    model_utils.create_params_auto(batch, model_utils.Colors.RED, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                if blueChecked:
                    model_utils.create_params_auto(batch, model_utils.Colors.GREEN, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                if greenChecked:
                    model_utils.create_params_auto(batch, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)

                #Do Auto with parameters above
                return HttpResponseRedirect('/results/') #redirect results view

            elif form.isCross():
                #Cross correlations only forms
                redgreenChecked = form.cleaned_data['redgreen'];
                redblueChecked = form.cleaned_data['redblue']
                greenblueChecked = form.cleaned_data['greenblue']
                considerDeltas = form.cleaned_data['deltaCross'] #check this boolean

                rangeValue = form.cleaned_data['rangeCross']
                gzeroValue = form.cleaned_data['gzeroCross']
                wValue = form.cleaned_data['wCross']
                ginfValue = form.cleaned_data['ginfCross']

                if redgreenChecked:
                    model_utils.create_params_cross(batch, model_utils.Colors.RED, model_utils.Colors.GREEN, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                if redblueChecked:
                    model_utils.create_params_cross(batch, model_utils.Colors.RED, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                if greenblueChecked:
                    model_utils.create_params_cross(batch, model_utils.Colors.GREEN, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)

                #Do Cross Correlation with above parameters
                return HttpResponseRedirect('/results/') #redirect results view

            elif form.isTriple():
                #Triple correlations only
                #Redirect to tripleSetRes (Triple Sample Resolution)
                return HttpResponseRedirect('/triple/setRes/')

            elif form.isAll():
                #All correlations form
                allChannelsChecked = form.cleaned_data['allChannels']
                considerDeltas = form.cleaned_data['deltaAll']

                rangeValue = form.cleaned_data['rangeAutoCrossAll']
                gzeroValue = form.cleaned_data['gzeroAutoCrossAll']
                wValue = form.cleaned_data['wAutoCrossAll']
                ginfValue = form.cleaned_data['gzeroAutoCrossAll']

                model_utils.create_params_auto(batch, model_utils.Colors.RED, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                model_utils.create_params_auto(batch, model_utils.Colors.GREEN, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                model_utils.create_params_auto(batch, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                model_utils.create_params_cross(batch, model_utils.Colors.RED, model_utils.Colors.GREEN, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                model_utils.create_params_cross(batch, model_utils.Colors.RED, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)
                model_utils.create_params_cross(batch, model_utils.Colors.GREEN, model_utils.Colors.BLUE, rangeValue, gzeroValue, wValue, ginfValue, considerDeltas)

                #Redirect to tripleSetRes (Ask User for Triple's Sample Resolution)
                return HttpResponseRedirect('/triple/setRes/') # see tripleSetRes view function
    else:
         form = RgbSettingsForm()
    
    batch = Batch.objects.get(id=request.session['batch_id'])
    job = Job.objects.get(batch=batch)
    rgbUrl = job.rgb_image.url
    redUrl = job.red_image.url
    greenUrl = job.green_image.url
    blueUrl = job.blue_image.url
    images = {}
    images['RGB'] = {}
    images['RGB']['url'] = rgbUrl
    images['Red'] = {}
    images['Red']['url'] = redUrl
    images['Green'] = {}
    images['Green']['url'] = greenUrl
    images['Blue'] = {}
    images['Blue']['url'] = blueUrl
    temp = {"sec_title": "Image Correlation Spectroscopy Program","form": form, "rgbimgs": images}
    return render(request, 'icslayout.html', temp)

@login_required(login_url='/accounts/login/')
def tripleSetRes(request):

    """ Renders the a view that asks users to input the sample resolution 
        for triple correlation.

         Template: /web/web/templates/tripleSetResolutions.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
    """
    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            resolution = form.selectedResolution() #get the sample resolution as 16,32,64
            batch = Batch.objects.get(id=request.session['batch_id'])
            params = Parameters(batch=batch, correlationType=Parameters.TRIPLE, resolution=resolution)
            params.save()
            #Redirect to tripleSetParams (Triple Parameters)
            return HttpResponseRedirect('/triple/setParams/') 
    else:
        form = RgbSettingsForm()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Triple Correlation Set Resolution To Sample", "form": form,}
    return render(request, 'tripleSetResolution.html', temp)

@login_required(login_url='/accounts/login/')
def tripleSetParams(request):
    """ Renders the a view that asks users to set parameters 
        for triple correlation

         Template: /web/web/templates/registration/login.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
    """
    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            # Update Triple Correlation Parameters Here
            rangeValue = form.cleaned_data['rangeTriple']
            gzeroValue = form.cleaned_data['gzeroTriple']
            wValue = form.cleaned_data['wTriple']
            ginfValue = form.cleaned_data['ginfTriple']
            batch = Batch.objects.get(id=request.session['batch_id'])
            params = Parameters.objects.get(batch=batch, correlationType=Parameters.TRIPLE)
            params.range_val = rangeValue
            params.g0 = gzeroValue
            params.w = wValue
            params.ginf = ginfValue
            params.save()
            return HttpResponseRedirect('/results/') # redirect after post
    else:
        form = RgbSettingsForm()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Triple Correlation Set Parameters", "form": form,}
    return render(request, 'tripleSetParameters.html', temp)


def home(request):
    """ Renders a home  view.
         Template: /web/web/templates/homepage.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
    """
    temp = {"sec_title": "Welcome to the Homepage",}
    return render(request, 'homepage.html', temp)

@login_required(login_url='/accounts/login/')
def rgb_upload(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = icsform.SampleImageForm(request.POST, request.FILES)
        if form.is_valid():
            batch = models.Batch(user=request.user) # create a new batch
            batch.save()
            request.session['batch_id'] = batch.id

            if form.isSingleUpload():
                # Process the data in form.cleaned_data
                rgbImage = form.cleaned_data['mixedImg']
                rgb = scipy.misc.fromimage(rgbImage)
                r, g, b = image_utils.get_channels(rgb) # generate the three channels
                redImage, greenImage, blueImage = image_utils.create_images(r, g, b) #create the images
                
                singleJob = models.Job(number=1,
                                       batch=batch,
                                       state=models.Job.UPLOADING,
                                       red=dumps(r),
                                       green=dumps(g),
                                       blue=dumps(b))
                singleJob.red_image.save('r.png', ContentFile(image_utils.image_to_string_io(redImage).read()))
                singleJob.green_image.save('g.png', ContentFile(image_utils.image_to_string_io(greenImage).read()))
                singleJob.blue_image.save('b.png', ContentFile(image_utils.image_to_string_io(blueImage).read()))
                singleJob.rgb_image.save('rgb.png', ContentFile(image_utils.image_to_string_io(rgbImage).read()))
                singleJob.save()

                return HttpResponseRedirect('/program/')
            else:
                # Proccess the three image data in form.cleaned_data
                redImage = form.cleaned_data['redImg']
                greenImage = form.cleaned_data['greenImg']
                blueImage = form.cleaned_data['blueImg']
                r = scipy.misc.fromimage(redImage)
                g = scipy.misc.fromimage(greenImage)
                b = scipy.misc.fromimage(blueImage)
                rgbImage = image_utils.create_image(r, g, b)

                singleJob = models.Job(number=1,
                                       batch=batch,
                                       state=models.Job.UPLOADING, 
                                       red=dumps(r),
                                       green=dumps(g),
                                       blue=dumps(b))
                singleJob.red_image.save('r.png', ContentFile(image_utils.image_to_string_io(redImage).read()))
                singleJob.green_image.save('g.png', ContentFile(image_utils.image_to_string_io(greenImage).read()))
                singleJob.blue_image.save('b.png', ContentFile(image_utils.image_to_string_io(blueImage).read()))
                singleJob.rgb_image.save('rgb.png', ContentFile(image_utils.image_to_string_io(rgbImage).read()))
                singleJob.save()

                return HttpResponseRedirect('/program/')
    else:
        form = icsform.SampleImageForm()  # An unbound form

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Image Upload",
            "form": form}
    return render(request, 'rgb_upload.html', temp)

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def batch(request):
    """ Renders a batch view.
         Template: /web/web/templates/batch.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
    """
    if request.method == 'POST':  #form has been submitted
        form = BatchSettingsForm(request.POST, request.FILES)
        if form.is_valid():
           # Proccess the data in form.cleaned_data
           # get the filenameFormat of each image file in the batch from user
           zipfile =  form.cleaned_data['zip_file']
           filenameFormat = form.cleaned_data['filenameFormat']
           imageSize = form.cleaned_data['imageSize']; #get the size of images from the user
           resolutions = form.selectedResolution() #the size to sample for triple correlation
           firstImageIndex = form.cleaned_data['firstImageIndex'] #which image file number to start at (suppose they skip some)
           lastImageIndex = form.cleaned_data['lastImageIndex'] #which image file number to end at

           # Auto and Cross Parameters
           rangeValue = form.cleaned_data['rangeAutoCross']
           gzeroValue = form.cleaned_data['gzeroAutoCross']
           wValue = form.cleaned_data['wAutoCross']
           ginfValue = form.cleaned_data['ginfAutoCross']
           deltaAuto = form.cleaned_data['considerDeltaForAuto'] #check this boolean
           deltaCross = form.cleaned_data['considerDeltaForCross'] #check this boolean

           rangeTripleValue = form.cleaned_data['rangeTriple']
           gzeroTripleValue = form.cleaned_data['gzeroTriple']
           wTripleValue = form.cleaned_data['wTriple']
           ginfTripleValue = form.cleaned_data['ginfTriple']

           # Run Batch with settings

           # Redirect to batch result
           
           return HttpResponseRedirect('/results/') # redirect after post
    else:
        form = BatchSettingsForm()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Batch Mode", "form": form}
    return render(request, 'batch.html', temp)
