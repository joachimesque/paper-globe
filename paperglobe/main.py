from paperglobe import get_stripes, write_pdf, STATUS_TYPES, format_output_filename


class PaperGlobe:
    """The main class for the PaperGlobe module


    """

    def __init__(self, on_update=None, bold=lambda x: x):
        
        self.status = (None, "")
        self.on_update = on_update
        self.bold = bold

    def update_status(self, status_type, message):

        self.status = (status_type, message)
        if callable(self.on_update):
            self.on_update(status_type, message)

    def generate_paperglobe(self, file, projection, print_size):

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
