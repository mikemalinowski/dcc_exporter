"""
This is open source application agnostic exporter ui. It makes no assumption about
the application it is running in, and no assumption about the type of data being
exported.

This framework is built on top of the xstack framework which tailors it toward
exporting and gives it its own UI. It does however still use the xstack widgets
for representing option ui elements.

Repository:
https://github.com/mikemalinowski/dcc_exporter
"""
from .core import launch

__version__ = '1.0.1'
