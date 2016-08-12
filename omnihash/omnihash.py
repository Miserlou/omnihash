#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Imports
from collections import OrderedDict
import functools as fnt
import hashlib
import io
import itertools as itt
import os
import sys

# 3rd Party 
import click
import requests
import validators

# Algos
import crcmod.predefined as crcmod
from pyblake2 import blake2b, blake2s
import sha3


class FileIter(object):
    """An iterator for file-descriptor that auto-closes when exhausted."""
    def __init__(self, fd):
        self._fd = fd
        self._iter = iter(lambda: fd.read(io.DEFAULT_BUFFER_SIZE), b'')

    def __iter__(self):
        return self._iter

    def next(self):
        try:
            return self._iter.next()
        except StopIteration:
            self._fd.close()
            raise


@click.command()
@click.argument('hashmes', nargs=-1)
@click.option('-s', is_flag=True, default=False, help="Hash input as string, even if there is a file with that name.")
@click.option('-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('-c', is_flag=True, default=False, help="Calculate CRCs as well.")
def main(hashmes, s, v, c):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """

    # Print version and quit
    if v:
        import pkg_resources
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    if not hashmes:
        digesters = make_digesters(c)
        if hasattr(sys.stdin, 'buffer'):
            bytechunks = iter(lambda: sys.stdin.buffer.read(io.DEFAULT_BUFFER_SIZE), b'')
        else:
            bytechunks = iter(lambda: sys.stdin.read(io.DEFAULT_BUFFER_SIZE), b'')

        if not sys.stdin.isatty():
            click.echo("Hashing standard input..")
            produce_hashes(bytechunks, digesters)
    else:
        for hashme in hashmes:
            digesters = make_digesters(c)
            bytechunks = iterate_bytechunks(hashme, s)
            produce_hashes(bytechunks, digesters)


def iterate_bytechunks(hashme, is_string=True):
    """
    Prep our bytes.
    """

    # URL
    if not is_string and validators.url(hashme):
        click.echo("Hashing content of URL '{}'..".format(hashme))
        try:
            response = requests.get(hashme)
        except requests.exceptions.ConnectionError as e:
            raise ValueError("Not a valid URL. :(")
        except Exception as e:
            raise ValueError("Not a valid URL. {}.".format(e))
        if response.status_code != 200:
            click.echo("Response returned %s. :(" % response.status_code, err=True)
        bytechunks = response.iter_content()
    # File
    elif os.path.exists(hashme) and not is_string:
        click.echo("Hashing file {}..".format(hashme))
        bytechunks = FileIter(open(hashme, mode='rb'))
    # String
    else:
        click.echo("Hashing string '{}'..".format(hashme))
        bytechunks = (hashme.encode('utf-8'), )

    return bytechunks


def make_digesters(include_CRCs=False):
    """
    Create and return a dictionary of all our active hash algorithms.
    """
    digesters = OrderedDict()

    # Default Algos
    for algo in sorted(hashlib.algorithms_available):

        # algorithms_available can have duplicates
        if algo.upper() not in digesters:
            digesters[algo.upper()] = (hashlib.new(algo), lambda d: d.hexdigest())

    # SHA3 Family
    digesters['SHA3_224'] = (sha3.SHA3224(), lambda d: d.hexdigest().decode("utf-8"))
    digesters['SHA3_256'] = (sha3.SHA3256(), lambda d: d.hexdigest().decode("utf-8"))
    digesters['SHA3_384'] = (sha3.SHA3384(), lambda d: d.hexdigest().decode("utf-8"))
    digesters['SHA3_512'] = (sha3.SHA3512(), lambda d: d.hexdigest().decode("utf-8"))

    # BLAKE
    digesters['BLAKE2s'] = (blake2s(), lambda d: d.hexdigest())
    digesters['BLAKE2b'] = (blake2b(), lambda d: d.hexdigest())

    # CRC
    if include_CRCs:
        for name in sorted(crcmod._crc_definitions_by_name):
            crc_name = crcmod._crc_definitions_by_name[name]['name']
            digesters[crc_name.upper()] = (crcmod.PredefinedCrc(crc_name),
                                           lambda d: hex(d.crcValue))

    return digesters

def produce_hashes(bytechunks, digesters):
    """
    Given our bytes and our algorithms, calculate and print our hashes.
    """

    # Produce hashes
    streams = itt.tee(bytechunks, len(digesters))
    batch = zip(streams, digesters.items())
    for stream, (algo, (digester, hashfunc)) in batch:
        for b in stream:
            digester.update(b)
        echo(algo, hashfunc(digester))

def echo(algo, digest):
    click.echo('  %-*s%s' % (32, click.style(algo, fg='green') + ':', digest))

if __name__ == '__main__':
    try:
        main()
    except ValueError as ex:
        echo(ex, err=True)
