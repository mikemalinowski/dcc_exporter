"""
This is open source application agnostic export framework. It makes no assumption about
the application it is running in, and no assumption about the type of data being
exported.

All export types are declared using a plugin approach. You must implement an
ExportDefinition class where you can declare option data and implement the run
function to suit your needs.

This framework is built on top of the xstack framework.

Repository:
https://github.com/mikemalinowski/dcc_exporter
"""
from .core import Exporter
from .definition import ExportDefinition

# -- We do not force a hard reliance on the ui as we allow this module
# -- to operate in a completely headless environment.
try:
    from . import widgets
    from . import app
    from .app.core import launch

except ImportError:
    print("running with no qt support")

__version__ = '1.0.1'
