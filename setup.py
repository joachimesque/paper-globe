from setuptools import setup, find_packages

setup(
    name="paperglobe",
    description="Turns a map into a paper globe template",
    long_description="A Python utility that will transform an image of the Earth to a template that you can cut and assemble by yourself",
    url="https://github.com/joachimesque/paper-globe",
    version="0.1.1",
    author="Joachim Robert",
    author_email="joachim.robert@protonmail.com",
    license="GNU AGPL 3",
    py_modules=["paperglobe"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "colorama",
        "PyMuPDF",
        "wand",
    ],
    entry_points={
        "console_scripts": [
            "paperglobe = paperglobe.scripts:cli",
        ],
    },
)
