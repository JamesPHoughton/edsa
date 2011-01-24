
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
""" EDSA Tag models

The tagging models are very abstract and will likely see greater use in later
phases of the EDSA program.  These models are derived from Tag, which is
essentially a string (albeit in short and long forms) stored in a forest structure.
Each instance of Tag refers to its parent Tag (or None, if it is a 'root node').

Each category of tags should have its own root node.  This allows code to easily
select the subset of tags relevant to a particular task.

Subclasses of Tag are introduced to avoid confusion with foreign keys from other
structures.  For example, DataValues are assigned a category, but only some Tags
are actually meant to represent categories.  These Tags are created as instances
of a DataCategory model to make that separation more explicit.
"""

from django.db import models
from django.db.models import signals as model_signals

import mptt
from mptt.models import MPTTModel
from mptt.signals import pre_save

#   Add fields and manager to make Tags a nested-sets tree
class Tag(MPTTModel):
    """ Base class for EDSA tags. 
        Needs to have some kind of hierarchy (tree anchor). 
        For now, assume the 'label' is a hierarchical URI.
    """
    label = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return u'%s' % self.label

class DataCategory(Tag):
    """ A tag that describes the level of confidence and intended purpose for
        some piece of data.  Examples include:
        -   variable
        -   assumption
        -   requirement
        -   guess
        -   measurement
    """
    
    """ Static methods for tag elements that should be readily available. """
    @staticmethod
    def root():
        result, created = Tag.objects.get_or_create(label='Data categories', parent=None)
        return result
    
    @staticmethod
    def default():
        result, created = DataCategory.objects.get_or_create(label='Wild guess', parent=DataCategory.root())
        return result

#   The following options are required for the admin interface to work.
#   (The subclasses of Tag should not be registered separately since MPTT
#   doesn't deal correctly with Django subclassing.)
DataCategory._mptt_meta.tree_id_attr = 'tree_id'
DataCategory._mptt_meta.parent_attr = 'parent'
DataCategory._mptt_meta.left_attr = 'lft'
DataCategory._mptt_meta.order_insertion_by = None
model_signals.pre_save.connect(pre_save, sender=DataCategory)

class ValueNamespace(Tag):
    """ A tag that describes what project or effort a data value pertains to.
        This makes it possible to decide whether to re-run tasks in order
        to recalculate values in the desired namespace.
    """
    
    """ Static methods for tag elements that should be readily available. """
    @staticmethod
    def root():
        result, created = Tag.objects.get_or_create(label='Namespaces', parent=None)
        return result
    
    @staticmethod
    def default():
        result, created = DataCategory.objects.get_or_create(label='Default', parent=ValueNamespace.root())
        return result
    
ValueNamespace._mptt_meta.tree_id_attr = 'tree_id'
ValueNamespace._mptt_meta.parent_attr = 'parent'
ValueNamespace._mptt_meta.left_attr = 'lft'
ValueNamespace._mptt_meta.order_insertion_by = None
model_signals.pre_save.connect(pre_save, sender=ValueNamespace)
