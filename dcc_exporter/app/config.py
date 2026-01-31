import xstack

from . import resources
from ..core import Exporter


class AppConfig(xstack.app.AppConfig):
    label = "Exporter"
    component_label = "Export Definition"
    execute_label = "Export"
    header_label = "Exports"
    stack_class = Exporter
    show_tree_header = False
    splitter_bias = 0.4
    show_menu_bar = False
    forced_orientation = "horizontal"  # -- Alternative is "horizontal"

    # -- These let you tailor the icons which will be displayed for various
    # -- items and actions
    icon = resources.get("icon.png")
    component_icon = resources.get("icon.png")

    # -- These are how the background of the stack should show
    splash_image = resources.get("icon.png")
    stack_background = resources.get("stack_background.png")