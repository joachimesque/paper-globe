from setuptools import setup, find_packages

setup(
    name="paperglobe",
    version="0.0.1",
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
