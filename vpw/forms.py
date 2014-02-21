from django import forms
from django.core.exceptions import ValidationError
from registration.forms import RegistrationForm
from vpw.fields import ReCaptchaField
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext as _


class MaterialCreationForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1000, required=False)
    keywords = forms.CharField(max_length=200, required=False)
    language = forms.CharField(max_length=2)
    categories = forms.CharField(max_length=3)
    authors = forms.CharField(max_length=100, required=False)
    editors = forms.CharField(max_length=100, required=False)
    licensors = forms.CharField(max_length=100, required=False)
    maintainers = forms.CharField(max_length=100, required=False)
    translators = forms.CharField(max_length=100, required=False)
    coeditors = forms.CharField(max_length=100, required=False)
    version = forms.IntegerField(initial=0, required=False)
    material_id = forms.CharField(max_length=64, required=False)
    mid = forms.IntegerField(required=False)

    def clean_title(self):
        if self.cleaned_data.get('title', '') == '':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('title', '')

    def clean_categories(self):
        if self.cleaned_data.get('categories', '') == '':
            raise ValidationError(_('Required'))
        return self.cleaned_data.get('categories', '')

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

class ModuleCreationForm(MaterialCreationForm):
    body = forms.CharField(widget=TinyMCE(attrs={'rows': 7}), required=False)


class CollectionCreationForm(MaterialCreationForm):
    body = forms.CharField(required=False)


class EditProfileForm(forms.Form):
    current_password = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(max_length=255)
    new_password = forms.CharField(max_length=255, required=False)
    confirm_password = forms.CharField(max_length=255, required=False)
    fullname = forms.CharField(max_length=255)
    homepage = forms.URLField(max_length=255, required=False)
    affiliation_url = forms.URLField(max_length=255, required=False)

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
    recaptcha = ReCaptchaField(label="I'm a human")

