import xstack
import qtility
import crosswalk
from Qt import QtWidgets

from . import config
from ..core import Exporter


def launch(blocking=False):

    q_app = qtility.app.get()
    exporter = Exporter()
    app = xstack.launch(
        app_config=config.AppConfig,
        blocking=False,
        active_stack=exporter,
        parent=qtility.windows.application(),
        storage_identifier=f"{crosswalk.module_name}_dcc_exporter",
        allow_threading=False,
    )

    # -- Expose a general export button which will export all
    # -- given configs.
    export_button = QtWidgets.QPushButton("Export")
    export_button.clicked.connect(app.core.build)
    app.core.layout().addWidget(export_button)

    if blocking:
        q_app.exec_()
