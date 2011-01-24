
__author__    = "Aurora Flight Sciences"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "GPL v.3"
__copyright__ = """
This file is part of EDSA, the Extensible Dataset Architecture system
Copyright (c) 2010-2011 Aurora Flight Sciences Corp.

Work on EDSA was sponsored by NASA Dryden Flight Research Center
under 2009 STTR contract NNX10CF57P.

EDSA is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free 
Software Foundation; either version 3 of the License, or (at your option) 
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
""" EDSA Data models

These models provide the core of EDSA's data storage mechanism.  There are 
three main principles.

1.  Units
EDSA tracks units.  What this means is that every piece of data can be traced
back to some physical quantity (e.g. mass) in some measurement system (e.g. SI)
and converted to other units that represent the same physical quantity, either
in the same measurement system or a different one.  Models used to represent
units include MeasurementSystem, PhysicalQuantity, BaseUnit, Unit, UnitExponent,
and UnitConversion.

2.  Variables
A variable is like a symbol in an algebraic expression (e.g. 'x' or 'rho_a').
The variable carries some metadata, such as the units that it should be expressed
in.  However, it does not carry the actual data; several different values may
be bound to a variable.  Variables are encoded in the Variable model.

3.  Values
The value is an instance of a variable (e.g. 'x' = 4).  It can take on any Python
type, so it could be a string or a numpy array as well as a floating-point value.
Values are encoded in the DataValue model.

"""

import copy

from django.db import models
from django.core.exceptions import ValidationError

from edsa.tags.models import Tag, DataCategory, ValueNamespace
from edsa.clients.models import EDSAUser, Tool, Machine, RegisteredPythonModule
from edsa.utils.uris import get_object_label, generate_object_label, get_machine_name
from edsa.settings import EDSA_STORAGE_DIR

import random
try:
    import cPickle as pickle
except:
    import pickle

class MeasurementSystem(models.Model):
    """ A placeholder for a measurement system: SI, imperial, cgs, etc. """
    
    name = models.CharField(max_length=80)
    #   access units through manager: baseunit_set, unit_set

    def __unicode__(self):
        return u'%s' % self.name

class PhysicalQuantity(models.Model):
    """ A placeholder for some type of physical quantity: force, mass, etc. """
    
    """ TODO: add relationships between quantities
        (i.e. torque has units of force * distance;
              energy has units of force * distance;
              but torque and energy are not the same thing)
    """
    label = models.CharField(max_length=80)
    #   access units through manager: baseunit_set, unit_set
    
    def __unicode__(self):
        return u'%s' % self.label

class BaseUnit(models.Model):
    """ A fundamental unit that other units may be derived from. """
    
    symbol = models.CharField(max_length=8)
    name = models.CharField(max_length=80)
    quantity_expressed = models.ForeignKey(PhysicalQuantity)
    system = models.ForeignKey(MeasurementSystem)
    
    def __unicode__(self):
        return u'%s (%s: %s) - %s' % (self.name, self.system, self.symbol, self.quantity_expressed)

    def get_conversion_path(self, dest_unit, path=[], visited_fwd=[], visited_rev=[]):
        """ Perform a depth-first search of UnitConversions to get from
            one unit to another.
        """
        
        current_unit = self
        adjacent_units_fwd = BaseUnit.objects.filter(id__in=current_unit.conversion_source.values_list('dest_unit', flat=True)).exclude(id__in=visited_fwd)
        adjacent_units_rev = BaseUnit.objects.filter(id__in=current_unit.conversion_dest.values_list('source_unit', flat=True)).exclude(id__in=visited_rev)

        if dest_unit.id in adjacent_units_fwd.values_list('id', flat=True):
            return path + [dest_unit.id], True
        if dest_unit.id in adjacent_units_rev.values_list('id', flat=True):
            return path + [dest_unit.id], True    
        
        orig_path = copy.copy(path)
        
        for unit in adjacent_units_fwd:
            path = orig_path + [unit.id]
            visited_fwd = visited_fwd + [unit.id]
            path, found = unit.get_conversion_path(dest_unit, path, visited_fwd, visited_rev)
            if found:
                return path, True
        for unit in adjacent_units_rev:
            path = orig_path + [unit.id]
            visited_rev = visited_rev + [unit.id]
            path, found = unit.get_conversion_path(dest_unit, path, visited_fwd, visited_rev)
            if found:
                return path, True
    
        return path, False
        
    def get_conversion(self, dest_unit):
        """ Searches for a path from 'self' to 'dest_unit'.
        
            If one is found, returns a UnitConversion that converts a value
            in unit 'self' to one in unit 'dest_unit'.  This will not be saved to the database.
        """
        
        path, found = self.get_conversion_path(dest_unit)
        if not found:
            return None
        
        #   Initialize an 'identity' unit conversion
        conv = UnitConversion(source_unit=self, dest_unit=dest_unit)
        conv.ratio = 1.0
        conv.offset = 0.0
        last_unit = self
        
        for unit_id in path:
            next_unit = BaseUnit.objects.get(id=unit_id)
            qs_fwd = last_unit.conversion_source.filter(dest_unit__id=unit_id)
            if qs_fwd.exists():
                #   Apply the conversion in the forward direction
                conv_step = qs_fwd[0]
                conv.offset = conv.offset * conv_step.ratio + conv_step.offset
                conv.ratio = conv.ratio * conv_step.ratio
            else:
                #   Apply the conversion in the reverse direction
                conv_step = last_unit.conversion_dest.filter(source_unit__id=unit_id)[0]
                conv.offset = (conv.offset - conv_step.offset) / conv_step.ratio
                conv.ratio = conv.ratio / conv_step.ratio

            last_unit = next_unit
            
        return conv
            
    
class Unit(BaseUnit):
    """ Allow expressing an equality between different units as a product
        of exponentiated terms. 
    """

    components = models.ManyToManyField(BaseUnit, through='UnitExponent', related_name='unit_components')

class UnitExponent(models.Model):
    """ Intermediate model for the many-to-many relationship needed by Unit """
    
    unit = models.ForeignKey(BaseUnit)
    expression = models.ForeignKey(Unit, related_name='expression')
    power_num = models.IntegerField(default=1)
    power_denom = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        if self.power_denom:
            return '%s: component %s^(%s/%s)' % (self.expression, self.unit.symbol, self.power_num, self.power_denom)
        else:
            return '%s: component %s^%s' % (self.expression, self.unit.symbol, self.power_num)
            

class UnitConversion(models.Model):
    """ Let x_s = qty x in source unit, 
            x_d = qty x in dest unit.
        Then x_d = m * x_s + b
        where
            m = ratio
            b = offset
    """
    source_unit = models.ForeignKey(BaseUnit, related_name='conversion_source')
    dest_unit = models.ForeignKey(BaseUnit, related_name='conversion_dest')
    ratio = models.FloatField()
    offset = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return u'%s to %s (ratio = %s, offset = %s)' % (self.source_unit.name, self.dest_unit.name, self.ratio, self.offset)

class VarType(models.Model):
    label = models.CharField(max_length=20)
    field_class = models.ForeignKey(RegisteredPythonModule, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s ' % (self.label)

    def get_formfield(self, *args, **kwargs):
        if self.field_class:
            return self.field_class.get_instance(*args, **kwargs)
        else:
            return forms.CharField()
            
class Variable(models.Model):
    """ A variable that data values can be bound to.  The variable specifies what units
        the values are stored in. 
    """
    
    label = models.CharField(max_length=80)
    description = models.TextField(default='')
    unit = models.ForeignKey(BaseUnit)
    tags = models.ManyToManyField(Tag, blank=True)
    varType = models.ForeignKey(VarType)
    
    def __unicode__(self):
        if len(self.unit.symbol.strip()) == 0:
            return u'%s' % self.label
        else:
            return u'%s (%s)' % (self.label, self.unit.symbol)
        
    def latest_value(self):
        """ Get the most recent value bound to a variable 
            (or None if there aren't any).
        """
        if self.datavalue_set.all().exists():
            return self.datavalue_set.all().order_by('-timestamp')[0]
        else:
            return None
            
    def new_value(self, category):
        """ Create a new value for this variable, but don't save it yet. """
        
        val = DataValue(variable=self, category=category)
        return val
    
    #   A property for accessing the latest value of a variable directly.
    def _get_current_data(self):
        self._last_value = self.latest_value()
        if self._last_value:
            return self._last_value.data
        else:
            return None
    def _set_current_data(self, val):
        #   Create a new value matching the characteristics of the previous one
        #   (Values can be set here, automatically saving a new version; they 
        #   must be created as DataValue instances to provide metadata.)
        if not hasattr(self, '_last_value'):
            self._last_value = self.latest_value()
            if not self._last_value:
                raise RuntimeError('No value assigned to variable')
        new_value = self._last_value.clone()
        new_value.data = val        
        new_value.save()
    current_data = property(_get_current_data, _set_current_data)
    
class DataValue(models.Model):
    """ A value that can be bound to a variable.  Has a lot of optional fields
        that can be set in views to improve usability.
    
        The actual data is pickled and stored in '_data'; data can be any Python type.
        Be careful that the type is consistent between different values of a 
        variable (the database does not enforce this).
    """
    
    variable = models.ForeignKey(Variable)
    timestamp = models.DateTimeField(auto_now=True)
    _data = models.TextField(verbose_name='Picked data', help_text='Do not edit this value in the admin interface; it is dynamically typed.')   #   pickled - see 'data' property below
    supplier = models.ForeignKey(Tool, blank=True, null=True)
    user = models.ForeignKey(EDSAUser, blank=True, null=True)
    category = models.ForeignKey(DataCategory, related_name='variable_category')
    namespace = models.ForeignKey(ValueNamespace, related_name='variable_namespace', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    #   Eventually: add some uncertainty measure
    
    #   A property for accessing the underlying data in whatever Python type it
    #   was originally stored in.  Special-cased to automatically handle
    #   FileValues and their derived objects (the original FileValue must be 
    #   pickled and re-converted to the derived object when unpickled in order
    #   to work across Pyro invocations.
    def _get_data(self):
        if len(self._data) > 0:
            result = pickle.loads(str(self._data))
            if hasattr(result, 'cast'):
                return result.cast()
            else:
                return result
        else:
            #   Data not initialized - set to None.
            self._data = pickle.dumps(None)
            return None
    def _set_data(self, data):
        if hasattr(data, 'uncast'):
            self._data = pickle.dumps(data.uncast)
        else:
            self._data = pickle.dumps(data)
    data = property(_get_data, _set_data)

    def __unicode__(self):
        return u'%s = %s - %s value from %s' % (self.variable, self.data, self.category.label, self.timestamp)
    
    def clone(self):
        """ Make a copy of this value, perhaps for initializing it in a new
            namespace.
        """
        
        #   Iterate over all data fields in the instance
        new_value = DataValue()
        for field in self._meta.fields:
            #   Copy over attributes and [foreign key] related objects
            if type(field) == models.AutoField:
                pass
            else:
                setattr(new_value, field.name, getattr(self, field.name))
        new_value.save()
        for field in self._meta.many_to_many:
            #   Copy over [many to many] related objects
            for item in getattr(self, field.name).all():
                getattr(new_value, field.name).add(item)
        return new_value
    

class FileValue(models.Model):
    """ Encodes an object that is stored in a file.  Calling the cast()
        function returns an object that can be
        pickled and stored in the database as a DataValue.  No other metadata
        is kept around besides the ID, so it is recommended that the values
        are bound to variables and saved.
        
        The type must be defined as a RegisteredPythonModule, which can be in 
        the EDSA repository or local to certain machines.  Its constructor
        should accept a keyword argument 'file' containing a file-like object
        with methods 'read', 'seek', 'tell', and 'close'.  The object can be
        cached locally and the methods used to fetch data from the file as
        necessary.
    
    """
    machines = models.ManyToManyField(Machine, through='FileInstance')
    value_type = models.ForeignKey(RegisteredPythonModule)
    
    def __unicode__(self):
        return '%s #%d' % (self.value_type.class_name, self.id)
    
    def cast(self, machine=None):
        """ Retrieve a RemoteFile proxy on the specified machine.    """
        from edsa.clients.pyro import pyro_manager
        
        if machine not in self.machines.all():
            machine = random.choice(self.machines.all())
        instance = FileInstance.objects.get(value=self, machine=machine)
        
        name_list = pyro_manager.get_names()
        for item in name_list:
            if get_object_label(item[0]) == generate_object_label(instance):
                if machine.label == get_machine_name(item[0]):
                    remote_obj = item[1].getAttrProxy()
                    result = self.value_type.get_class()(remote_obj)
                    #   Save original FileValue as the result of an 'uncast' function
                    result.uncast = self
                    return result
    
class FileInstance(models.Model):
    """ Track an instance of a file-based object (FileValue).  A FileValue can
        be stored on multiple machines on the network and synchronized
        between the machines using rsync.  The purpose of this model is to
        abstract these components away so that the FileValue can be used locally
        wherever it is needed.
    """
    machine = models.ForeignKey(Machine)
    value = models.ForeignKey(FileValue)
    relative_path = models.CharField(max_length=255)
    revision = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    exists = models.BooleanField()
    
    def __unicode__(self):
        if self.exists:
            status_msg = 'on'
        else:
            status_msg = 'missing from'
        return '%s (rev %d) %s %s' % (self.relative_path, self.revision, status_msg, self.machine.label)
    
class Constraint(models.Model):
    """ Base class for a constraint that can be applied to a set of variables 
        that evaluates to True (satisfied) or False (unsatisfied).
    """
    variables = models.ManyToManyField(Variable, related_name='constraint_variables')
    
    def evaluate(self, values):
        raise NotImplementedError
    
class LimitConstraint(Constraint):
    """ A basic example of a Constraint implementation.
        Establishes hard limits on a set of variables.
    """
    
    min_values = models.TextField()
    max_values = models.TextField()
    
    def evaluate(self, values):
        min = [float(x) for x in min_values.split(',')]
        max = [float(x) for x in max_values.split(',')]
        for i in range(len(values)):
            if values[i] < min[i] or values[i] > max[i]:
                return False
        return True
