from paperglobe import get_stripes, write_pdf, STATUS_TYPES, format_output_filename


class PaperGlobe:
    """The main class for the PaperGlobe module

    Attributes
    ----------
    status : tup
        a tuple containing the status type and the status message
    on_update : function
        function to be executed on status change
    bold : function
        function to be executed to style some texts inside the status message

    Methods
    -------
    update_status(status_type, message)
        updates self.status and executes on_update
    generate_paperglobe(file, projection, print_size)
        runs the paper globe generation and calls status updates
    """

    def __init__(self, on_update=None, bold=lambda x: x):
        """
        Parameters
        ----------
        on_update : function, optional
            function to be executed on status change
        bold : function, optional
            function to be executed to style some texts inside the status message
        """
        
        self.status = (None, "")
        self.on_update = on_update
        self.bold = bold

    def update_status(self, status_type, message):
        """Updates self.status and executes on_update

        Parameters
        ----------
        status_type : string
            type of status. one of:
                - "error"
                - "warning"
                - "info"
        message : string
            status message to be displayed
        """

        self.status = (status_type, message)
        if callable(self.on_update):
            self.on_update(status_type, message)

    def generate_paperglobe(self, file, projection, print_size):
        """Runs the paper globe template generation and calls status updates

        Parameters
        ----------
        file : str
            path of the image file to be used to generate the template
        projection : str
            type of projection. one of:
                - "equirectangular"
                - "mercator"
                - "gall-stereo"
        print_size : str
            printing size of the template. one of:
                - "a4"
                - "us-letter"
        """

        self.update_status(
            STATUS_TYPES["INFO"],
            f"{self.bold(file)} has been found, starting conversion. 🧑‍🚀🪄 🗺",
        )

        try:
            stripes = get_stripes(file, projection)
            write_pdf(file, stripes, print_size)
        except Exception as ex:
            self.update_status(
                STATUS_TYPES["ERROR"],
                f"The file couldn’t be written ({self.bold(type(ex).__name__)})",
            )
        else:
            filename = format_output_filename(file, print_size)
            self.update_status(
                STATUS_TYPES["INFO"],
                f"The file {self.bold(filename)} has been saved 🧑‍🚀 ✨🌏🌍🌎✨",
            )
