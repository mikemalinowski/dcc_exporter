import xstack_app
import dcc_exporter


class AppConfig(xstack_app.AppConfig):
    label = "Exporter"
    component_label = "Export Definition"
    execute_label = "Export"
    stack_class = dcc_exporter.Exporter
