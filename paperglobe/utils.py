from pathlib import Path


def format_output_filename(file, print_size):
    """Returns the name of the output file"""

    return f"{Path(file).stem}_{print_size}.pdf"
