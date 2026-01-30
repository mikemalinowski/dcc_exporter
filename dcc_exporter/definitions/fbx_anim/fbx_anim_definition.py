"""
This is a generalised Fbx Animation export. Given a skeleton
root it will export that and place it at the scene root as well
as removing namespaces.

This expects the fbx module to be available (which does not come
with the dcc exporter module).
"""
import os
import maya
import fbxtra
import pathlib
import dcc_exporter
from maya import cmds as mc


class FbxAnimationExport(dcc_exporter.ExportDefinition):
    """
    Exports skeletal animation - removing namespaces and parent nodes.
    """
    identifier = "Fbx Animation"

    def __init__(self, *args, **kwargs):
        super(FbxAnimationExport, self).__init__(*args, **kwargs)

        self.declare_option(
            name="Export Path",
            value="",
            group="Inputs/Outputs",
            description="This is the path the animation should be exported to",
        )
        self.declare_option(
            name="Skeletal Root",
            description=(
                "The root joint of the rig to be exported. "
                "All recursive children will be exported."
            ),
            value="",
            group="Inputs/Outputs",
        )

        self.declare_option(
            name="Start Frame",
            value=int(mc.playbackOptions(query=True, min=True)),
            group="General",
            description="The frame number to start exporting",
            pre_expose=True,
        )

        self.declare_option(
            name="End Frame",
            value=int(mc.playbackOptions(query=True, min=True)),
            group="General",
            description="The last frame to export",
            pre_expose=True,
        )

        self.declare_option(
            name="Remove Root Motion",
            value=False,
            group="General",
            description="Removes the keys on the translation/rotation/scale of the root bone",
            pre_expose=True,
        )

    def option_widget(self, option_name: str) -> "PySide6.QWidget":
        """
        Return bespoke widgets for the objects and filepath options
        """
        if option_name == "Skeletal Root":
            return dcc_exporter.widgets.ObjectSelector()
        if option_name == "Export Path":
            return dcc_exporter.widgets.FilepathSelector()

    def validate(self) -> bool:
        """
        Ensure that the variables we have been given are valid
        before we attempt to export.
        """
        skeleton_root = self.option("Skeletal Root").get()
        if not skeleton_root or not mc.objExists(skeleton_root):
            print("You must provide a valid Skeletal Root")
            return False

        if not self.option("Export Path").get():
            print("You must provide a valid Export Path")
            return False

        return True

    def run(self) -> bool:
        """
        This is called when the user instigates the export.
        """
        # -- Read out our option values
        skeletal_root = self.option("Skeletal Root").get()
        export_path = pathlib.Path(self.option("Export Path").get()).as_posix()
        start_frame = int(self.option("Start Frame").get())
        end_frame = int(self.option("End Frame").get())

        # -- Get a list of all the joints which we expect to export
        exportable_joints = mc.listRelatives(
            skeletal_root,
            ad=True,
            type="joint",
        )
        exportable_joints.insert(0, skeletal_root)

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

        # -- Set our time frame settings
        maya.mel.eval(f"FBXExportBakeComplexStart -v {start_frame}")
        maya.mel.eval(f"FBXExportBakeComplexEnd -v {end_frame}")

        # -- Attempt to export the fbx file. This needs to be done through
        # -- mel due to a niggle with maya.
        mc.select(exportable_joints)
        maya.mel.eval(f"FBXExport -f \"{export_path}\" -s")

        # -- Now we can start to use the Fbx Sdk to wrangle the fbx file
        # -- into a game ready state
        # -- Now we open the Fbx file to clean it
        fbx_scene = fbxtra.files.load(export_path)

        # -- Remove namespaces
        fbxtra.scene.clear_namespaces(fbx_scene)

        # -- Get the skeleton root
        local_skeletal_root = skeletal_root.split(":")[-1]
        fbx_skeletal_root = fbxtra.scene.get(fbx_scene, name=local_skeletal_root)
        fbxtra.node.set_parent(fbx_skeletal_root, parent=None)

        # -- Remove all items that are not part of the skeleton
        fbxtra.scene.clear(fbx_scene, excluding=[fbx_skeletal_root])

        # -- Remove animation on teh skeletal root if that ooption
        # -- is ticked.
        if self.option("Remove Root Motion").get():
            fbxtra.animation.remove_tr_keys(
                fbx_skeletal_root,
                zero=True,
            )

        # -- Ensure the time frame is specifically set
        fbxtra.animation.set_time_range(
            fbx_scene,
            start_frame,
            end_frame,
        )
        fbxtra.animation.shift_all_keys(
            fbx_scene,
            offset=-start_frame,
            reframe=True,
        )

        # -- Name the take according to the file name, removing the
        # -- suffix
        fbxtra.animation.set_current_take_name(
            fbx_scene,
            ".".join(os.path.basename(export_path).split(".")[:-1])
        )

        # -- Finally, save the fbx file
        fbxtra.files.save(fbx_scene, export_path)

        return True