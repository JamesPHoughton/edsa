
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
from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

register = template.Library()

@register.tag
def render_dependencies(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, task = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return DependenciesNode(task)

def render_task_dependencies(task, parent=None, root_id=None, history=[]):
    result = '<li>%s' % task.tool
    if parent:
        parent_id = parent.id
    else:
        parent_id = -1
    if parent is None:
        root_id = task.id
    context = {'task': task, 'parent_id': parent_id, 'root_id': root_id, 'history': history}
    result += render_to_string("ajax_fragments/dependency_entry.html", context)
    if task.dependencies.count() > 0:
        result += '<ul>'
        for dep in task.dependencies.all().order_by('id'):
            result += render_task_dependencies(dep, task, root_id, history + [task.id]) 
        result += '</ul>'
    result += '</li>'
    return result

class DependenciesNode(template.Node):
    def __init__(self, task):
        self.task_name = task
    def render(self, context):
        task = context[self.task_name]
        return render_task_dependencies(task)
        