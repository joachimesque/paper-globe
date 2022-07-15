import math

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing

from paperglobe import PROJECTIONS

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
    """

    original_image = Image(filename=file, resolution=450)

    tile_width = math.floor(original_image.width / COLS_NUMBER)
    tile_height = math.floor(original_image.height / ROWS_NUMBER)

    row_height_ratios = [0.935, 0.988, 0.988, 0.935]
    row_heights = [math.floor(tile_width * i) for i in row_height_ratios]

    halfway_padding = tile_width * 0.146
    projection_ratios = PROJECTIONS_RATIOS[projection]
    projection_heights = [i * original_image.height for i in projection_ratios]

    stripes = [
        Image(
            width=tile_width, height=sum(row_heights), background=Color("transparent")
        )
        for i in range(COLS_NUMBER)
    ]

    iterator = 0

    for iterator in range(COLS_NUMBER * ROWS_NUMBER):
        col = iterator % COLS_NUMBER
        row = math.floor(iterator / COLS_NUMBER)

        pos_x_start = tile_width * col
        pos_x_end = tile_width * (col + 1)
        pos_y_start = math.floor(sum(projection_heights[:row]))
        pos_y_end = math.floor(sum(projection_heights[: row + 1]))

        chunk = original_image[pos_x_start:pos_x_end, pos_y_start:pos_y_end]
        chunk.virtual_pixel = "transparent"
        chunk.interpolate = "spline"

        chunk.sample(tile_width, row_heights[row])

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
                operator="replace",
                left=0,
                top=sum(row_heights[:row]),
                width=chunk.width,
                height=chunk.height,
                image=chunk,
            )
            draw(stripes[col])

    return stripes
