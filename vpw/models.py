from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import IntegerField, TextField, DateTimeField,\
    CharField
from django.db.models.fields.files import ImageField


# Create your models here.
from registration.signals import user_activated
from vpw.vpr_api import vpr_create_person


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
    material_id = CharField(max_length=64)
    material_type = IntegerField(default=1)
    text = TextField()
    version = IntegerField(default=1)
    title = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    categories = CharField(max_length=256, blank=True, null=True)
    keywords = TextField(blank=True, null=True)
    language = CharField(max_length=2, blank=True)
    license_id = IntegerField(null=True)
    modified = DateTimeField(blank=True)
    derived_from = CharField(max_length=64, blank=True, null=True)


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