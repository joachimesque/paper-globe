from paperglobe import get_stripes, write_pdf


def generate_paperglobe(file, projection, print_size):
    """Basic app flow"""

    stripes = get_stripes(file, projection)
    status = write_pdf(file, stripes, print_size)

    return status
