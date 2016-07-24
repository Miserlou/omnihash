import os
import setuptools
import omnihash 
import sys

from setuptools import setup

# To support 2/3 installation
setup_version = int(setuptools.__version__.split('.')[0])
if setup_version < 18:
    print("Please upgrade your setuptools to install omnihash: ")
    print("pip install -U pip wheel setuptools")
    quit()

# Set external files
try:
    from pypandoc import convert
    README = convert('README.md', 'rst')	 
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='omnihash',
    version=omnihash.__version__,
    packages=['omnihash'],
    install_requires=required,
    include_package_data=True,
    license='MIT License',
    description='Hash files and strings in various common algorithms',
    long_description=README,
    url='https://github.com/Miserlou/omnihash',
    author='Rich Jones',
    author_email='rich@openwatch.net',
    entry_points={
        'console_scripts': [
            'omnihash = omnihash.omnihash:main',
        ]
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
)
