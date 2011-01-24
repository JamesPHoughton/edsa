# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ValueNamespace'
        db.create_table('tags_valuenamespace', (
            ('tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tags.Tag'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tags', ['ValueNamespace'])


    def backwards(self, orm):
        
        # Deleting model 'ValueNamespace'
        db.delete_table('tags_valuenamespace')


    models = {
        'tags.datacategory': {
            'Meta': {'object_name': 'DataCategory', '_ormbases': ['tags.Tag']},
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tags.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['tags.Tag']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'tags.valuenamespace': {
            'Meta': {'object_name': 'ValueNamespace', '_ormbases': ['tags.Tag']},
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tags.Tag']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tags']
