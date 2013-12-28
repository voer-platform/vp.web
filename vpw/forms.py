from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _


class MaterialCreationForm(forms.Form):
    title = forms.CharField(max_length=255)
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


class ModuleCreationForm(MaterialCreationForm):
    body = forms.CharField(widget=TinyMCE(attrs={'rows': 7}), required=False)


class CollectionCreationForm(MaterialCreationForm):
    body = forms.CharField(required=False)


class EditProfileForm(forms.Form):
    email = forms.EmailField(max_length=255)
    fullname = forms.CharField(max_length=255)
