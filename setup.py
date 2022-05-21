from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'

DESCRIPTION = 'Python wrapper for the COD API (Warzone) as well as wzstats.gg, with some useful functions to process and parse the stat responses.'

# Setting up
setup(
    name="WarzoneStats",
    version=VERSION,
    author="valtov",
    author_email="<vladialtv@gmail.com>",
    url = 'https://github.com/valtov/WarzoneStats',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'warzone', 'tracker', 'tracker.gg', 'sbmm', 'kd'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
