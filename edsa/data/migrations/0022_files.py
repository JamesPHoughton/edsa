# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FileInstance'
        db.create_table('data_fileinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Machine'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FileValue'])),
            ('path', self.gf('django.db.models.fields.FilePathField')(path='F:/projects/edsa/edsa_repo/trunk//files', max_length=255, recursive=True)),
            ('revision', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('exists', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('data', ['FileInstance'])

        # Adding model 'FileValue'
        db.create_table('data_filevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.RegisteredPythonModule'])),
        ))
        db.send_create_signal('data', ['FileValue'])


    def backwards(self, orm):
        
        # Deleting model 'FileInstance'
        db.delete_table('data_fileinstance')

        # Deleting model 'FileValue'
        db.delete_table('data_filevalue')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'clients.edsauser': {
            'Meta': {'object_name': 'EDSAUser', 'db_table': "'auth_user'", '_ormbases': ['auth.User']}
        },
        'clients.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'maintainer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'clients.registeredpythonmodule': {
            'Meta': {'object_name': 'RegisteredPythonModule'},
            '_default_params': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'documentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'clients.tool': {
            'Meta': {'object_name': 'Tool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_constraints': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tool_input_constraints'", 'blank': 'True', 'to': "orm['data.Constraint']"}),
            'inputs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_inputs'", 'symmetrical': 'False', 'to': "orm['data.Variable']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.Machine']", 'symmetrical': 'False'}),
            'maintainer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'output_constraints': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tool_output_constraints'", 'blank': 'True', 'to': "orm['data.Constraint']"}),
            'outputs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_outputs'", 'symmetrical': 'False', 'to': "orm['data.Variable']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'data.baseunit': {
            'Meta': {'object_name': 'BaseUnit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'quantity_expressed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PhysicalQuantity']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.MeasurementSystem']"})
        },
        'data.constraint': {
            'Meta': {'object_name': 'Constraint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'constraint_variables'", 'symmetrical': 'False', 'to': "orm['data.Variable']"})
        },
        'data.datavalue': {
            'Meta': {'object_name': 'DataValue'},
            '_data': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variable_category'", 'to': "orm['tags.DataCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variable_namespace'", 'null': 'True', 'to': "orm['tags.ValueNamespace']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Tool']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Variable']"})
        },
        'data.fileinstance': {
            'Meta': {'object_name': 'FileInstance'},
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Machine']"}),
            'path': ('django.db.models.fields.FilePathField', [], {'path': "'F:/projects/edsa/edsa_repo/trunk//files'", 'max_length': '255', 'recursive': 'True'}),
            'revision': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FileValue']"})
        },
        'data.filevalue': {
            'Meta': {'object_name': 'FileValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.Machine']", 'through': "orm['data.FileInstance']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']"})
        },
        'data.limitconstraint': {
            'Meta': {'object_name': 'LimitConstraint', '_ormbases': ['data.Constraint']},
            'constraint_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Constraint']", 'unique': 'True', 'primary_key': 'True'}),
            'max_values': ('django.db.models.fields.TextField', [], {}),
            'min_values': ('django.db.models.fields.TextField', [], {})
        },
        'data.measurementsystem': {
            'Meta': {'object_name': 'MeasurementSystem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'data.physicalquantity': {
            'Meta': {'object_name': 'PhysicalQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'data.unit': {
            'Meta': {'object_name': 'Unit', '_ormbases': ['data.BaseUnit']},
            'baseunit_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.BaseUnit']", 'unique': 'True', 'primary_key': 'True'}),
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'unit_components'", 'symmetrical': 'False', 'through': "orm['data.UnitExponent']", 'to': "orm['data.BaseUnit']"})
        },
        'data.unitconversion': {
            'Meta': {'object_name': 'UnitConversion'},
            'dest_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conversion_dest'", 'to': "orm['data.BaseUnit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'ratio': ('django.db.models.fields.FloatField', [], {}),
            'source_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conversion_source'", 'to': "orm['data.BaseUnit']"})
        },
        'data.unitexponent': {
            'Meta': {'object_name': 'UnitExponent'},
            'expression': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expression'", 'to': "orm['data.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power_denom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'power_num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.BaseUnit']"})
        },
        'data.variable': {
            'Meta': {'object_name': 'Variable'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.BaseUnit']"}),
            'varType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.VarType']"})
        },
        'data.vartype': {
            'Meta': {'object_name': 'VarType'},
            'base_field': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
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

    complete_apps = ['data']
