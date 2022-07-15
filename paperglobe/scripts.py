import click
from paperglobe import (
    PaperGlobe,
    PROJECTIONS,
    PRINT_SIZES,
    STATUS_TYPES,
)


@click.command()
@click.argument("file", type=click.Path(exists=True, file_okay=True), metavar="<file>")
@click.argument("out_path", type=click.Path(), default="", metavar="<output_path>")
@click.option(
    "-p",
    "--projection",
    default=PROJECTIONS["EQUIRECTANGULAR"],
    metavar="<projection>",
    help="The map projection on your input image.",
    type=click.Choice([PROJECTIONS[i] for i in PROJECTIONS]),
)
@click.option(
    "-s",
    "--print-size",
    default=PRINT_SIZES["A4"],
    help=f"PDF print size.",
    type=click.Choice([PRINT_SIZES[i] for i in PRINT_SIZES]),
)
@click.version_option()
def cli(file, projection, print_size, out_path):
    """Generate a Paper Globe template from a cylindrical projection map. 🗺

    \b
    <projection> can be:
      - equirectangular
      - mercator
      - gall-stereo (for a Gall Stereographic projection)
    """

    def echo_status(status_type, message):
        if status_type == STATUS_TYPES["ERROR"]:
            click.echo(f"{click.style('Error', bold=True, fg='red')}: ", nl=False)
        click.echo(message)

    def bold(text):
        return click.style(text, bold=True)

    pg = PaperGlobe(on_update=echo_status, bold=bold)
    pg.generate_paperglobe(file, projection, print_size, out_path)
