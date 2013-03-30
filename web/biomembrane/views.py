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
from django.conf import settings
from icsform import RgbSettingsForm, BatchSettingsForm;
from models import Batch, Job, DualParameters, TripleParameters, Correlation, TempResult
from os import listdir
import os.path
import scipy.misc
import PIL.Image
import icsform
import models
import image_utils
try:
    from StringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO
import zipfile
import tasks

@login_required(login_url='/accounts/login/')
def program(request):

    """ Renders the ICS Program view.
         Template: /web/web/templates/layout.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section.
    """

    if 'batch_id' not in request.session:
        return HttpResponseRedirect('/rgb_upload/')
        
    batch = Batch.objects.get(id=request.session['batch_id'])
    job = Job.objects.get(batch=batch)

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

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, auto_deltas=considerDeltas).save()

                if redChecked:
                    Correlation(batch=batch, color=Correlation.R).save()
                if greenChecked:
                    Correlation(batch=batch, color=Correlation.G).save()
                if blueChecked:
                    Correlation(batch=batch, color=Correlation.B).save()

                tasks.run_dual.delay(job)

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

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, cross_deltas=considerDeltas).save()

                if redgreenChecked:
                    Correlation(batch=batch, color=Correlation.RG).save()
                if redblueChecked:
                    Correlation(batch=batch, color=Correlation.RB).save()
                if greenblueChecked:
                    Correlation(batch=batch, color=Correlation.GB).save()

                tasks.run_dual.delay(job)

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

                DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, auto_deltas=considerDeltas, cross_deltas=considerDeltas).save()

                Correlation(batch=batch, color=Correlation.R).save()
                Correlation(batch=batch, color=Correlation.G).save()
                Correlation(batch=batch, color=Correlation.B).save()
                Correlation(batch=batch, color=Correlation.RG).save()
                Correlation(batch=batch, color=Correlation.RB).save()
                Correlation(batch=batch, color=Correlation.GB).save()
                Correlation(batch=batch, color=Correlation.RGB).save()

                tasks.run_dual.delay(job)

                #Redirect to tripleSetRes (Ask User for Triple's Sample Resolution)
                return HttpResponseRedirect('/triple/setRes/') # see tripleSetRes view function
    else:
         form = RgbSettingsForm()
    
    batch = Batch.objects.get(id=request.session['batch_id'])
    job = Job.objects.get(batch=batch)
    images = [job.rgb_image.url, job.red_image.url, job.green_image.url, job.blue_image.url]
    imageAttrs = {}
    image = PIL.Image.open(job.rgb_image.path)
    intensities = image_utils.get_intensities(image)
    imageAttrs['size'] = str(image.size[0]) + 'x' + str(image.size[1])
    imageAttrs['red'] = intensities[0]
    imageAttrs['green'] = intensities[1]
    imageAttrs['blue'] = intensities[2]

    temp = {"sec_title": "Image Correlation Spectroscopy Program","form": form, "rgbimgs": images, "imgAttrs": imageAttrs}
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

    if 'batch_id' not in request.session:
        return HttpResponseRedirect('/rgb_upload/')

    batch = Batch.objects.get(id=request.session['batch_id'])

    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST, request.FILES)
        form.paramsSettingState = False # Don't require triple correlation parameters from user at this point/state
        if form.is_valid():
            resolution = form.selectedResolution() #get the sample resolution as 16,32,64
            TripleParameters(batch=batch, limit=resolution).save()
            #Redirect to tripleSetParams (Triple Parameters)
            return HttpResponseRedirect('/triple/setParams/') 
    else:
        form = RgbSettingsForm()

    job = Job.objects.get(batch=batch)
    try:
        temp = TempResult.objects.get(job=job)
    except TempResult.DoesNotExist: 
        triple1 = tasks.run_triple1(job)
        request.session['triple1'] = triple1 
        temp = TempResult(job=job)
        temp.first_graph.save('triple1.png', ContentFile(triple1.plotToStringIO().read()))
        temp.save()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Triple Correlation Set Resolution To Sample", "form": form, "graph_path": temp.first_graph.url}
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
    if 'batch_id' not in request.session:
        return HttpResponseRedirect('/rgb_upload/')

    batch = Batch.objects.get(id=request.session['batch_id'])
    job = Job.objects.get(batch=batch)

    if request.method == 'POST':  #form has been submitted
        form = RgbSettingsForm(request.POST, request.FILES)
        form.paramsSettingState = True # require triple correlation parameters from users at this state
        params = TripleParameters.objects.get(batch=batch)
        form.setResolutionSize = params.limit #set the resolution to batch 
        if form.is_valid():
            # Update Triple Correlation Parameters Here
            rangeVal = form.cleaned_data['rangeTriple']
            gzero= form.cleaned_data['gzeroTriple']
            w= form.cleaned_data['wTriple']
            ginf= form.cleaned_data['ginfTriple']
            params = TripleParameters.objects.get(batch=batch)
            params.range_val = rangeVal
            params.g0 = gzero
            params.w = w
            params.ginf = ginf
            params.save()
            tasks.run_triple3.delay(job, request.session['triple2'])
            return HttpResponseRedirect('/results/') # redirect after post
    else:
        form = RgbSettingsForm()

    temp = TempResult.objects.get(job=job)
    if temp.second_graph == '':
        triple1 = request.session['triple1']
        triple2 = tasks.run_triple2(job, triple1)
        request.session['triple2'] = triple2 
        temp.second_graph.save('triple2.png', ContentFile(triple2.plotToStringIO().read()))
        temp.save()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Triple Correlation Set Parameters", "form": form, "graph_path": temp.second_graph.url}
    return render(request, 'tripleSetParameters.html', temp)

def home(request):
    """ Renders a home  view.
         Template: /web/web/templates/homepage.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
    """
    temp = {"sec_title": "Image Correlation Spectroscopy Program | Welcome to the Homepage",}
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
                
                job = models.Job(number=1, batch=batch)
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
                redImage, greenImage, blueImage = image_utils.create_images(r, g, b)

                job = models.Job(number=1, batch=batch) 
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
            resolution = form.selectedResolution() #the size to sample for triple correlation
            firstImageIndex = form.cleaned_data['firstImageIndex'] #which image file number to start at (suppose they skip some)
            lastImageIndex = form.cleaned_data['lastImageIndex'] #which image file number to end at
 
            # Auto and Cross Parameters
            rangeVal = form.cleaned_data['rangeAutoCross']
            gzero = form.cleaned_data['gzeroAutoCross']
            w = form.cleaned_data['wAutoCross']
            ginf = form.cleaned_data['ginfAutoCross']
            deltaAuto = form.cleaned_data['considerDeltaForAuto'] #check this boolean
            deltaCross = form.cleaned_data['considerDeltaForCross'] #check this boolean
 
            rangeTriple = form.cleaned_data['rangeTriple']
            gzeroTriple = form.cleaned_data['gzeroTriple']
            wTriple = form.cleaned_data['wTriple']
            ginfTriple = form.cleaned_data['ginfTriple']
 
            batch = Batch(user=request.user, state=Batch.UPLOADING)
            batch.image_type = Batch.MIXED
            batch.image_size = imageSize
            batch.start = firstImageIndex
            batch.stop = lastImageIndex
            batch.name_format = filenameFormat
            batch.save()
 
            DualParameters(batch=batch, range_val=rangeVal, g0=gzero, w=w, ginf=ginf, auto_deltas=deltaAuto, cross_deltas=deltaCross).save()
            TripleParameters(batch=batch, range_val=rangeTriple, g0=gzeroTriple, w=wTriple, ginf=ginfTriple, limit=resolution).save()

            # Take upload as zip file
            zipdata = form.cleaned_data['zip_file']
 
            # Reading each file in the zip file
            with zipfile.ZipFile(zipdata) as zipf:
                path = os.path.join(settings.MEDIA_ROOT, batch.get_inputs_path())
                zipf.extractall(path)
                image_path = os.path.join(path, listdir(path)[0])
                image = PIL.Image.open(image_path)
                if len(image.getbands()) == 3:
                    batch.image_type = Batch.MIXED
                else:
                    batch.image_type = Batch.SINGLE
                batch.save()

            tasks.run_batch.delay(batch)
             
            return HttpResponseRedirect('/results/') # redirect after post
    else:
        form = BatchSettingsForm()

    temp = {"sec_title": "Image Correlation Spectroscopy Program | Batch Mode", "form": form}
    return render(request, 'batch.html', temp)

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
    #if 'batch_id' not in request.session:
        #return HttpResponseRedirect('/rgb_upload/')
    
    temp = {"sec_title": "Image Correlation Spectroscopy Program | Results", "copyrightdate": 2013,}
    return render(request, 'results.html', temp)


@login_required(login_url='/accounts/login/')
def batchResults(request):
    """ Renders a home  view.
         Template: /web/web/templates/batchResults.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
        - copyrightdate: The year of copyright.
    """
    
    temp = {"sec_title": "", "copyrightdate": 2013,}
    return render(request, 'batch_results.html', temp)

def help(request):
    """ Renders a documentation help page view.
         Template: /web/web/templates/help.html

         Request parameters (ie, parameters in the request object):
         - None

         Context parameters (ie, keys in the dictionary passed to the template):
        - sec_ title: The title of the section
    """
    temp = {"sec_title": "Image Correlation Spectroscopy Program | Documentation",}
    return render(request, 'help.html', temp)
