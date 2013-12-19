# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MaterialFeature'
        db.create_table(u'vpw_materialfeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'vpw', ['MaterialFeature'])


    def backwards(self, orm):
        # Deleting model 'MaterialFeature'
        db.delete_table(u'vpw_materialfeature')


    models = {
        u'vpw.materialfeature': {
            'Meta': {'object_name': 'MaterialFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['vpw']