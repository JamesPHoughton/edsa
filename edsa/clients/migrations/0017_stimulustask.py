# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'StimulusTask'
        db.create_table('clients_stimulustask', (
            ('task_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Task'], unique=True, primary_key=True)),
            ('_variable_params', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.RegisteredPythonModule'])),
        ))
        db.send_create_signal('clients', ['StimulusTask'])

        # Adding M2M table for field stimulus_variables on 'StimulusTask'
        db.create_table('clients_stimulustask_stimulus_variables', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stimulustask', models.ForeignKey(orm['clients.stimulustask'], null=False)),
            ('variable', models.ForeignKey(orm['data.variable'], null=False))
        ))
        db.create_unique('clients_stimulustask_stimulus_variables', ['stimulustask_id', 'variable_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'StimulusTask'
        db.delete_table('clients_stimulustask')

        # Removing M2M table for field stimulus_variables on 'StimulusTask'
        db.delete_table('clients_stimulustask_stimulus_variables')
    
    
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
        'clients.address': {
            'Meta': {'unique_together': "(('address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'),)", 'object_name': 'Address'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contactinfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.ContactInfo']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state_province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.StateProvince']"})
        },
        'clients.biography': {
            'Meta': {'object_name': 'Biography'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'clients.commandlinetool': {
            'Meta': {'object_name': 'CommandLineTool', '_ormbases': ['clients.Tool']},
            'client_cmd': ('django.db.models.fields.TextField', [], {}),
            'processors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.RegisteredPythonModule']", 'through': "orm['clients.VariableProcessor']", 'symmetrical': 'False'}),
            'tool_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Tool']", 'unique': 'True', 'primary_key': 'True'})
        },
        'clients.contactinfo': {
            'Meta': {'object_name': 'ContactInfo'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Institution']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'clients.country': {
            'Meta': {'object_name': 'Country'},
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'clients.edsauser': {
            'Meta': {'object_name': 'EDSAUser', 'db_table': "'auth_user'", '_ormbases': ['auth.User']}
        },
        'clients.institution': {
            'Meta': {'object_name': 'Institution'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'clients.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'maintainer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'clients.pythontool': {
            'Meta': {'object_name': 'PythonTool', '_ormbases': ['clients.Tool']},
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']"}),
            'tool_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Tool']", 'unique': 'True', 'primary_key': 'True'})
        },
        'clients.registeredpythonmodule': {
            'Meta': {'object_name': 'RegisteredPythonModule'},
            '_default_params': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'documentation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'clients.stateprovince': {
            'Meta': {'object_name': 'StateProvince'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Country']"}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'clients.stimulustask': {
            'Meta': {'object_name': 'StimulusTask', '_ormbases': ['clients.Task']},
            '_variable_params': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']"}),
            'stimulus_variables': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Variable']", 'symmetrical': 'False'}),
            'task_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Task']", 'unique': 'True', 'primary_key': 'True'})
        },
        'clients.task': {
            'Meta': {'object_name': 'Task'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.Task']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Tool']", 'null': 'True', 'blank': 'True'})
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
        'clients.variableprocessor': {
            'Meta': {'object_name': 'VariableProcessor'},
            '_params': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']"}),
            'processor_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'seq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.CommandLineTool']"}),
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Variable']", 'symmetrical': 'False'})
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
        'data.variable': {
            'Meta': {'object_name': 'Variable'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.BaseUnit']"})
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
        }
    }
    
    complete_apps = ['clients']
