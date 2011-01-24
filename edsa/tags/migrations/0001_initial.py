# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('tags_tag', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('tags', ['Tag'])

        # Adding model 'DataCategory'
        db.create_table('tags_datacategory', (
            ('tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tags.Tag'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tags', ['DataCategory'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('tags_tag')

        # Deleting model 'DataCategory'
        db.delete_table('tags_datacategory')
    
    
    models = {
        'tags.datacategory': {
            'Meta': {'object_name': 'DataCategory', '_ormbases': ['tags.Tag']},
            'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tags.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['tags']
