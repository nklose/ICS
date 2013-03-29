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
from django.http import HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from icsform import RgbSettingsForm, BatchSettingsForm;
from models import Batch, Job, DualParameters, TripleParameters, Correlation
import scipy.misc
import icsform
import models
import image_utils
try:
    from StringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO
import zipfile

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

                rangeVal = form.cleaned_data['rangeAuto']
                gzero = form.cleaned_data['gzeroAuto']
                w = form.cleaned_data['wAuto']
                ginf = form.cleaned_data['ginfAuto']

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, use_deltas=considerDeltas).save()

                if redChecked:
                    Correlation(batch=batch, color=Correlation.R).save()
                if greenChecked:
                    Correlation(batch=batch, color=Correlation.G).save()
                if blueChecked:
                    Correlation(batch=batch, color=Correlation.B).save()

                #Do Auto with parameters above
                return HttpResponseRedirect('/results/') #redirect results view

            elif form.isCross():
                #Cross correlations only forms
                redgreenChecked = form.cleaned_data['redgreen'];
                redblueChecked = form.cleaned_data['redblue']
                greenblueChecked = form.cleaned_data['greenblue']
                considerDeltas = form.cleaned_data['deltaCross'] #check this boolean

                rangeVal = form.cleaned_data['rangeCross']
                gzero = form.cleaned_data['gzeroCross']
                w = form.cleaned_data['wCross']
                ginf = form.cleaned_data['ginfCross']

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, use_deltas=considerDeltas).save()

                if redgreenChecked:
                    Correlation(batch=batch, color=Correlation.RG).save()
                if redblueChecked:
                    Correlation(batch=batch, color=Correlation.RB).save()
                if greenblueChecked:
                    Correlation(batch=batch, color=Correlation.GB).save()

                #Do Cross Correlation with above parameters
                return HttpResponseRedirect('/results/') #redirect results view

            elif form.isTriple():
                #Triple correlations only
                #Redirect to tripleSetRes (Triple Sample Resolution)
                Correlation(batch=batch, color=Correlation.RGB).save()
                return HttpResponseRedirect('/triple/setRes/')

            elif form.isAll():
                #All correlations form
                considerDeltas = form.cleaned_data['deltaAll']

                rangeVal = form.cleaned_data['rangeAutoCrossAll']
                gzero = form.cleaned_data['gzeroAutoCrossAll']
                w = form.cleaned_data['wAutoCrossAll']
                ginf = form.cleaned_data['ginfAutoCrossAll']

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, use_deltas=considerDeltas).save()

                Correlation(batch=batch, color=Correlation.R).save()
                Correlation(batch=batch, color=Correlation.G).save()
                Correlation(batch=batch, color=Correlation.B).save()
                Correlation(batch=batch, color=Correlation.RG).save()
                Correlation(batch=batch, color=Correlation.RB).save()
                Correlation(batch=batch, color=Correlation.GB).save()
                Correlation(batch=batch, color=Correlation.RGB).save()

                #Redirect to tripleSetRes (Ask User for Triple's Sample Resolution)
                return HttpResponseRedirect('/triple/setRes/') # see tripleSetRes view function
    else:
         form = RgbSettingsForm()
    
    batch = Batch.objects.get(id=request.session['batch_id'])
    job = Job.objects.get(batch=batch)
    images = {}
    images['RGB'] = {}
    images['RGB']['url'] = job.rgb_image.url
    images['Red'] = {}
    images['Red']['url'] = job.red_image.url
    images['Green'] = {}
    images['Green']['url'] = job.green_image.url
    images['Blue'] = {}
    images['Blue']['url'] = job.blue_image.url

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
            TripleParameters(batch=batch, limit=resolution).save()
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
            rangeVal = form.cleaned_data['rangeTriple']
            gzero= form.cleaned_data['gzeroTriple']
            w= form.cleaned_data['wTriple']
            ginf= form.cleaned_data['ginfTriple']
            batch = Batch.objects.get(id=request.session['batch_id'])
            params = TripleParameters.objects.get(batch=batch)
            params.range_val = rangeVal
            params.g0 = gzero
            params.w = w
            params.ginf = ginf
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
                
                job = models.Job(number=1, batch=batch, state=models.Job.UPLOADING)
                job.red_image.save('r.png', ContentFile(image_utils.image_to_string_io(redImage).read()))
                job.green_image.save('g.png', ContentFile(image_utils.image_to_string_io(greenImage).read()))
                job.blue_image.save('b.png', ContentFile(image_utils.image_to_string_io(blueImage).read()))
                job.rgb_image.save('rgb.png', ContentFile(image_utils.image_to_string_io(rgbImage).read()))
                job.save()

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

                job = models.Job(number=1, batch=batch, state=models.Job.UPLOADING) 
                job.red_image.save('r.png', ContentFile(image_utils.image_to_string_io(redImage).read()))
                job.green_image.save('g.png', ContentFile(image_utils.image_to_string_io(greenImage).read()))
                job.blue_image.save('b.png', ContentFile(image_utils.image_to_string_io(blueImage).read()))
                job.rgb_image.save('rgb.png', ContentFile(image_utils.image_to_string_io(rgbImage).read()))
                job.save()

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

           # Take upload as zip file
           zipdata = form.cleaned_data['zip_file']
           # Run Batch with settings

           # Reading each file in the zip file
           myzip = zipfile.ZipFile(zipdata)
           for filename in myzip.namelist():
               # Do something here with each file in the .ZIP archive.
               #
               # For example, if you expect the archive to contain image
               # files, you could process each one with PIL, then create
               # and create jobs for each.
               data = myzip.read(filename)
               
           myzip.close()
            
           # Redirect to batch result
           
           return HttpResponseRedirect('/results/') # redirect after post
    else:
        form = BatchSettingsForm()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Batch Mode", "form": form}
    return render(request, 'batch.html', temp)
