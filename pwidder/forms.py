from django import forms
from .models import Pweet
from django.contrib.auth.models import User


# class PweetCreate(forms.Form):
#     username = forms.CharField()
#     content = forms.CharField()


class ImageCreate(forms.Form):
    profile_image = forms.ImageField()




class PweetCreate(forms.ModelForm):
    class Meta:
        model = Pweet        
        fields = ['content']
    





