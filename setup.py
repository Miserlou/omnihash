import io
import os

from setuptools import setup
import setuptools


# To support 2/3 installation
setup_version = int(setuptools.__version__.split('.')[0])
if setup_version < 18:
    print("Please upgrade your setuptools to install omnihash: ")
    print("pip install -U pip wheel setuptools")
    quit()

mydir = os.path.dirname(__file__)

# Set external files
try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


## Version-trick to have version-info in a single place, taken from:
# http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
#
def read_project_version():
    fglobals = {}
    with io.open(os.path.join(
            mydir, 'omnihash', '__init__.py'), encoding='UTF-8') as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = [l for l in f.read().splitlines()  # Exclude extras.
                if not any(r in l for r in ('pyblake2', 'sha3'))]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='omnihash',
    version=read_project_version(),
    packages=['omnihash'],
    install_requires=required,
    include_package_data=True,
    license='MIT License',
    description='Hash files, strings, input streams and network resources in various common algorithms simultaneously',
    long_description=README,
    url='https://github.com/Miserlou/omnihash',
    author='Rich Jones',
    author_email='rich@openwatch.net',
    entry_points={
        'console_scripts': [
            'omnihash = omnihash.omnihash:main',
            'oh = omnihash.omnihash:main',
        ],
        'omnihash.plugins': [
            'a_sha3 = omnihash.omnihash:plugin_sha3_digesters [sha3]',
            'b_pyblake2 = omnihash.omnihash:plugin_pyblake2_digesters [pyblake2]',
        ],
    },
    extras_require={
        'sha3': ['sha3'],
        'pyblake2': ['pyblake2'],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    tests_require=['nose'],
    zip_safe=True,
    options={
        'bdist_wheel': {
            'universal': True,
        },
    },
    platforms=['any'],
)
