import math
import os

from fitz import fitz

from paperglobe import format_output_filename, PRINT_SIZES


def write_pdf(file, stripes, print_size):
    """Place the stripe Image objects onto the PDF

    If will take a list of stripes and inserts each one at its right position
    on the right page of the right PDF template file

    Parameters
    ----------
    file : str
        path of the image file to be used to generate the template
    stripes : list
        a list of Image objects
    print_size : str
        printing size of the template. one of:
            - "a4"
            - "us-letter"
    """

    output_filename = format_output_filename(file, print_size)
    pdf_path = os.path.join(
        os.path.dirname(__file__), f"assets/template-{print_size}.pdf"
    )

    pdf = fitz.open(pdf_path)

    for index, stripe in enumerate(stripes):
        stripe.transform_colorspace("cmyk")
        stripe_blob = stripe.make_blob("png")
        page = pdf[math.floor(index / 2)]

        """On each page, two stripes are displayed.
           Both share the same `y` coordinates but have different `x` coordinates.
        """
        positions = {
            PRINT_SIZES["A4"]: {
                "x": ((66.5, 251.3), (344, 528.7)),
                "y": (65.5, 776.4),
            },
            PRINT_SIZES["US_LETTER"]: {
                "x": ((74.9, 259.6), (352.4, 537.1)),
                "y": (40.5, 751.5),
            },
        }

        rect = fitz.Rect(
            positions[print_size]["x"][index % 2][0],
            positions[print_size]["y"][0],
            positions[print_size]["x"][index % 2][1],
            positions[print_size]["y"][1],
        )

        if not page.is_wrapped:
            page.wrap_contents()

        page.insert_image(rect, stream=stripe_blob)

    pdf.save(output_filename)
