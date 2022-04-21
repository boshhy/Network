from turtle import color
from django import forms
from .models import Posts


# This form will be used so a user can enter text for a post
class PostForm(forms.Form):
    post = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4,
                                     'cols': 64,
                                     'style':   'resize:none; \
                                                border-radius: 10px; \
                                                padding:5px;'
                                     }))
