# PaperGlobe 🪄🗺

PaperGlobe is a Python utility that will transform an image of the Earth to a template that you can cut and assemble by yourself.

Of course you’re not limited to the Earth, you can use any other planet or quasi-spherical object as a source, as long as its surface is projected in the correct way. The image of the planet must be a cylindrical projection. Right now it works with [Equirectangular](https://en.wikipedia.org/wiki/Equirectangular_projection), [Mercator](https://en.wikipedia.org/wiki/Mercator_projection) or [Gall stereographic](https://en.wikipedia.org/wiki/Gall_stereographic_projection) projections. PaperGlobe will work with another projection, but the results won’t make you happy.

## Installing PaperGlobe

PaperGlobe is neatly served as a Python module.

First off, you have to have *Python 3* installed on your machine.

Then you have to download or clone the contents of this repository.

Then, these three commands will setup the script:

```shell
python3 -m virtualenv venv
source venv/bin/activate
pip install .
```

The script can then be run with:

```shell
paperglobe earth.jpg
```

If the command `paperglobe` is not recognized by your shell, you might have to run the Virtual Environment activation command:

```shell
source venv/bin/activate
```

## Options

### `--projection`, `-p`

This option lets you choose between three map projections:

- `--projection equirectangular` (by default)
- `--projection mercator`
- `--projection gall-stereo`

### `--size`, `-s`

This option lets you choose between two paper sizes for printing the template:

- `--size a4` (by default)
- `--size us-letter` (which uses wizard measures)

## Developing

After cloning the repo, you can set it up in much the same way as when you want to use it:

```shell
python3 -m virtualenv venv
source venv/bin/activate
pip install --editable .
```

Before submiting a PR, be sure to lint your code with `black`.

## License

This software is released under the GNU AGPL v3.

The image `earth.jpg` is in the public domain in the United States because it was solely created by NASA. [Please see the source for more information](https://en.wikipedia.org/wiki/File:Equirectangular-projection.jpg).
