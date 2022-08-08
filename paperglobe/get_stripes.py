"""Generates a list of stripes from an image"""

import math

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

from paperglobe.config import PROJECTIONS

COLS_NUMBER = 8
ROWS_NUMBER = 4

PROJECTIONS_RATIOS = {
    PROJECTIONS["EQUIRECTANGULAR"]: [
        0.25,
        0.25,
        0.25,
        0.25,
    ],
    PROJECTIONS["MERCATOR"]: [
        0.36,
        0.14,
        0.14,
        0.36,
    ],
    PROJECTIONS["GALL_STEREOGRAPHIC"]: [
        0.295,
        0.205,
        0.205,
        0.295,
    ],
}

ROW_HEIGHT_RATIOS = [0.935, 0.988, 0.988, 0.935]

SHEAR_ANGLES = [
    19.51,
    8.28,
    -8.28,
    -19.51,
]

WING_VERTICAL_DISPLACEMENT = [
    (0.30, 1),  # (top, bottom)
    (0.28, 0.65),
    (0.65, 0.28),
    (1, 0.30),
]

# pylint: disable=too-many-locals,too-many-statements
def get_stripes(file, projection):
    """Generates a stripes array from an image and a projection type

    Parameters
    ----------
    file : str
        path of the image file to be used to generate the template
    projection : str
        type of projection. one of:
            - "equirectangular"
            - "mercator"
            - "gall-stereo"

    Returns
    -------
    list
        a list of vertical Image objects

    TODO
    ----
    - refactor to get rid of the pylint warning
    """

    if file.endswith(".svg"):
        original_image = Image(filename=file, resolution=450)
        if original_image.width > 2048:
            original_image.resize(2048)
    else:
        original_image = Image(filename=file)

    tile_width = math.floor(original_image.width / COLS_NUMBER)
    tile_height = math.floor(original_image.height / ROWS_NUMBER)
    tile_ratio = tile_width / tile_height
    wing_width = math.floor(tile_width * 0.08)

    stripe_width = tile_width + (2 * wing_width)

    row_heights = [math.floor(tile_width * i) for i in ROW_HEIGHT_RATIOS]

    halfway_padding = math.floor(tile_width * 0.146)
    projection_heights = [
        i * original_image.height for i in PROJECTIONS_RATIOS[projection]
    ]

    stripes = [
        Image(
            width=stripe_width, height=sum(row_heights), background=Color("transparent")
        )
        for i in range(COLS_NUMBER)
    ]

    for col in range(COLS_NUMBER):
        pos_x_start = tile_width * col
        pos_x_end = tile_width * (col + 1)

        for row in range(ROWS_NUMBER):
            pos_y_start = math.floor(sum(projection_heights[:row]))
            pos_y_end = math.floor(sum(projection_heights[: row + 1]))

            chunk = original_image[pos_x_start:pos_x_end, pos_y_start:pos_y_end]
            chunk.virtual_pixel = "transparent"
            chunk.interpolate = "spline"

            chunk.resize(tile_width, row_heights[row])

            shear_angle = SHEAR_ANGLES[row] * tile_width / tile_height

            # WEST WING
            x_start = original_image.width if col == 0 else pos_x_start
            w_wing_x_start = x_start - wing_width
            w_wing_x_end = x_start
            w_wing_chunk = original_image[
                w_wing_x_start:w_wing_x_end, pos_y_start:pos_y_end
            ]
            w_wing_chunk.virtual_pixel = "transparent"
            w_wing_chunk.distort(
                "bilinear_forward",
                (
                    0,
                    0,
                    0,
                    WING_VERTICAL_DISPLACEMENT[row][0] * wing_width / tile_ratio,
                    w_wing_chunk.width,
                    0,
                    w_wing_chunk.width,
                    0,
                    w_wing_chunk.width,
                    w_wing_chunk.height,
                    w_wing_chunk.width,
                    w_wing_chunk.height,
                    0,
                    w_wing_chunk.height,
                    0,
                    w_wing_chunk.height
                    - WING_VERTICAL_DISPLACEMENT[row][1] * wing_width / tile_ratio,
                ),
                best_fit=True,
            )
            w_wing_chunk.shear(Color("transparent"), x=shear_angle, y=0)

            with Drawing() as draw:
                draw.composite(
                    operator="over",
                    left=(0 if row in (1, 2) else halfway_padding) + 1,
                    top=sum(row_heights[:row]),
                    width=w_wing_chunk.width,
                    height=chunk.height,
                    image=w_wing_chunk,
                )
                draw(stripes[col])

            # EAST WING
            x_end = 0 if col == COLS_NUMBER - 1 else pos_x_end
            e_wing_x_start = x_end
            e_wing_x_end = x_end + wing_width
            e_wing_chunk = original_image[
                e_wing_x_start:e_wing_x_end, pos_y_start:pos_y_end
            ]
            e_wing_chunk.virtual_pixel = "transparent"
            e_wing_chunk.distort(
                "bilinear_forward",
                (
                    0,
                    0,
                    0,
                    0,
                    e_wing_chunk.width,
                    0,
                    e_wing_chunk.width,
                    WING_VERTICAL_DISPLACEMENT[row][0] * wing_width / tile_ratio,
                    e_wing_chunk.width,
                    e_wing_chunk.height,
                    e_wing_chunk.width,
                    e_wing_chunk.height
                    - WING_VERTICAL_DISPLACEMENT[row][1] * wing_width / tile_ratio,
                    0,
                    e_wing_chunk.height,
                    0,
                    e_wing_chunk.height,
                ),
                best_fit=True,
            )
            e_wing_chunk.shear(Color("transparent"), x=shear_angle * -1, y=0)

            with Drawing() as draw:
                draw.composite(
                    operator="over",
                    left=(
                        stripe_width - e_wing_chunk.width
                        if row in (1, 2)
                        else stripe_width - e_wing_chunk.width - halfway_padding
                    )
                    - 1,
                    top=sum(row_heights[:row]),
                    width=e_wing_chunk.width,
                    height=chunk.height,
                    image=e_wing_chunk,
                )
                draw(stripes[col])

            # MAIN SQUARE
            if row == 0:
                chunk.distort(
                    "bilinear_forward",
                    (
                        0,
                        0,
                        tile_width / 2,
                        0,
                        tile_width,
                        0,
                        tile_width / 2 + 1,
                        0,
                        tile_width,
                        row_heights[row],
                        tile_width - halfway_padding,
                        row_heights[row],
                        0,
                        row_heights[row],
                        halfway_padding,
                        row_heights[row],
                    ),
                    best_fit=True,
                )
            elif row == 1:
                chunk.distort(
                    "bilinear_forward",
                    (
                        0,
                        0,
                        halfway_padding,
                        0,
                        tile_width,
                        0,
                        tile_width - halfway_padding,
                        0,
                        tile_width,
                        row_heights[row],
                        tile_width,
                        row_heights[row],
                        0,
                        row_heights[row],
                        0,
                        row_heights[row],
                    ),
                    best_fit=True,
                )

            elif row == 2:
                chunk.distort(
                    "bilinear_forward",
                    (
                        0,
                        0,
                        0,
                        0,
                        tile_width,
                        0,
                        tile_width,
                        0,
                        tile_width,
                        row_heights[row],
                        tile_width - halfway_padding,
                        row_heights[row],
                        0,
                        row_heights[row],
                        halfway_padding,
                        row_heights[row],
                    ),
                    best_fit=True,
                )
            elif row == 3:
                chunk.distort(
                    "bilinear_forward",
                    (
                        0,
                        0,
                        halfway_padding,
                        0,
                        tile_width,
                        0,
                        tile_width - halfway_padding,
                        0,
                        tile_width,
                        row_heights[row],
                        tile_width / 2 + 1,
                        row_heights[row],
                        0,
                        row_heights[row],
                        tile_width / 2,
                        row_heights[row],
                    ),
                    best_fit=True,
                )

            with Drawing() as draw:
                draw.composite(
                    operator="over",
                    left=wing_width,
                    top=sum(row_heights[:row]),
                    width=chunk.width,
                    height=chunk.height,
                    image=chunk,
                )
                draw(stripes[col])

    return stripes
