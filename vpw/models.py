from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import IntegerField, TextField, DateTimeField,\
    CharField
from registration.signals import user_activated
from vpw.vpr_api import vpr_create_person


# Create your models here.

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
    version = IntegerField(null=True, blank=True)
    title = CharField(max_length=255)
    description = TextField(blank=True, default="")
    categories = CharField(max_length=256, blank=True)
    keywords = TextField(blank=True, default="")
    language = CharField(max_length=2, blank=True, default="vi")
    license_id = IntegerField(null=True, default=1)
    modified = DateTimeField(auto_now=True, blank=True)
    derived_from = CharField(max_length=64, blank=True)


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

        if new_person.has_key("id"):
            if (new_person["id"] > 0):
                author = Author(user=user)
                author.author_id = new_person['id']
                author.save()

user_activated.connect(user_activated_callback, dispatch_uid="ACTIVE_USER")

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