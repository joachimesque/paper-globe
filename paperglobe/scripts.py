import click
from paperglobe import (
    generate_paperglobe,
    PROJECTIONS,
    PRINT_SIZES,
    format_output_filename,
)


@click.command()
@click.argument("file", type=click.Path(exists=True), metavar="<file>")
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
def cli(file, projection, print_size):
    """Generate a Paper Globe template from a cylindrical projection map. 🗺

    \b
    <projection> can be:
      • equirectangular
      • mercator
      • gall-stereo (for a Gall Stereographic projection)
    """

    click.echo(
        f"{click.style(file, bold=True)} has been found, starting conversion. 🧑‍🚀🪄 🗺"
    )

    generation_status = generate_paperglobe(file, projection, print_size)

    if generation_status:
        filename = click.style(format_output_filename(file, print_size), bold=True)
        click.echo(f"The file {filename} has been saved. 🧑‍🚀 ✨🌏🌍🌎✨")
    else:
        click.echo("An error has occured.")
