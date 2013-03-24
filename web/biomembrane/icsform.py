from django import forms
import formfields


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



class RgbSettingsForm(forms.Form):

    """ Renders a home  view.
         A set of forms used in program view

         forms.Form
         - None
    """

    red = forms.BooleanField(required=False, initial=True)
    blue = forms.BooleanField(required=False, initial=True)
    green = forms.BooleanField(required=False, initial=True)
    redgreen = forms.BooleanField(required=False, initial=True)
    redblue = forms.BooleanField(required=False, initial=True)
    greenblue = forms.BooleanField(required=False, initial=True)
    all = forms.BooleanField(required=False, initial=True)
    deltaAuto = forms.BooleanField(required=False)
    deltaCross = forms.BooleanField(required=False)
    deltaTriple = forms.BooleanField(required=False)
    deltaAll = forms.BooleanField(required=False)

    userSelected = forms.CharField(required=False) # field containing the id of the type of correlation the user selects
    rangeAuto = forms.FloatField(required=False)  # parameters for auto correlation
    gzeroAuto = forms.FloatField(required=False)
    wAuto = forms.FloatField(required=False)
    ginfAuto = forms.FloatField(required=False)

    rangeCross = forms.FloatField(required=False) # parameters when only the cross correlation option is selected
    gzeroCross  = forms.FloatField(required=False)
    wCross = forms.FloatField(required=False)
    ginfCross= forms.FloatField(required=False)

    rangeTriple = forms.FloatField(required=False) # parameters when only triple correlation when option is selected
    gzeroTriple = forms.FloatField(required=False)
    wTriple = forms.FloatField(required=False)
    ginfTriple = forms.FloatField(required=False)

    rangeAutoCrossAll = forms.FloatField(required=False) # parameters for auto and cross when the "all correlation" option is selected
    ginfAutoCrossAll = forms.FloatField(required=False)
    wAutoCrossAll = forms.FloatField(required=False)
    gzeroAutoCrossAll = forms.FloatField(required=False)

    rangeTripleAll = forms.FloatField(required=False) # parameters for triple when the "all correlation" option is selected.
    gzeroTripleAll = forms.FloatField(required=False)
    wTripleAll = forms.FloatField(required=False)
    ginfTripleAll = forms.FloatField(required=False)


    SIXTEEN, THIRTYTWO, SIXTYFOUR = u'16x16', u'32x32', u'64x64'
    RESOLUTIONS  = (     # set options for the user to specify sample for triple correlation
        (SIXTEEN, u'16x16'),
        (THIRTYTWO, u'32x32'),
        (SIXTYFOUR, u'64x64'),
    )

    resolutions = forms.ChoiceField(initial=SIXTYFOUR, choices=RESOLUTIONS)

    def selectedResolution(self):
       if self.cleaned_data['resolutions'] == SIXTEEN:
          return 16
       elif self.cleaned_data['resolutions'] == THIRTYTWO:
          return 32
       elif self.cleaned_data['resolutions'] == SIXTYFOUR:
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
        if self.cleaned_data['userSelected'] == 'id_triple':
           return True
        else:
           return False

    def isAll(self):
        if self.cleaned_data['userSelected'] == 'id_all':
           return True
        else:
           return False


class BatchSettingsForm(forms.Form):
    imageSize = forms.IntegerField();
    firstImageIndex = forms.IntegerField(); # name_min in batch
    lastImageIndex = forms.IntegerField(); #  name_max in batch
    filenameFormat = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'rgb_{:03d}.bmp'}))
    considerDeltaForAuto = forms.BooleanField(initial=False)
    considerDeltaForCross = forms.BooleanField(initial=False)

    rangeAutoCross = forms.FloatField(initial=20) # parameters for auto and cross
    ginfAutoCross = forms.FloatField(initial=10)
    wAutoCross = forms.FloatField(initial=0)
    gzeroAutoCross = forms.FloatField(initial=20)

    rangeTriple = forms.FloatField(initial=15) # parameters for triple when the "all correlation" option is selected.
    gzeroTriple = forms.FloatField(initial=0)
    wTriple = forms.FloatField(initial=0)
    ginfTriple = forms.FloatField(initial=0)

    SIXTEEN, THIRTYTWO, SIXTYFOUR = u'16x16', u'32x32', u'64x64'
    RESOLUTIONS  = (     # set options for the user to specify sample for triple correlation
        (SIXTEEN, u'16x16'),
        (THIRTYTWO, u'32x32'),
        (SIXTYFOUR, u'64x64'),
    )

    resolutions = forms.ChoiceField(initial=SIXTYFOUR, choices=RESOLUTIONS)

    def selectedResolution(self):
       if self.cleaned_data['resolutions'] == SIXTEEN:
          return 16
       elif self.cleaned_data['resolutions'] == THIRTYTWO:
          return 32
       elif self.cleaned_data['resolutions'] == SIXTYFOUR:
          return 64
       else:
          return None;
