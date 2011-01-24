# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RegisteredPythonModule'
        db.create_table('clients_registeredpythonmodule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('documentation', self.gf('django.db.models.fields.TextField')()),
            ('_default_params', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clients', ['RegisteredPythonModule'])

        # Adding model 'VariableProcessor'
        db.create_table('clients_variableprocessor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.RegisteredPythonModule'])),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.CommandLineTool'])),
            ('processor_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('_params', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clients', ['VariableProcessor'])

        # Adding model 'CommandLineTool'
        db.create_table('clients_commandlinetool', (
            ('tool_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Tool'], unique=True, primary_key=True)),
            ('client_cmd', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clients', ['CommandLineTool'])

        # Adding model 'PythonTool'
        db.create_table('clients_pythontool', (
            ('registeredpythonmodule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.RegisteredPythonModule'], unique=True)),
            ('tool_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Tool'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('clients', ['PythonTool'])


    def backwards(self, orm):
        
        # Deleting model 'RegisteredPythonModule'
        db.delete_table('clients_registeredpythonmodule')

        # Deleting model 'VariableProcessor'
        db.delete_table('clients_variableprocessor')

        # Deleting model 'CommandLineTool'
        db.delete_table('clients_commandlinetool')

        # Deleting model 'PythonTool'
        db.delete_table('clients_pythontool')


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
            'Meta': {'object_name': 'PythonTool', '_ormbases': ['clients.Tool', 'clients.RegisteredPythonModule']},
            'registeredpythonmodule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.RegisteredPythonModule']", 'unique': 'True'}),
            'tool_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Tool']", 'unique': 'True', 'primary_key': 'True'})
        },
        'clients.registeredpythonmodule': {
            'Meta': {'object_name': 'RegisteredPythonModule'},
            '_default_params': ('django.db.models.fields.TextField', [], {}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'documentation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'clients.stateprovince': {
            'Meta': {'object_name': 'StateProvince'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Country']"}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'clients.task': {
            'Meta': {'object_name': 'Task'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dependencies_rel_+'", 'blank': 'True', 'to': "orm['clients.Task']"}),
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
            'outputs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_outputs'", 'symmetrical': 'False', 'to': "orm['data.Variable']"})
        },
        'clients.variableprocessor': {
            'Meta': {'object_name': 'VariableProcessor'},
            '_params': ('django.db.models.fields.TextField', [], {}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RegisteredPythonModule']"}),
            'processor_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.BaseUnit']"})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['clients']
