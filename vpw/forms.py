from django import forms
from tinymce.widgets import TinyMCE


class ModuleCreationForm(forms.Form):
    body = forms.CharField(widget=TinyMCE(attrs={'rows': 7}))
