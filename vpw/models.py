from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import IntegerField, TextField, DateTimeField,\
    CharField
from registration.signals import user_activated
from vpw.vpr_api import vpr_create_person
from django.utils.translation import ugettext as _

# Create your models here.

class Settings(models.Model):
    """
    A table to store configurable settings with a pair of name and value,
    also support multiple languagues.
    """
    name = CharField(max_length=64)
    value = TextField(blank=True, default='')
    language= CharField(max_length=8, default='vi')


class MaterialFeature(models.Model):
    material_id = CharField(max_length=64, null=True)
    weight = IntegerField(default=1)


class FeaturedAuthor(models.Model):
    author_id = IntegerField(null=False)
    weight = IntegerField(default=1)


class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    author_id = models.IntegerField()


class Material(models.Model):
    material_id = CharField(max_length=64, blank=True, default="")
    material_type = IntegerField(default=1)
    text = TextField(blank=True, default='')
    version = IntegerField(null=True, blank=True, default=0)
    title = CharField(max_length=255, verbose_name=_("Title"))
    description = TextField(blank=True)
    categories = CharField(max_length=256, blank=True, verbose_name=_("Categories"))
    keywords = TextField(blank=True, default="")
    language = CharField(max_length=2, blank=True, default="vi", verbose_name=_("Language"))
    license_id = IntegerField(null=True, default=1)
    modified = DateTimeField(auto_now=True, blank=True)
    derived_from = CharField(max_length=64, blank=True)
    creator = models.ForeignKey(User)
    status = IntegerField(null=True, default=1)
    author = CharField(max_length=100, blank=True, default="")
    editor = CharField(max_length=100, blank=True, default="")
    licensor = CharField(max_length=100, blank=True, default="")
    maintainer = CharField(max_length=100, blank=True, default="")
    translator = CharField(max_length=100, blank=True, default="")
    coeditor = CharField(max_length=100, blank=True, default="")

    def to_dict(self):
        material = dict()
        material['id'] = self.id
        material['material_id'] = self.material_id
        material['material_type'] = int(self.material_type)
        material['text'] = self.text
        material['version'] = self.version
        material['title'] = self.title
        material['description'] = self.description
        material['categories'] = self.categories
        material['status'] = self.status
        material['modified'] = self.modified

        if self.author:
            material['author'] = self.author

        return material


# Declare Signs
def user_activated_callback(sender, user, request, **kwargs):
    try:
        author = Author.objects.get(user=user)
    except Author.DoesNotExist:
        # create person on vpr
        params = dict()
        params["fullname"] = '%s %s' % (user.first_name, user.last_name)
        params["user_id"] = user.username
        params["first_name"] = user.first_name
        params["last_name"] = user.last_name
        params["email"] = user.email

        new_person = vpr_create_person(**params)

        if 'id' in new_person:
            if new_person["id"] > 0:
                author = Author(user=user)
                author.author_id = new_person['id']
                author.save()

user_activated.connect(user_activated_callback, dispatch_uid="ACTIVE_USER")
