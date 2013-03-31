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
               msg = u"Please specify a mixed image to upload"
               self._errors["mixedImg"] = self.error_class([msg])
               del cleaned_data["mixedImg"]

        if self.isMultipleUpload():
           if cleaned_data.get("redImg") == None:
               msg = u"Please specify a red image to upload"
               self._errors["redImg"] = self.error_class([msg])
               del cleaned_data["redImg"]

           if cleaned_data.get("greenImg") == None:
               msg = u"Please specify a green image to upload"
               self._errors["greenImg"] = self.error_class([msg])
               del cleaned_data["greenImg"]

           if cleaned_data.get("blueImg") == None:
               msg = u"Please specify a blue image to upload"
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
    paramsSettingState = False;

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

    setResolutionSize = 64;

    resolutions = forms.ChoiceField(required=False, initial=SIXTYFOUR, choices=RESOLUTIONS)

    def selectedResolution(self):
       if self.cleaned_data['resolutions'] == self.SIXTEEN:
          return 16
       elif self.cleaned_data['resolutions'] == self.THIRTYTWO:
          return 32
       elif self.cleaned_data['resolutions'] == self.SIXTYFOUR:
          return 64
       else:
          return self.setResolutionSize;

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

    def isTripleParamsRequired(self):
        """ Look at if the user has reached the state where Triple Correlation Parameter must be set
        """
        if self.paramsSettingState:
           return True
        else:
            return False

    def clean(self):
        cleaned_data = super(RgbSettingsForm, self).clean()
        
        if self.isAuto():

           if cleaned_data.get("rangeAuto") == None:
              msg = u"Must specifiy a range value for auto correlation"
              self._errors["rangeAuto"] = self.error_class([msg])
              del cleaned_data["rangeAuto"]
           elif cleaned_data.get("rangeAuto") <= 0:
              msg = u"w value should not be zero or less than zero for auto correlation"
              self._errors["rangeAuto"] = self.error_class([msg])
              del cleaned_data["rangeAuto"]

           if cleaned_data.get("gzeroAuto") == None:
              msg = u"Must specifiy a g(0) value for auto correlation"
              self._errors["gzeroAuto"] = self.error_class([msg])
              del cleaned_data["gzeroAuto"]
           elif cleaned_data.get("gzeroAuto") < 0:
              msg = u"g(0) value should not be less than zero for auto correlation"
              self._errors["gzeroAuto"] = self.error_class([msg])
              del cleaned_data["gzeroAuto"]

           if cleaned_data.get("wAuto") == None:
              msg = u"Must specifiy a w value for auto correlation"
              self._errors["wAuto"] = self.error_class([msg])
              del cleaned_data["wAuto"]
           elif cleaned_data.get("wAuto") <= 0:
              msg = u"w value should not be zero or less than zero for auto correlation"
              self._errors["wAuto"] = self.error_class([msg])
              del cleaned_data["wAuto"]

           if cleaned_data.get("ginfAuto") == None:
              msg = u"Must specifiy a ginf value for auto correlation"
              self._errors["ginfAuto"] = self.error_class([msg])
              del cleaned_data["ginfAuto"]
           elif cleaned_data.get("ginfAuto") < 0:
              msg = u"ginf value should not be less than zero for auto correlation"
              self._errors["ginfAuto"] = self.error_class([msg])
              del cleaned_data["ginfAuto"]

        elif self.isCross():

           if cleaned_data.get("rangeCross") == None:
              msg = u"Must specifiy a range value for cross correlation"
              self._errors["rangeCross"] = self.error_class([msg])
              del cleaned_data["rangeCross"]
           elif cleaned_data.get("rangeCross") <= 0:
              msg = u"range value should not be zero or less than zero for cross correlation"
              self._errors["rangeCross"] = self.error_class([msg])
              del cleaned_data["rangeCross"]


           if cleaned_data.get("gzeroCross") == None:
              msg = u"Must specifiy a g(0) value for cross correlation"
              self._errors["gzeroCross"] = self.error_class([msg])
              del cleaned_data["gzeroCross"]
           elif cleaned_data.get("gzeroCross") < 0:
              msg = u"g(0) value should not be less than zero for cross correlation"
              self._errors["gzeroCross"] = self.error_class([msg])
              del cleaned_data["gzeroCross"]

           if cleaned_data.get("wCross") == None:
              msg = u"Must specifiy a w value for cross correlation"
              self._errors["wCross"] = self.error_class([msg])
              del cleaned_data["wCross"]
           elif cleaned_data.get("wCross") <= 0:
              msg = u"w value should not be zero or less than zero for cross correlation"
              self._errors["wCross"] = self.error_class([msg])
              del cleaned_data["wCross"]

           if cleaned_data.get("ginfCross") == None:
              msg = u"Must specifiy a ginf value for cross correlation"
              self._errors["ginfCross"] = self.error_class([msg])
              del cleaned_data["ginfCross"]
           elif cleaned_data.get("ginfCross") < 0:
              msg = u"ginf value should not be zero or less than zero for cross correlation"
              self._errors["ginfCross"] = self.error_class([msg])
              del cleaned_data["ginfCross"]

        elif self.isTripleParamsRequired():

           if cleaned_data.get("rangeTriple") == None:
              msg = u"Must specifiy a range value for triple correlation"
              self._errors["rangeTriple"] = self.error_class([msg])
              del cleaned_data["rangeTriple"]
           elif cleaned_data.get("rangeTriple") > self.selectedResolution():
              msg = u"Range value should not be larger than the sample resolution for triple correlation"
              self._errors["rangeTriple"] = self.error_class([msg])
              del cleaned_data["rangeTriple"]
           elif cleaned_data.get("rangeTriple") <= 0:
              msg = u"Range value should not be zero or less than zero for triple correlation"
              self._errors["rangeTriple"] = self.error_class([msg])
              del cleaned_data["rangeTriple"]

           if cleaned_data.get("gzeroTriple") == None:
              msg = u"Must specifiy a g(0) value for triple correlation"
              self._errors["gzeroTriple"] = self.error_class([msg])
              del cleaned_data["gzeroTriple"]
           elif cleaned_data.get("gzeroTriple") < 0:
              msg = u"g(0) value should not be less than zero for triple correlation"
              self._errors["gzeroTriple"] = self.error_class([msg])
              del cleaned_data["gzeroTriple"]  


           if cleaned_data.get("wTriple") == None:
              msg = u"Must specifiy a w value for triple correlation"
              self._errors["wTriple"] = self.error_class([msg])
              del cleaned_data["wTriple"]
           elif cleaned_data.get("wTriple") <= 0:
              msg = u"w value should not be zero or less than zero for triple correlation"
              self._errors["wTriple"] = self.error_class([msg])
              del cleaned_data["wTriple"]

           if cleaned_data.get("ginfTriple") == None:
              msg = u"Must specifiy a ginf value for triple correlation"
              self._errors["ginfTriple"] = self.error_class([msg])
              del cleaned_data["ginfTriple"]
           elif cleaned_data.get("wTriple") < 0:
              msg = u"ginf value should not be less than zero for triple correlation"
              self._errors["wTriple"] = self.error_class([msg])
              del cleaned_data["wTriple"]


        elif self.isAll():

           if cleaned_data.get("rangeAutoCrossAll") == None:
              msg = u"Must specifiy a range value for the auto and cross correlation"
              self._errors["rangeAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["rangeAutoCrossAll"]
           elif cleaned_data.get("rangeAutoCrossAll") <= 0:
              msg = u"range value should not be zero or less than zero for the auto and cross correlation"
              self._errors["rangeAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["rangeAutoCrossAll"]

           if cleaned_data.get("gzeroAutoCrossAll") == None:
              msg = u"Must specifiy a g(0) value for the auto and corss correlation"
              self._errors["gzeroAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["gzeroAutoCrossAll"]
           elif cleaned_data.get("gzeroAutoCrossAll") < 0:
              msg = u"g(0) value should not be less than zero for auto and cross correlation"
              self._errors["gzeroAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["gzeroAutoCrossAll"]

           if cleaned_data.get("wAutoCrossAll") == None:
              msg = u"Must specifiy a w value for auto and cross correlation"
              self._errors["wAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["wAutoCrossAll"]
           elif cleaned_data.get("wAutoCrossAll") <= 0:
              msg = u"w value should not be zero or less than zero for auto and cross correlation"
              self._errors["wAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["wAutoCrossAll"]               

           if cleaned_data.get("ginfAutoCrossAll") == None:
              msg = u"Must specifiy a ginf value for auto and cross correlation"
              self._errors["ginfAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["ginfAutoCrossAll"]
           elif cleaned_data.get("ginfAutoCrossAll") < 0:
              msg = u"ginf value should not be less zero for auto and cross correlation"
              self._errors["ginfAutoCrossAll"] = self.error_class([msg])
              del cleaned_data["ginfAutoCrossAll"]           

        return cleaned_data
          
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

    def clean(self):
        cleaned_data = super(BatchSettingsForm, self).clean()
        if cleaned_data.get("rangeTriple") > self.selectedResolution():
              msg = u"Range value must not be larger than the sample resolution for triple correlation"
              self._errors["rangeTriple"] = self.error_class([msg])
              del cleaned_data["rangeTriple"]

        if cleaned_data.get("wTriple") == 0:
              msg = u"w value cannot be zero for triple correlation"
              self._errors["wTriple"] = self.error_class([msg])
              del cleaned_data["wTriple"]

        if cleaned_data.get("wAutoCross") == 0:
              msg = u"w value cannot be zero for auto and cross correlation"
              self._errors["wAutoCross"] = self.error_class([msg])
              del cleaned_data["wAutoCross"]

        return cleaned_data
