from django import forms
import formfields

class SampleImageForm(forms.Form):
    img = formfields.LosslessImageField()

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

    rangeAuto = forms.FloatField()  # parameters for auto correlation
    gzeroAuto = forms.FloatField()
    wAuto = forms.FloatField()
    ginfAuto = forms.FloatField()

    rangeCross = forms.FloatField() # parameters for cross correlation
    gzeroCross  = forms.FloatField()
    wCross = forms.FloatField()
    ginfCross= forms.FloatField()

    rangeTriple = forms.FloatField() # parameters for triple correlation
    gzeroTriple = forms.FloatField()
    wAutoTriple = forms.FloatField()
    ginfTriple = forms.FloatField()

    ginfAutoCross = forms.FloatField() # parameters for both auto and triple
    rangeAutoCross = forms.FloatField()
    gzeroAutoCross = forms.FloatField()
    wAutoCross = forms.FloatField()
    ginfAutoCross = forms.FloatField()

    RESOLUTIONS  = (     # set options for the user to specify sample
             (1,'16x16'),
             (2,'32x32'),
             (3,'64x64'),
     )

    resolutions = forms.ChoiceField(initial=3,choices=RESOLUTIONS)