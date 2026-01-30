import xstack
import qtility
import crosswalk

from . import config
from ..core import Exporter


def launch(blocking=False):

    q_app = qtility.app.get()
    exporter = Exporter()
    app = xstack.launch(
        app_config=config.AppConfig,
        blocking=blocking,
        active_stack=exporter,
        parent=qtility.windows.application(),
        storage_identifier=f"{crosswalk.module_name}_dcc_exporter",
        allow_threading=False,
    )
