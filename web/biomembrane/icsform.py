from django import forms
import formfields


class SampleImageForm(forms.Form):

    redImg = formfields.LosslessImageField(required=False)
    greenImg = formfields.LosslessImageField(required=False)
    blueImg = formfields.LosslessImageField(required=False)
    mixedImg = formfields.LosslessImageField(required=False)

    uploadType = forms.CharField()
    
    def isSingleUpload(self):
        if self.clean_uploadtype['singleRGB']:
           return True
        else:
           return False

    def isMultipleUpload(self):
        if self.clean_uploadtype['threeRGB']:
           return True
        else:
           return False
        


class RgbSettingsForm(forms.Form):

    """ Renders a home  view.
         A set of forms used in program view

         forms.Form
         - None
    """

    red = forms.BooleanField(required=False)
    blue = forms.BooleanField(required=False)
    green = forms.BooleanField(required=False)
    redgreen = forms.BooleanField(required=False)
    redblue = forms.BooleanField(required=False)
    greenblue = forms.BooleanField(required=False)
    all = forms.BooleanField(required=False)

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
    wAutoTriple = forms.FloatField(required=False)
    ginfTriple = forms.FloatField(required=False)

    rangeAutoCrossAll = forms.FloatField(required=False) # parameters for auto and cross when the "all correlation" option is selected
    ginfAutoCrossAll = forms.FloatField(required=False)
    wAutoCrossAll = forms.FloatField(required=False)
    gzeroAutoCrossAll = forms.FloatField(required=False)

    rangeTripleAll = forms.FloatField(required=False) # parameters for triple when the "all correlation" option is selected.
    gzeroTripleAll = forms.FloatField(required=False)
    wAutoTripleAll = forms.FloatField(required=False)
    ginfTripleAll = forms.FloatField(required=False)


    RESOLUTIONS  = (     # set options for the user to specify sample for triple correlation
        (1, '16x16'),
        (2, '32x32'),
        (3, '64x64'),
    )

    resolutions = forms.ChoiceField(initial=3, choices=RESOLUTIONS)

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
        if self.clean_userSelected['id_auto']:
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
        if self.clean_userSelected['id_cross']:
            return True
        else:
            return False

    def isTriple(self):
        if self.clean_userSelected['id_triple']:
           return True
        else:
           return False

    def isAll(self):
        if self.clean_userSelected['id_all']:
           return True
        else:
           return False

