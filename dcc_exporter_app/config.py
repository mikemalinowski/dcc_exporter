import dcc_exporter
from dcc_exporter.vendor import xstack_app


class AppConfig(xstack_app.AppConfig):
    label = "Exporter"
    component_label = "Export Definition"
    execute_label = "Export"
    stack_class = dcc_exporter.Exporter
