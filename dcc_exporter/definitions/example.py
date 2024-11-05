import dcc_exporter


# --------------------------------------------------------------------------------------
class ExampleExportDefintion(dcc_exporter.ExportDefinition):

    identifier = "Example Definition"
    icon = ""

    # ----------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ExampleExportDefintion, self).__init__(*args, **kwargs)

        self.declare_option(
            name="Rig",
            value="",
            group="Scene",
        )

        self.declare_option(
            name="Start Frame",
            value=0.0,
        )

        self.declare_option(
            name="End Frame",
            value=30.0,
        )

        self.declare_option(
            name="Save Path",
            value="",
        )

    # ----------------------------------------------------------------------------------
    def run(self) -> bool:

        # -- Read the option data
        rig = self.option("Rig").get()

        # -- Read the time data
        start_frame = self.option("Start Frame").get()
        end_frame = self.option("End Frame").get()

        # -- Get the path we want to save to
        save_path = self.option("Save Path").get()

        # -- Now we cna do whatever logic we want/need to be able export
        print("exporting....")

        return True
