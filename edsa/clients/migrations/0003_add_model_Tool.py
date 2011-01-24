# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("data", "0004_add_model_Constraint"),
    )

    def forwards(self, orm):
        
        # Adding model 'Tool'
        db.create_table('clients_tool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('maintainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('client_cmd', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clients', ['Tool'])


    def backwards(self, orm):
        
        # Deleting model 'Tool'
        db.delete_table('clients_tool')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
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
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'clients.biography': {
            'Meta': {'object_name': 'Biography'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
        'clients.stateprovince': {
            'Meta': {'object_name': 'StateProvince'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Country']"}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'clients.task': {
            'Meta': {'object_name': 'Task'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dependencies_rel_+'", 'to': "orm['clients.Task']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Tool']", 'null': 'True', 'blank': 'True'})
        },
        'clients.tool': {
            'Meta': {'object_name': 'Tool'},
            'client_cmd': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_constraints': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_input_constraints'", 'to': "orm['data.Constraint']"}),
            'inputs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_inputs'", 'to': "orm['data.Variable']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'machines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.Machine']"}),
            'maintainer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'output_constraints': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_output_constraints'", 'to': "orm['data.Constraint']"}),
            'outputs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tool_outputs'", 'to': "orm['data.Variable']"})
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
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'constraint_variables'", 'to': "orm['data.Variable']"})
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
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'unit_components'", 'through': "'UnitExponent'", 'to': "orm['data.BaseUnit']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tags.Tag']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Unit']"})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['clients']
