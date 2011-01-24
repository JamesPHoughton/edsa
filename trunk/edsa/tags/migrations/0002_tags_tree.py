# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from edsa.tags.models import Tag
from mptt.managers import TreeManager

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Tag.lft'
        db.add_column('tags_tag', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Tag.rght'
        db.add_column('tags_tag', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Tag.tree_id'
        db.add_column('tags_tag', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'Tag.level'
        db.add_column('tags_tag', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        #   Migrate data (WARNING: flattens tree)
        old_tags = Tag.objects.all()
        for tag in old_tags:
            label = tag.label
            desc = tag.description
            tag.delete()
            Tag._tree_manager.insert_node(Tag(label=label, description=desc), None)
            print 'Created tree tag ID #%d (%d--%d)' % (tag.id, tag.lft, tag.rght)

    def backwards(self, orm):
        
        # Deleting field 'Tag.lft'
        db.delete_column('tags_tag', 'lft')

        # Deleting field 'Tag.rght'
        db.delete_column('tags_tag', 'rght')

        # Deleting field 'Tag.tree_id'
        db.delete_column('tags_tag', 'tree_id')

        # Deleting field 'Tag.level'
        db.delete_column('tags_tag', 'level')


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
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['tags']
