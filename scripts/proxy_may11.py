from edsa.clients.pyro import pyro_manager
from edsa.clients.models import Tool

tool = Tool.objects.get(id=3)
tp = tool.get_proxy()
print tp

