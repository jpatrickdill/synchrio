from setuptools import setup

__author__ = "J Patrick Dill"
__version__ = "0.7"

with open("readme.rst", "r") as readme:
    long_description = readme.read()

setup(
    name="synchrio",
    description="Wrapper class to run async code synchronously",
    long_description=long_description,

    licence="GPLv3",

    version=__version__,
    packages=["synchrio"],

    author=__author__,
    author_email="jamespatrickdill@gmail.com",


)