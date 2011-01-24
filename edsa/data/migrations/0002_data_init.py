
from south.db import db
from django.db import models
from edsa.data.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'BaseUnit'
        db.create_table('data_baseunit', (
            ('id', orm['data.baseunit:id']),
            ('symbol', orm['data.baseunit:symbol']),
            ('name', orm['data.baseunit:name']),
            ('quantity_expressed', orm['data.baseunit:quantity_expressed']),
            ('system', orm['data.baseunit:system']),
        ))
        db.send_create_signal('data', ['BaseUnit'])
        
        # Adding model 'MeasurementSystem'
        db.create_table('data_measurementsystem', (
            ('id', orm['data.measurementsystem:id']),
            ('name', orm['data.measurementsystem:name']),
        ))
        db.send_create_signal('data', ['MeasurementSystem'])
        
        # Adding model 'Unit'
        db.create_table('data_unit', (
            ('baseunit_ptr', orm['data.unit:baseunit_ptr']),
        ))
        db.send_create_signal('data', ['Unit'])
        
        # Adding model 'UnitConversion'
        db.create_table('data_unitconversion', (
            ('id', orm['data.unitconversion:id']),
            ('source_unit', orm['data.unitconversion:source_unit']),
            ('dest_unit', orm['data.unitconversion:dest_unit']),
            ('ratio', orm['data.unitconversion:ratio']),
        ))
        db.send_create_signal('data', ['UnitConversion'])
        
        # Adding model 'UnitExponent'
        db.create_table('data_unitexponent', (
            ('id', orm['data.unitexponent:id']),
            ('unit', orm['data.unitexponent:unit']),
            ('expression', orm['data.unitexponent:expression']),
            ('power_num', orm['data.unitexponent:power_num']),
            ('power_denom', orm['data.unitexponent:power_denom']),
        ))
        db.send_create_signal('data', ['UnitExponent'])
        
        # Adding model 'DataCategory'
        db.create_table('data_datacategory', (
            ('id', orm['data.datacategory:id']),
            ('label', orm['data.datacategory:label']),
            ('description', orm['data.datacategory:description']),
        ))
        db.send_create_signal('data', ['DataCategory'])
        
        # Adding model 'PhysicalQuantity'
        db.create_table('data_physicalquantity', (
            ('id', orm['data.physicalquantity:id']),
            ('label', orm['data.physicalquantity:label']),
        ))
        db.send_create_signal('data', ['PhysicalQuantity'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'BaseUnit'
        db.delete_table('data_baseunit')
        
        # Deleting model 'MeasurementSystem'
        db.delete_table('data_measurementsystem')
        
        # Deleting model 'Unit'
        db.delete_table('data_unit')
        
        # Deleting model 'UnitConversion'
        db.delete_table('data_unitconversion')
        
        # Deleting model 'UnitExponent'
        db.delete_table('data_unitexponent')
        
        # Deleting model 'DataCategory'
        db.delete_table('data_datacategory')
        
        # Deleting model 'PhysicalQuantity'
        db.delete_table('data_physicalquantity')
        
    
    
    models = {
        'data.baseunit': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'quantity_expressed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PhysicalQuantity']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.MeasurementSystem']"})
        },
        'data.datacategory': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'data.measurementsystem': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'data.physicalquantity': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'data.unit': {
            'baseunit_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.BaseUnit']", 'unique': 'True', 'primary_key': 'True'}),
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.BaseUnit']"})
        },
        'data.unitconversion': {
            'dest_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conversion_dest'", 'to': "orm['data.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ratio': ('django.db.models.fields.FloatField', [], {}),
            'source_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conversion_source'", 'to': "orm['data.Unit']"})
        },
        'data.unitexponent': {
            'expression': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expression'", 'to': "orm['data.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power_denom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'power_num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.BaseUnit']"})
        }
    }
    
    complete_apps = ['data']
