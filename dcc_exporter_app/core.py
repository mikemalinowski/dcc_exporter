import qtility
import dcc_exporter

from xstack_app.add import AddComponentWidget
from xstack_app.options import ComponentEditor
from Qt import QtWidgets, QtCore, QtGui

from . import config
from . import resources
from . import uic_app


# --------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
class ExporterWidget(QtWidgets.QWidget):

    # ----------------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(ExporterWidget, self).__init__(parent=parent)

        # -- Instance the exporter
        self.exporter = dcc_exporter.Exporter()

        # -- Start building the layout
        self.setLayout(
            qtility.layouts.slimify(
                QtWidgets.QHBoxLayout(),
            ),
        )

        self.ui = uic_app.Ui_Form()
        self.ui.setupUi(self)

        # self.layout().addWidget(self.ui)
        self.layout().addLayout(self.ui.verticalLayout_4)

        # -- Show the version to the user
        self.ui.version_label.setText(f"v{dcc_exporter.__version__}")

        # -- Use this to store a reference to the definition add window
        self.add_definition_window = None

        # # -- Define the option panel - this is where we show any options
        # # -- an export type will show
        self.option_panel = ComponentEditor(parent=self)
        self.ui.options_layout.addWidget(self.option_panel)

        self.populate()

        self.ui.add_button.clicked.connect(self.add)
        self.ui.remove_button.clicked.connect(self.remove)
        self.ui.export_button.clicked.connect(self.export)
        self.ui.export_list.currentItemChanged.connect(self.on_export_selection_change)

    # ----------------------------------------------------------------------------------
    def populate(self):

        self.ui.export_list.clear()

        for entry in self.exporter.components():

            item = QtWidgets.QListWidgetItem(entry.label())

            if entry.icon:
                item.setIcon(QtGui.QIcon(entry.icon))

            item.uuid = entry.uuid()

            self.ui.export_list.addItem(item)

    # ----------------------------------------------------------------------------------
    def add(self):

        self.add_definition_window = AddComponentWidget(
            stack=self.exporter,
            component_parent=None,
            app_config=config.AppConfig,
            parent=self,
        )

        self.add_definition_window.component_added.connect(self.populate)

        self.add_definition_window.show()

    # ----------------------------------------------------------------------------------
    def remove(self):

        confirmation = qtility.request.confirmation(
            title="Remove Export Entries",
            label="Are you sure?",
            parent=self,
        )

        if not confirmation:
            return

        for item in self.ui.export_list.selectedItems():
            self.exporter.remove_component(
                self.exporter.component(
                    item.uuid,
                ),
            )

        self.populate()

    # ----------------------------------------------------------------------------------
    def export(self):

        components_to_export = list()

        for item in self.ui.export_list.selectedItems():
            components_to_export.append(
                self.exporter.component(item.uuid),
            )

        self.exporter.export(export_only=components_to_export)

        qtility.request.message(
            title="Export Complete",
            label="Export Complete",
            parent=self,
        )

    # ----------------------------------------------------------------------------------
    def on_export_selection_change(self, *args, **kwargs):
        """
        We use this as a pass-through mechanism, so that when a component is selected
        in the tree view we call the set_component in the editor panel.
        """
        try:
            export_entry = self.exporter.component(
                self.ui.export_list.currentItem().uuid,
            )

        except AttributeError:
            return

        if not export_entry:
            return

        self.option_panel.set_component(export_entry)


# --------------------------------------------------------------------------------------
class ExporterWindow(qtility.windows.MemorableWindow):

    # ----------------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(ExporterWindow, self).__init__(parent=parent, storage_identifier="DCCExporter")

        self.setWindowTitle("Exporter")

        self.setCentralWidget(ExporterWidget(parent=self))

        qtility.styling.apply(
            [
                resources.get("exporter_app.css"),
            ],
            apply_to=self,
        )


# --------------------------------------------------------------------------------------
def launch(blocking=False):

    q_app = qtility.app.get()

    w = ExporterWindow(parent=qtility.windows.application())
    w.show()


    if blocking:
        q_app.exec_()
