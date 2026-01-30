import maya
import pathlib
import dcc_exporter
import maya.cmds as mc


class FbxSimple(dcc_exporter.ExportDefinition):
    """
    Exports any objects you declare (along with their parents).
    """
    identifier = 'Fbx Simple'

    def __init__(self, *args, **kwargs):
        super(FbxSimple, self).__init__(*args, **kwargs)

        self.declare_option(
            name="Export Path",
            value="",
            group="Inputs/Outputs",
            description="This is the path the mesh should be exported to",
        )

        self.declare_option(
            name="Objects",
            description="List of objects that should be exported",
            value=[],
            group="General"
        )

    def option_widget(self, option_name: str) -> "PySide6.QWidget":
        """
        Return bespoke widgets for the objects and filepath options
        """
        if option_name == "Objects":
            return dcc_exporter.widgets.ObjectList()

        if option_name == "Export Path":
            return dcc_exporter.widgets.FilepathSelector(
                default_value=self.option("Export Path").get(),
            )

    def validate(self) -> bool:
        """
        Ensure that the variables we have been given are valid
        before we attempt to export.
        """
        if not self.option("Export Path").get():
            print("You must provide a valid Export Path")
            return False

        if not self.option("Objects").get():
            print("No meshes specified")
            return False

        for item in self.option("Objects").get():
            if not mc.objExists(item):
                print(f"{item} does not exist")
                return False
        return True

    def run(self) -> bool:
        """
        This is called when the user instigates the export.
        """
        export_path = pathlib.Path(self.option("Export Path").get()).as_posix()
        items = self.option("Objects").get()

        # -- Declare the Fbx settings using a preset file for the
        # -- static values
        preset_path = pathlib.Path(
            __file__.replace(
                ".py",
                ".fbxexportpreset",
            ),
        ).as_posix()

        # -- Load in the preset
        maya.mel.eval('FBXResetExport')
        maya.mel.eval(f'FBXLoadExportPresetFile -f "{preset_path}"')

        # -- Attempt to export the fbx file. This needs to be done through
        # -- mel due to a niggle with maya.
        mc.select(items)
        maya.mel.eval(f"FBXExport -f \"{export_path}\" -s")
