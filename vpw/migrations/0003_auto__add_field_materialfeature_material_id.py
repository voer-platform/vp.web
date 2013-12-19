# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MaterialFeature.material_id'
        db.add_column(u'vpw_materialfeature', 'material_id',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MaterialFeature.material_id'
        db.delete_column(u'vpw_materialfeature', 'material_id')


    models = {
        u'vpw.materialfeature': {
            'Meta': {'object_name': 'MaterialFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['vpw']