import requests

from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from registration.forms import RegistrationForm
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _
from django.conf import settings

from vpw.models import Material


class MaterialForm(ModelForm):
    # title = forms.CharField(max_length=255)
    # description = forms.CharField(max_length=1000, required=False)
    # keywords = forms.CharField(max_length=200, required=False)
    # language = forms.CharField(max_length=2)
    # categories = forms.CharField(max_length=3)
    # authors = forms.CharField(max_length=100, required=False)
    # editors = forms.CharField(max_length=100, required=False)
    # licensors = forms.CharField(max_length=100, required=False)
    # maintainers = forms.CharField(max_length=100, required=False)
    # translators = forms.CharField(max_length=100, required=False)
    # coeditors = forms.CharField(max_length=100, required=False)
    # version = forms.IntegerField(initial=0, required=False)
    # material_id = forms.CharField(max_length=64, required=False)
    mid = forms.IntegerField(required=False)
    # derived_from = forms.CharField(max_length=64, required=False)
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['title'].required = True
        self.fields['categories'].required = True
        self.fields['language'].required = True

    class Meta:
        model = Material
        fields = ['title', 'description', 'categories', 'keywords', 'language', 'derived_from',
                  'author', 'editor', 'licensor', 'maintainer', 'translator', 'coeditor', 'text']

    def clean_language(self):
        if self.cleaned_data.get('language', '00') == '00':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('language', '')

    def clean_version(self):
        if self.cleaned_data.get('version'):
            try:
                return int(self.cleaned_data['version'])
            except ValueError:
                raise ValidationError("Invalid number")
        return 0


class ModuleForm(MaterialForm):
    body = forms.CharField(widget=TinyMCE(attrs={'rows': 7}), required=False)

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['body'].initial = kwargs['instance'].text


class CollectionForm(MaterialForm):
    body = forms.CharField(required=False)


class EditProfileForm(forms.Form):
    current_password = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(max_length=255)
    new_password = forms.CharField(max_length=255, required=False)
    confirm_password = forms.CharField(max_length=255, required=False)
    fullname = forms.CharField(max_length=255)
    homepage = forms.URLField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control typetext', 'id': 'InputHomepage', 'placeholder': _('Enter homepage')}))
    affiliation_url = forms.URLField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control typetext', 'id': 'InputAffiliationURL', 'placeholder': _('Enter affiliaton URL')}))
    biography = forms.CharField(widget=TinyMCE(attrs={'rows': 7}), required=False)

    def clean(self):
        cleaned_data = self.cleaned_data # individual field's clean methods have already been called
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            self._errors["confirm_password"] = self.error_class([u"Confirm password is not matchs"])

        return cleaned_data


class SettingsForm(forms.Form):
    module_license = forms.CharField(widget=TinyMCE(attrs={'rows': 4}), required=False)
    collection_license = forms.CharField(widget=TinyMCE(attrs={'rows': 4}), required=False)


class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = forms.CharField(max_length=512, required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(RecaptchaRegistrationForm, self).clean()

        recaptcha_response = cleaned_data.get('recaptcha', '')
        data = {
            'response': recaptcha_response,
            'secret': settings.RECAPTCHA_SECRET_KEY
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if not result_json.get('success', False):
            raise ValidationError("Captcha validation failed")

        return cleaned_data
