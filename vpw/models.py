from django.db import models
from django.db.models.fields import IntegerField, TextField, DateTimeField,\
    CharField
from django.db.models.fields.files import ImageField

# Create your models here.
class MaterialFeature(models.Model):
    material_id = CharField(max_length=64, null=True)
    weight = IntegerField(default=1)
    
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