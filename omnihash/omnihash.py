#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Imports
from collections import OrderedDict
import hashlib
import io
import itertools as itt
import os
import pkg_resources
import sys

# 3rd Party imports
import click
import requests
import validators

# Algos
import crcmod.predefined as crcmod


PLUGIN_GROUP_NAME = 'omnihash.plugins'

known_digesters = OrderedDict()
""" Plugins add here 2-tuples (digester-factory-func, final-hashing-func). """


def _init_plugins(plugin_group_name=PLUGIN_GROUP_NAME):
    entry_points = pkg_resources.working_set.iter_entry_points(plugin_group_name)
    for ep in sorted(entry_points, key=lambda ep: ep.name):
        try:
            plugin_loader = ep.load()
            if callable(plugin_loader):
                plugin_loader()
        except Exception as ex:
            click.echo('Failed LOADING plugin(%r@%s) due to: %s' % (
                      ep, ep.dist, ex), err=1)

# Plugin algos
def plugin_sha3_digesters(include_CRCs=False):
    import sha3  # @UnresolvedImport

    known_digesters['SHA3_224'] = (sha3.SHA3224(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_256'] = (sha3.SHA3256(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_384'] = (sha3.SHA3384(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_512'] = (sha3.SHA3512(), lambda d: d.hexdigest().decode("utf-8"))

def plugin_pyblake2_digesters(include_CRCs=False):
    import pyblake2  # @UnresolvedImport

    known_digesters['BLAKE2s'] = (pyblake2.blake2s(), lambda d: d.hexdigest())
    known_digesters['BLAKE2b'] = (pyblake2.blake2b(), lambda d: d.hexdigest())


class FileIter(object):
    """An iterator that chunks in bytes a file-descriptor, auto-closing it when exhausted."""
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
@click.option('-c', is_flag=True, default=False, help="Calculate CRCs as well.")
@click.version_option(version=pkg_resources.require("omnihash")[0].version)
@click.pass_context
def main(click_context, hashmes, s, v, c):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """
    _init_plugins()

    if not hashmes:
        # If no stdin, just help and quit.
        if not sys.stdin.isatty():
            digesters = make_digesters(c)
            stdin = click.get_binary_stream('stdin')
            bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')
            click.echo("Hashing standard input..")
            produce_hashes(bytechunks, digesters)
        else:
            print(click_context.get_help())
            return
    else:
        for hashme in hashmes:
            digesters = make_digesters(c)
            bytechunks = iterate_bytechunks(hashme, s)
            if bytechunks:
                produce_hashes(bytechunks, digesters)


def iterate_bytechunks(hashme, is_string=True):
    """
    Prep our bytes.
    """

    # URL
    if not is_string and validators.url(hashme):
        click.echo("Hashing content of URL " + click.style("{}".format(hashme), bold=True) + "..")
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
        if os.path.isdir(hashme):
            click.echo(click.style("Skipping", fg="yellow") + " directory " + "'" + hashme + "'..")
            return None

        click.echo("Hashing file " + click.style("{}".format(hashme), bold=True) + "..")
        bytechunks = FileIter(open(hashme, mode='rb'))
    # String
    else:
        click.echo("Hashing string " + click.style("{}".format(hashme), bold=True) + "..")
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

    ## Append plugin digesters.
    digesters.update(known_digesters)

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
