from django import forms
from .models import Posts


class PostForm(forms.Form):
    post = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 64, 'style': 'resize:none;'}))
