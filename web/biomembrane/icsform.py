from django import forms

import formfields


class SampleImageForm(forms.Form):
    img = formfields.LosslessImageField()


class ImgCorrelateForm(forms.Form):
    red = forms.BooleanField()
    blue = forms.BooleanField()
    green = forms.BooleanField()
    range = forms.IntegerField();
    gzero = forms.DecimalField();
    w = forms.DecimalField();
    ginf = forms.DecimalField();
