import os
import json
import typing
import xstack

from crosswalk import app

from . import definition
from . import constants


# --------------------------------------------------------------------------------------
# noinspection PyTypeChecker
class Exporter(xstack.Stack):

    # ----------------------------------------------------------------------------------
    def __init__(self, component_paths: typing.List or None = None):
        super(Exporter, self).__init__(
            label=constants.LABEL,
            component_paths=component_paths,
            component_base_class=definition.ExportDefinition,
        )


        # -- If we're not given a host, then we need to add one
        if not app.objects.exists(constants.LABEL):
            self._host = self._create_host(constants.LABEL)

        else:
            self._host = app.objects.get_object("Exporter")

        # -- Ensure we add any paths set by the environment
        paths = os.environ.get(constants.EXPORTER_DEFINITION_PATHS_ENVVAR, "").split(",")

        paths.append(
            os.path.join(
                os.path.dirname(__file__),
                "definitions",
            ),
        )

        for path in paths:
            if path:
                self.component_library.register_path(path)

        self.deserialize(
            json.loads(
                app.attributes.get_attribute(
                    self.host(),
                    "exporter_data",
                ),
            )
        )

        # -- As we have now populated the class, emit the fact that the class has
        # -- changed
        self.changed.connect(
            self.serialise,
        )

    # ----------------------------------------------------------------------------------
    def add_definition(self, defintion_type, label, options):
        return self.add_component(
            component_type=defintion_type,
            label=label,
            options=options,
        )

    # ----------------------------------------------------------------------------------
    def instances(self, of_type=None):
        return self.components(of_type=of_type)

    # ----------------------------------------------------------------------------------
    @property
    def definition_library(self):
        return self.component_library

    # ----------------------------------------------------------------------------------
    def host(self):
        return self._host

    # ----------------------------------------------------------------------------------
    @property
    def label(self):
        """
        We always want to return the name of the host when getting the label
        """
        return app.objects.get_name(self.host())

    # ----------------------------------------------------------------------------------
    @label.setter
    def label(self, v):
        """
        Our label is always defined by the name of the host
        """
        pass

    # ----------------------------------------------------------------------------------
    def serialise(self) -> typing.Dict:
        """
        We subclass the serialise function so that we can take the serialised
        data and store it within the host object
        """
        data = super(Exporter, self).serialise()

        app.attributes.set_attribute(
            object_=self.host(),
            attribute_name="exporter_data",
            value=json.dumps(data),
        )

        return data

    # ----------------------------------------------------------------------------------
    @classmethod
    def _create_host(cls, name: str):
        """
        This will create the host object within the applications scene. It ensures the host
        has the right attributes to be able to store its serialised
        """
        host = app.objects.create(
            name=name,
        )

        app.attributes.add_float_attribute(
            object_=host,
            attribute_name="exporter_node",
            value=1,
        )

        app.attributes.add_string_attribute(
            object_=host,
            attribute_name="exporter_data",
            value="{}"
        )

        return host

    # ----------------------------------------------------------------------------------
    # noinspection PyBroadException
    def export(
        self,
        export_only: list = None,
    ) -> bool:
        """
        We re-implement the build to allow us to check whether we have a rig configuration
        component in a stack. If we do not, or if it is not valid then we do not allow
        the build to continue
        """

        return super(Exporter, self).build(
            build_only=export_only,
        )
