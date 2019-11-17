"""traitsui GUI elements for HyperSpy.

"""
# setup.py adapted from https://github.com/pypa/sampleproject/blob/master/setup.py
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, OSError):
    # pypandoc.convert raise OSError if pandoc is not in the path
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


version = {}
with open(path.join(here, "hyperspy_gui_traitsui", "version.py")) as fp:
    exec(fp.read(), version)


setup(
    name='hyperspy_gui_traitsui',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version['__version__'],

    description=('traitsui GUI elements for HyperSpy.'),
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/hyperspy/hyperspy_gui_traitsui',

    # Author details
    author='The HyperSpy Developers',
    author_email='devel@hyperspy.org',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],

    # What does your project relate to?
    keywords='hyperspy traitsui',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['hyperspy>=1.5', 'traitsui>=6.0'],
    entry_points={'hyperspy.extensions': 'hyperspy-gui-traitsui = hyperspy_gui_traitsui'},
    package_data={  # Optional
        'hyperspy_gui_traitsui': ['hyperspy_extension.yaml'], },
        )
