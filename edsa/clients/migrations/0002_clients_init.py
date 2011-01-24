
from south.db import db
from django.db import models
from edsa.clients.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Biography'
        db.create_table('clients_biography', (
            ('id', orm['clients.biography:id']),
            ('user', orm['clients.biography:user']),
            ('summary', orm['clients.biography:summary']),
            ('text', orm['clients.biography:text']),
            ('image', orm['clients.biography:image']),
        ))
        db.send_create_signal('clients', ['Biography'])
        
        # Adding model 'StateProvince'
        db.create_table('clients_stateprovince', (
            ('iso_code', orm['clients.stateprovince:iso_code']),
            ('name', orm['clients.stateprovince:name']),
            ('country', orm['clients.stateprovince:country']),
        ))
        db.send_create_signal('clients', ['StateProvince'])
        
        # Adding model 'ContactInfo'
        db.create_table('clients_contactinfo', (
            ('id', orm['clients.contactinfo:id']),
            ('user', orm['clients.contactinfo:user']),
            ('department', orm['clients.contactinfo:department']),
            ('institution', orm['clients.contactinfo:institution']),
            ('last_updated', orm['clients.contactinfo:last_updated']),
        ))
        db.send_create_signal('clients', ['ContactInfo'])
        
        # Adding model 'Country'
        db.create_table('clients_country', (
            ('iso_code', orm['clients.country:iso_code']),
            ('name', orm['clients.country:name']),
        ))
        db.send_create_signal('clients', ['Country'])
        
        # Adding model 'Address'
        db.create_table('clients_address', (
            ('id', orm['clients.address:id']),
            ('contactinfo', orm['clients.address:contactinfo']),
            ('label', orm['clients.address:label']),
            ('address_line1', orm['clients.address:address_line1']),
            ('address_line2', orm['clients.address:address_line2']),
            ('postal_code', orm['clients.address:postal_code']),
            ('city', orm['clients.address:city']),
            ('state_province', orm['clients.address:state_province']),
            ('country', orm['clients.address:country']),
        ))
        db.send_create_signal('clients', ['Address'])
        
        # Adding model 'Institution'
        db.create_table('clients_institution', (
            ('id', orm['clients.institution:id']),
            ('name', orm['clients.institution:name']),
            ('description', orm['clients.institution:description']),
            ('url', orm['clients.institution:url']),
        ))
        db.send_create_signal('clients', ['Institution'])
        
        # Creating unique_together for [address_line1, address_line2, postal_code, city, state_province, country] on Address.
        db.create_unique('clients_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [address_line1, address_line2, postal_code, city, state_province, country] on Address.
        db.delete_unique('clients_address', ['address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country_id'])
        
        # Deleting model 'Biography'
        db.delete_table('clients_biography')
        
        # Deleting model 'StateProvince'
        db.delete_table('clients_stateprovince')
        
        # Deleting model 'ContactInfo'
        db.delete_table('clients_contactinfo')
        
        # Deleting model 'Country'
        db.delete_table('clients_country')
        
        # Deleting model 'Address'
        db.delete_table('clients_address')
        
        # Deleting model 'Institution'
        db.delete_table('clients_institution')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
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
            'Meta': {'unique_together': "(('address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country'),)"},
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'clients.contactinfo': {
            'department': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Institution']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'clients.country': {
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'clients.institution': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'clients.stateprovince': {
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Country']"}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['clients']
