# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Material'
        db.create_table(u'vpw_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('material_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('categories', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('license_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('derived_from', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'vpw', ['Material'])


    def backwards(self, orm):
        # Deleting model 'Material'
        db.delete_table(u'vpw_material')


    models = {
        u'vpw.material': {
            'Meta': {'object_name': 'Material'},
            'categories': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'derived_from': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'license_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'material_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'material_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'vpw.materialfeature': {
            'Meta': {'object_name': 'MaterialFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['vpw']