from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _


class ModuleCreationForm(forms.Form):
    title = forms.CharField(max_length=255)
    body = forms.CharField(widget=TinyMCE(attrs={'rows': 7}), required=False)
    description = forms.CharField(max_length=1000, required=False)
    keywords = forms.CharField(max_length=200, required=False)
    language = forms.CharField(max_length=2)
    categories = forms.CharField(max_length=3)

    def clean_title(self):
        if self.cleaned_data.get('title', '') == '':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('title', '')

    def clean_categories(self):
        if self.cleaned_data.get('categories', '') == '':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('categories', '')

    def clean_language(self):
        if self.cleaned_data.get('language', '') == '':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('language', '')

##### FORM ##################

# def MaterialForm(forms.Form):
#     material_type = IntegerField(default=1)
#     text = TextField()
#     title = forms.CharField(max_length=255)
#     description = forms.CharField(blank=True, null=True)
#     categories = CharField(max_length=256, blank=True, null=True)
#     keywords = TextField(blank=True, null=True)
#     language = CharField(max_length=2, blank=True)
#     forms.
#     license_id = IntegerField(null=True)
#     modified = DateTimeField(blank=True)
#     derived_from = CharField(max_length=64, blank=True, null=True)