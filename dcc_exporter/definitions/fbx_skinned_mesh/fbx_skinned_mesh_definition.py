import maya
import fbxtra
import pathlib
import dcc_exporter
import maya.cmds as mc


class FbxSkeletalMesh(dcc_exporter.ExportDefinition):
    """
    Exports a skeleton and declared meshes.
    """
    identifier = "Fbx Skeletal Mesh"

    def __init__(self, *args, **kwargs):
        super(FbxSkeletalMesh, self).__init__(*args, **kwargs)

        self.declare_option(
            name="Export Path",
            value="",
            group="Inputs/Outputs",
            description="This is the path the skeletal mesh should be exported to",
        )

        self.declare_option(
            name="Skeletal Root",
            description=(
                "The root joint of the rig to be exported. "
                "All recursive joints will be exported."
            ),
            value="",
            group="Inputs/Outputs",
        )

        self.declare_option(
            name="Meshes",
            description="List of meshes that should be exported",
            value=[],
            group="Inputs/Outputs"
        )

    def option_widget(self, option_name: str) -> "PySide6.QWidget":
        """
        Return bespoke widgets for the objects and filepath options
        """
        if option_name == "Skeletal Root":
            return dcc_exporter.widgets.ObjectSelector()
        if option_name == "Export Path":
            return dcc_exporter.widgets.FilepathSelector()
        if option_name == "Meshes":
            return dcc_exporter.widgets.ObjectList()

    def validate(self) -> bool:
        """
        Ensure that the variables we have been given are valid
        before we attempt to export.
        """
        if not self.option("Export Path").get():
            print("You must specify an export path")
            return False

        if not self.option("Skeletal Root").get():
            print("You must specify a skeletal root")
            return False

        meshes = self.option("Meshes").get()

        if not meshes:
            print("You must specify at least one mesh")
            return False

        for mesh in meshes:
            if not mc.objExists(mesh):
                print(f"{mesh} does not exist")
                return False

        return False

    def run(self) -> bool:
        """
        This is called when the user instigates the export.
        """
        # -- Read our options
        skeletal_root = self.option("Skeletal Root").get()
        meshes = self.option("Meshes").get()
        export_path = pathlib.Path(self.option("Export Path").get()).as_posix()

        # -- Get a list of exportable items
        exportable_items = mc.listRelatives(
            skeletal_root,
            allDescendents=True,
            type="joint",
        ) + [skeletal_root] + meshes

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
        mc.select(exportable_items)
        maya.mel.eval(f"FBXExport -f \"{export_path}\" -s")

        # -- Now we can start to use the Fbx Sdk to wrangle the fbx file
        # -- into a game ready state
        # -- Now we open the Fbx file to clean it
        fbx_scene = fbxtra.files.load(export_path)

        # -- Remove namespaces
        fbxtra.scene.clear_namespaces(fbx_scene)

        # -- Parent the skeletal root to the scene root
        fbx_skeletal_root = fbxtra.scene.get(
            fbx_scene,
            name=self._get_local_name(skeletal_root),
        )
        fbxtra.node.set_parent(fbx_skeletal_root, parent=None)

        # -- Make all the meshes also be a child of the world
        fbx_mesh_nodes = []
        for mesh in meshes:
            fbx_mesh = fbxtra.scene.get(fbx_scene, self._get_local_name(mesh))
            fbx_mesh_nodes.append(fbx_mesh)
            fbxtra.node.set_parent(fbx_skeletal_root, parent=None)

        # -- Remove everything else
        fbxtra.scene.clear(
            fbx_scene,
            excluding=[fbx_skeletal_root] + fbx_mesh_nodes,
        )

        # -- Finally we save the wrangled file
        fbxtra.files.save(fbx_scene, export_path)

        return True

    @classmethod
    def _get_local_name(cls, name):
        """
        Returns the given name with the namespace stripped
        """
        return name.split(":")[-1]
