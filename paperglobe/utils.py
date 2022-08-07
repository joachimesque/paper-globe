"""Utils"""

from pathlib import Path


def format_output_filename(file, print_size):
    """Returns the name of the output file

    Parameters
    ----------
    file : str
        path of the image file to be used to generate the template
    print_size : str
        printing size of the template. one of:
            - "a4"
            - "us-letter"

    Returns
    -------
    tuple : (str, str)
        the name of the destination file, the original name of the file
    """

    filename = Path(file).stem[:40]
    original_filename = Path(file).name

    return (f"paperglobe_{filename}_{print_size}.pdf", original_filename)
