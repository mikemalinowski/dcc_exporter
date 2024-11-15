from .vendor import xstack


# --------------------------------------------------------------------------------------
class ExportDefinition(xstack.Component):

    # ----------------------------------------------------------------------------------
    # This MUST be re-implemented
    def run(self) -> bool:
        """
        This should be re-implemented in your export definition and should contain all the
        code which you want to trigger during the export.
        """
        return True

    # ----------------------------------------------------------------------------------
    # You may re-implement this
    def is_valid(self) -> bool:
        """
        You can use this to test the validation of the options and environment.
        """
        return True

    # ----------------------------------------------------------------------------------
    # You may re-implement this
    def option_widget(self, option_name: str) -> "PySide6.QWidget":
        """
        This allows you to return a specific (or custom) QWidget to represent the
        given option in any ui's.

        This requires Qt, which is optional.

        For example, your code here might look like this:

        ```
        if option_name == "foobar":
            return qute.QLineEdit()
        ```

        If you do not want a specific option to be shown in the ui, you can do:

        if option_name == "foobar":
            return self.IGNORE_OPTION_FOR_UI
        """
        return None
