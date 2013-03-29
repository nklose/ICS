from django import forms
import formfields

try:
    from StringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO
import zipfile

class SampleImageForm(forms.Form):

    redImg = formfields.LosslessImageField(required=False, isSingleChannel=True)
    greenImg = formfields.LosslessImageField(required=False,
                                             isSingleChannel=True)
    blueImg = formfields.LosslessImageField(required=False,
                                            isSingleChannel=True)
    mixedImg = formfields.LosslessImageField(required=False)

    uploadType = forms.CharField()

    def isSingleUpload(self):
        if self.cleaned_data['uploadType'] == 'id_singleRGB':
           return True
        else:
           return False

    def isMultipleUpload(self):
        if self.cleaned_data['uploadType'] == 'id_threeRGB':
           return True
        else:
           return False

    def clean(self):
        cleaned_data = super(SampleImageForm, self).clean()
        if self.isSingleUpload():
           if cleaned_data.get("mixedImg") == None:
               msg = 'Please specify a mixed image to upload'
               self._errors["mixedImg"] = self.error_class([msg])
               del cleaned_data["mixedImg"]

        if self.isMultipleUpload():
           if cleaned_data.get("redImg") == None:
               msg = 'Please specify a red image to upload'
               self._errors["redImg"] = self.error_class([msg])
               del cleaned_data["redImg"]

           if cleaned_data.get("greenImg") == None:
               msg = 'Please specify a green image to upload'
               self._errors["greenImg"] = self.error_class([msg])
               del cleaned_data["greenImg"]

           if cleaned_data.get("blueImg") == None:
               msg = 'Please specify a blue image to upload'
               self._errors["blueImg"] = self.error_class([msg])
               del cleaned_data["blueImg"]

        return cleaned_data

class RgbSettingsForm(forms.Form):

    """ A set of forms used in program view

         forms.Form
         - None
    """

    red = forms.BooleanField(required=False, initial=True)
    blue = forms.BooleanField(required=False, initial=True)
    green = forms.BooleanField(required=False, initial=True)
    redgreen = forms.BooleanField(required=False, initial=True)
    redblue = forms.BooleanField(required=False, initial=True)
    greenblue = forms.BooleanField(required=False, initial=True)
    allChannels = forms.BooleanField(required=False, initial=True)
    deltaAuto = forms.BooleanField(required=False)
    deltaCross = forms.BooleanField(required=False)
    deltaAll = forms.BooleanField(required=False)

    userSelected = forms.CharField(required=False,error_messages={'blank': 'Please select a fit'}) # field containing the id of the type of correlation the user selects
    rangeAuto = forms.FloatField(required=False, initial=20)  # parameters for auto correlation
    gzeroAuto = forms.FloatField(required=False, initial=1)
    wAuto = forms.FloatField(required=False, initial=10)
    ginfAuto = forms.FloatField(required=False, initial=0)

    rangeCross = forms.FloatField(required=False, initial=20) # parameters when only the cross correlation option is selected
    gzeroCross  = forms.FloatField(required=False, initial=1)
    wCross = forms.FloatField(required=False, initial=10)
    ginfCross= forms.FloatField(required=False, initial=0)

    rangeTriple = forms.FloatField(required=False, initial=20) # parameters when only triple correlation when option is selected
    gzeroTriple = forms.FloatField(required=False, initial=1)
    wTriple = forms.FloatField(required=False, initial=10)
    ginfTriple = forms.FloatField(required=False, initial=0)

    rangeAutoCrossAll = forms.FloatField(required=False, initial=20) # parameters for auto and cross when the "all correlation" option is selected
    ginfAutoCrossAll = forms.FloatField(required=False, initial=0)
    wAutoCrossAll = forms.FloatField(required=False, initial=10)
    gzeroAutoCrossAll = forms.FloatField(required=False, initial=1)

    SIXTEEN, THIRTYTWO, SIXTYFOUR = u'16x16', u'32x32', u'64x64'
    RESOLUTIONS  = (     # set options for the user to specify sample for triple correlation
        (SIXTEEN, u'16x16'),
        (THIRTYTWO, u'32x32'),
        (SIXTYFOUR, u'64x64'),
    )

    resolutions = forms.ChoiceField(required=False, initial=SIXTYFOUR, choices=RESOLUTIONS)

    def selectedResolution(self):
       if self.cleaned_data['resolutions'] == self.SIXTEEN:
          return 16
       elif self.cleaned_data['resolutions'] == self.THIRTYTWO:
          return 32
       elif self.cleaned_data['resolutions'] == self.SIXTYFOUR:
          return 64
       else:
          return None;

    def _init_(self, *args, **kwargs):
        super(RgbSettingsForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['rangeAuto'].widget.attrs['cols'] = 6
        self.fields['ginfAuto'].widget.attrs['cols'] = 6
        self.fields['gzeroAuto'].widget.attrs['cols'] = 6
        self.fields['wAuto'].widget.attrs['cols'] = 6
        self.fields['rangeCross'].widget.attrs['cols'] = 6
        self.fields['ginfCross'].widget.attrs['cols'] = 6
        self.fields['gzeroCross'].widget.attrs['cols'] = 6
        self.fields['wCross'].widget.attrs['cols'] = 6
        self.fields['rangeTriple'].widget.attrs['cols'] = 6
        self.fields['ginfTriple'].widget.attrs['cols'] = 6
        self.fields['gzeroTriple'].widget.attrs['cols'] = 6
        self.fields['wTriple'].widget.attrs['cols'] = 6


    def isAuto(self):
        """ Look at cleaned data for some attribute that lets me know I should
        be using auto data.

        make an invisible input as part of the form, intercept the submit event,
        and parse and set the value of this input. OR, change it every time
        whatever you are using to determine the case changes.
        """
        if self.cleaned_data['userSelected'] == 'id_auto':
            return True
        else:
            return False

    def isCross(self):
        """ Look at cleaned data for some attribute that lets me know I should
        be using cross data.

        make an invisible input as part of the form, intercept the submit event,
        and parse and set the value of this input. OR, change it every time
        whatever you are using to determine the case changes.
        """
        if self.cleaned_data['userSelected'] == 'id_cross':
            return True
        else:
            return False

    def isTriple(self):
        """ Look at cleaned data for some attribute that lets me know I should
        be using triple data.
        """
        if self.cleaned_data['userSelected'] == 'id_triple':
           return True
        else:
           return False

    def isAll(self):
        """ Look at cleaned data for some attribute that lets me know I should
        be using all data.
        """
        if self.cleaned_data['userSelected'] == 'id_all':
           return True
        else:
           return False


class BatchSettingsForm(forms.Form):

    zip_file = forms.FileField(error_messages={'required': 'Select an zip file to upload'})
    imageSize = forms.IntegerField(error_messages={'required': 'Please input the image size of images to be fitted'});
    firstImageIndex = forms.IntegerField(error_messages={'required': 'Please specify the first image to fit'}); # name_min in batch
    lastImageIndex = forms.IntegerField(error_messages={'required': 'Please specify the last image to be fit'}); #  name_max in batch
    filenameFormat = forms.CharField(initial='rgb_{:03d}.bmp', error_messages={'required': 'Please specify the filename format for batch images'}) 
    considerDeltaForAuto = forms.BooleanField(required=False, initial=False)
    considerDeltaForCross = forms.BooleanField(required=False, initial=False)

    rangeAutoCross = forms.FloatField(initial=20) # parameters for auto and cross
    ginfAutoCross = forms.FloatField(initial=0)
    wAutoCross = forms.FloatField(initial=10)
    gzeroAutoCross = forms.FloatField(initial=1)

    rangeTriple = forms.FloatField(initial=20) # parameters for triple when the "all correlation" option is selected.
    gzeroTriple = forms.FloatField(initial=1)
    wTriple = forms.FloatField(initial=10)
    ginfTriple = forms.FloatField(initial=0)

    SIXTEEN, THIRTYTWO, SIXTYFOUR = u'16x16', u'32x32', u'64x64'
    RESOLUTIONS  = (     # set options for the user to specify sample for triple correlation
        (SIXTEEN, u'16x16'),
        (THIRTYTWO, u'32x32'),
        (SIXTYFOUR, u'64x64'),
    )

    resolutions = forms.ChoiceField(initial=SIXTYFOUR, choices=RESOLUTIONS)

    def selectedResolution(self):
       if self.cleaned_data['resolutions'] == self.SIXTEEN:
          return 16
       elif self.cleaned_data['resolutions'] == self.THIRTYTWO:
          return 32
       elif self.cleaned_data['resolutions'] == self.SIXTYFOUR:
          return 64
       else:
          return None;

    def clean_zip_file(self):
        if 'zip_file' in self.cleaned_data:
            zip_file = self.cleaned_data['zip_file']
            if zip_file.content_type != 'application/zip':
                msg = 'Only .ZIP archive files are allowed.'
                raise forms.ValidationError(msg)
            else:
                # Verify that it's a valid zipfile
                zip = zipfile.ZipFile(StringIO(zip_file.read()))
                bad_file = zip.testzip()
                zip.close()
                del zip
                if bad_file:
                    msg = '"%s" in the .ZIP archive is corrupt.' % (bad_file,)
                    raise forms.ValidationError(msg)
            return zip_file
        else:
            msg = 'Could not upload file'
            raise forms.ValidationError(msg)

