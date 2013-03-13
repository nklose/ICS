from django import forms

class RgbSettingsForm(forms.Form):

    red = forms.BooleanField(required=False)
    blue = forms.BooleanField(required=False)
    green = forms.BooleanField(required=False)
    redgreen = forms.BooleanField(required=False)
    redblue = forms.BooleanField(required=False)
    greenblue = forms.BooleanField(required=False)
    all = forms.BooleanField(required=False)

    rangeAuto = forms.FloatField()
    gzeroAuto = forms.FloatField()
    wAuto = forms.FloatField()
    ginfAuto = forms.FloatField()

    rangeCross = forms.FloatField()
    gzeroCross  = forms.FloatField()
    wCross = forms.FloatField()
    ginfCross= forms.FloatField()

    rangeTriple = forms.FloatField()
    gzeroTriple = forms.FloatField()
    wAutoTriple = forms.FloatField()
    ginfTriple = forms.FloatField()

    ginfAutoCross = forms.FloatField()
    rangeAutoCross = forms.FloatField()
    gzeroAutoCross = forms.FloatField()
    wAutoCross = forms.FloatField()
    ginfAutoCross = forms.FloatField()

    RESOLUTIONS  = (
             (1,'16x16'),
             (2,'32x32'),
             (3,'64x64'),
     )

    resolutions = forms.ChoiceField(initial=3,choices=RESOLUTIONS)