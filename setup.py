"""
To create the wheel run - python setup.py bdist_wheel
"""

from setuptools import setup
import os, sys

PACKAGE_NAME = 'futura'
VERSION = '0.0.4'

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('futura'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)

for dirpath, dirnames, filenames in os.walk('futura_ui'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


my_package_files = []
my_package_files.extend(package_files(os.path.join('futura', 'assets')))

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=packages,
    author="P. James Joyce",
    author_email="pjamesjoyce@gmail.com",
    license="BSD 3-Clause License",
    package_data={'futura': my_package_files},
    entry_points={
        'console_scripts': [
            'futura = futura_ui.bin.run_futura:main'
        ],
        'gui_scripts': [
            'futura_ui = futura_ui.bin.run_futura_ui:main'
        ]
    },
    # install_requires=[
    # ],
    include_package_data=True,
    url="https://github.com/pjamesjoyce/{}/".format(PACKAGE_NAME),
    download_url="https://github.com/pjamesjoyce/{}/archive/{}.tar.gz".format(PACKAGE_NAME, VERSION),
    long_description=open('README.md').read(),
    description='A tool for LCA',
    keywords=['LCA', 'Life Cycle Assessment', 'Foreground system', 'Background system', 'Foreground model',
              'Fully parameterised'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

# Also consider:
# http://code.activestate.com/recipes/577025-loggingwebmonitor-a-central-logging-server-and-mon/
