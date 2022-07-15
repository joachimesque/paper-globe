# PaperGlobe 🪄🗺

PaperGlobe is a Python utility that will transform an image of the Earth to a template that you can cut and assemble by yourself.

Of course you’re not limited to the Earth, you can use any other planet or quasi-spherical object as a source, as long as its surface is projected in the correct way. The image of the planet must be a cylindrical projection. Right now it works with [Equirectangular](https://en.wikipedia.org/wiki/Equirectangular_projection), [Mercator](https://en.wikipedia.org/wiki/Mercator_projection) or [Gall stereographic](https://en.wikipedia.org/wiki/Gall_stereographic_projection) projections. PaperGlobe could work with any other projection, but the results won’t make you happy.

![](https://repository-images.githubusercontent.com/513955992/0b1beb9c-7e3d-4535-8feb-ba6dadaff4f8)

## Using PaperGlobe

### Installation

PaperGlobe is neatly served as a Python module.

First off, you have to have **Python 3** installed on your machine. Then, these three commands will setup the script:

```shell
python3 -m venv venv
source venv/bin/activate
pip install https://github.com/joachimesque/paper-globe/archive/refs/tags/v0.0.2.zip
```

The script can then be run with:

```shell
paperglobe earth.jpg
```

If the command `paperglobe` is not recognized by your shell, you might have to run the Virtual Environment activation command:

```shell
source venv/bin/activate
```

### Options

#### `--projection`, `-p`

This option lets you choose between three map projections:

- `--projection equirectangular` (by default)
- `--projection mercator`
- `--projection gall-stereo`

#### `--size`, `-s`

This option lets you choose between two paper sizes for printing the template:

- `--size a4` (by default)
- `--size us-letter` (which uses wizard measurements)

## Contributing

### Code

After cloning the repo on your machine, you have to set it up:

```shell
python3 -m virtualenv venv
source venv/bin/activate
pip install --editable .
```

Before submiting a PR, be sure to lint your code with [black](https://github.com/psf/black).

### Template files

The template files are provided in the `.afdesign` format, which is authored by [Affinity Designer](https://affinity.serif.com/en-gb/designer/). Please do not hesitate to suggest a better, free alternative.

## The templates

I ([@joachimesque](github.com/joachimesque)) created the templates in 2012, inspired by the “Sectional Globe - earth's axis, 23.4 degrees” by [GeoGrafia](www.geo-grafia.jp). The templates have been hosted on [joachimesque.com/globe](joachimesque.com/globe) since that time. I originally released the templates under a [Creative Commons By-NC-SA 2.0 fr](https://creativecommons.org/licenses/by-nc-sa/2.0/fr/), but I now updated the licence of the templates to a [Creative Commons By-NC 4 International](https://creativecommons.org/licenses/by-nc/4.0/) license: the templates generated by this software do not need to be shared under a "Share Alike" license anymore, to avoid potential problems if the image used is copyrighted.

The template source files (`*.afdesign`) are shared under a [CC By-NC-SA license](https://creativecommons.org/licenses/by-nc/4.0/).

**Important**: a template generated through this tool can not be used for commercial purposes. If you want to use this tool, or templates generated through this tool for educative/academic purposes, you are most welcome to do it. The template is absolutely free to use, and should always stay free.

As mentioned on the templates, GeoGrafia’s globes are cheap and neat, you should really consider buying one if available.

## License

This software is released under the [GNU AGPL v3 license](https://github.com/joachimesque/paper-globe/blob/main/LICENSE), unless otherwise mentioned.

The image `earth.jpg` is in the public domain in the United States because it was solely created by NASA. [Please see the source for more information](https://en.wikipedia.org/wiki/File:Equirectangular-projection.jpg).
