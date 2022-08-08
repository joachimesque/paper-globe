"""Exports a list of stripes to PDF"""

import math
import os

from fitz import fitz

from paperglobe.config import PRINT_SIZES

PDF_STRIPE_HEIGHT = 710.9


def write_pdf(stripes, print_size, out_path):
    """Place the stripe Image objects onto the PDF

    If will take a list of stripes and inserts each one at its right position
    on the right page of the right PDF template file

    Parameters
    ----------
    stripes : list
        a list of Image objects
    print_size : str
        printing size of the template. one of:
            - "a4"
            - "us-letter"
    out_path : str
        path of the output file
    """

    pdf_path = os.path.join(
        os.path.dirname(__file__), f"assets/template-{print_size}.pdf"
    )

    pdf = fitz.open(pdf_path)

    for index, stripe in enumerate(stripes):
        stripe.transform_colorspace("cmyk")
        stripe_half_width = PDF_STRIPE_HEIGHT / stripe.height * stripe.width / 2
        stripe_blob = stripe.make_blob("png")
        page = pdf[math.floor(index / 2)]

        # On each page, two stripes are displayed.
        # Both share the same `y` coordinates but have different `x` coordinates.
        # The stripes are x-positioned by their center point.
        positions = {
            PRINT_SIZES["A4"]: {
                "x": (158.9, 436.2),
                "y": 65.5,
            },
            PRINT_SIZES["US_LETTER"]: {
                "x": (167.2, 444.6),
                "y": 40.5,
            },
        }

        rect = fitz.Rect(
            positions[print_size]["x"][index % 2] - stripe_half_width,
            positions[print_size]["y"],
            positions[print_size]["x"][index % 2] + stripe_half_width,
            positions[print_size]["y"] + PDF_STRIPE_HEIGHT,
        )

        if not page.is_wrapped:
            page.wrap_contents()

        page.insert_image(rect, stream=stripe_blob, keep_proportion=False)

    pdf.save(out_path)
