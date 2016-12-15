#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Imports
from collections import OrderedDict
import hashlib
import io
import json
import os
import sys

import click
import pkg_resources
import requests
import validators

import crcmod.predefined as crcmod
import itertools as itt


##
# Plugins
##
PLUGIN_GROUP_NAME = 'omnihash.plugins'

known_digesters = OrderedDict()
""" Plugins add here 2-tuples (digester-factory-func, final-hashing-func). """


def intialize_plugins(plugin_group_name=PLUGIN_GROUP_NAME):
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
def plugin_sha3_digesters():
    import sha3  # @UnresolvedImport

    known_digesters['SHA3_224'] = (sha3.SHA3224(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_256'] = (sha3.SHA3256(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_384'] = (sha3.SHA3384(), lambda d: d.hexdigest().decode("utf-8"))
    known_digesters['SHA3_512'] = (sha3.SHA3512(), lambda d: d.hexdigest().decode("utf-8"))


def plugin_pyblake2_digesters():
    import pyblake2  # @UnresolvedImport

    known_digesters['BLAKE2s'] = (pyblake2.blake2s(), lambda d: d.hexdigest())
    known_digesters['BLAKE2b'] = (pyblake2.blake2b(), lambda d: d.hexdigest())


class GitSlurpDigester:
    """
    Produce Git-like hashes for bytes without knowing their size a priori.

    Git SHA1-hashes the file-bytes prefixed with the filesize.
    So when reading STDIN, we have to slurp the bytes to derive their length,
    and hash them afterwards.

    But it's not that we slurp multiple files, just the STDIN once.
    """

    fbytes = b''

    def __init__(self, otype):
        self.otype = otype

    def update(self, fbytes):
        self.fbytes += fbytes

    def digest(self):
        fsize = len(self.fbytes)
        digester = hashlib.sha1(("%s %i\0" % (self.otype, fsize)).encode())
        digester.update(self.fbytes)
        return digester.hexdigest()


def add_git_digesters(digesters, fpath):
    """Note that contrary to ``git hash-object`` no unix2dos EOL is done!"""
    try:
        fsize = os.stat(fpath).st_size
        digesters['GIT-BLOB'] = (hashlib.sha1(b"blob %i\0" % fsize), lambda d: d.hexdigest())
        digesters['GIT-COMMIT'] = (hashlib.sha1(b"commit %i\0" % fsize), lambda d: d.hexdigest())
        digesters['GIT-TAG'] = (hashlib.sha1(b"tag %i\0" % fsize), lambda d: d.hexdigest())
    except:
        ## Failback to slurp-digesters `fpath` is not a file.
        #
        digesters['GIT-BLOB'] = (GitSlurpDigester('blob'), lambda d: d.digest())
        digesters['GIT-COMMIT'] = (GitSlurpDigester('commit'), lambda d: d.digest())
        digesters['GIT-TAG'] = (GitSlurpDigester('tag'), lambda d: d.digest())


##
# Classes
##

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


class LenDigester:
    length = 0

    def update(self, b):
        self.length += len(b)

    def digest(self):
        return str(self.length)

##
# CLI
##

@click.command()
@click.argument('hashmes', nargs=-1)
@click.option('-s', is_flag=True, default=False, help="Hash input as string, even if there is a file with that name.")
@click.option('-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('-c', is_flag=True, default=False, help="Calculate CRCs as well.")
@click.option('-f', is_flag=False, default=False, multiple=True,
              help="Select one or more family of algorithms: "
              "include only algos having TEXT (ci) in their names.")
@click.option('-m', is_flag=False, default=False, help="Match input string.")
@click.option('-j', is_flag=True, default=False, help="Output result in JSON format.")
@click.pass_context
def main(click_context, hashmes, s, v, c, f, m, j):
    """
    If there is a file at hashme, read and omnihash that file.
    Elif hashme is a string, omnihash that.
    """

    # Print version and quit
    if v:
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    intialize_plugins()

    results = None
    if not hashmes:
        # If no stdin, just help and quit.
        if not sys.stdin.isatty():
            digesters = make_digesters(None, f, c)
            stdin = click.get_binary_stream('stdin')
            bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')
            if not j:
                click.echo("Hashing " + click.style("standard input", bold=True) + "..", err=True)
            results = produce_hashes(bytechunks, digesters, match=m)
        else:
            print(click_context.get_help())
            return
    else:
        hash_many = len(hashmes) > 1
        for hashme in hashmes:
            digesters = make_digesters(hashme, f, c)
            bytechunks = iterate_bytechunks(hashme, s, j, hash_many)
            if bytechunks:
                results = produce_hashes(bytechunks, digesters, match=m, use_json=j)

    if results and j:
        print(json.dumps(results, indent=4, sort_keys=True))


##
# Main Logic
##

def iterate_bytechunks(hashme, is_string, use_json, hash_many):
    """
    Prep our bytes.
    """

    # URL
    if not is_string and validators.url(hashme):
        if not use_json:
            click.echo("Hashing content of URL " + click.style(hashme, bold=True) + "..", err=not hash_many)
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
            if not use_json:
                click.echo(click.style("Skipping", fg="yellow") + " directory " + "'" + hashme + "'..", err=True)
            return None

        if not use_json:
            click.echo("Hashing file " + click.style(hashme, bold=True) + "..", err=not hash_many)
        bytechunks = FileIter(open(hashme, mode='rb'))
    # String
    else:
        if not use_json:
            click.echo("Hashing string " + click.style(hashme, bold=True) + "..", err=not hash_many)
        bytechunks = (hashme.encode('utf-8'), )

    return bytechunks


def make_digesters(fpath, families, include_CRCs=False):
    """
    Create and return a dictionary of all our active hash algorithms.

    Each digester is a 2-tuple ``( digester.update_func(bytes), digest_func(digester) -> int)``.
    """
    ## TODO: simplify digester-tuple API, ie: (digester, update_func(d), digest_func(d))

    families = set(f.upper() for f in families)
    digesters = OrderedDict()

    digesters['LENGTH'] = (LenDigester(), LenDigester.digest)

    # Default Algos
    for algo in sorted(hashlib.algorithms_available):
        # algorithms_available can have duplicates
        aname = algo.upper()
        if aname not in digesters and is_algo_in_families(aname, families):
            digesters[aname] = (hashlib.new(algo), lambda d: d.hexdigest())

    # CRC
    if include_CRCs:
        for name in sorted(crcmod._crc_definitions_by_name):
            crc_name = crcmod._crc_definitions_by_name[name]['name']
            aname = crc_name.upper()
            if is_algo_in_families(aname, families):
                digesters[aname] = (crcmod.PredefinedCrc(crc_name),
                                    lambda d: hex(d.crcValue))

    add_git_digesters(digesters, fpath)

    ## Append plugin digesters.
    #
    digesters.update(known_digesters)
    for digester in list(digesters.keys()):
        if not is_algo_in_families(digester.upper(), families):
            digesters.pop(digester, None)

    return digesters


def produce_hashes(bytechunks, digesters, match, use_json=False):
    """
    Given our bytes and our algorithms, calculate and print our hashes.
    """

    # Produce hashes
    streams = itt.tee(bytechunks, len(digesters))
    batch = zip(streams, digesters.items())
    results = {}

    match_found = False
    for stream, (algo, (digester, hashfunc)) in batch:
        for b in stream:
            digester.update(b)

        result = hashfunc(digester)
        if match:
            if match in result:
                echo(algo, result, use_json)
                results[algo] = result
                match_found = True
        else:
            results[algo] = result
            echo(algo, result, use_json)

    if match:
        if not match_found:
            if not use_json:
                click.echo(click.style("No matches", fg='red') + " found!", err=True)

    return results


##
# Util
##

def is_algo_in_families(algo_name, families):
    """:param algo_name: make sure it is UPPER"""
    return not families or any(f in algo_name for f in families)


def echo(algo, digest, json=False):
    if not json:
        click.echo('  %-*s%s' % (32, click.style(algo, fg='green') + ':', digest))

##
# Entrypoint
##

if __name__ == '__main__':
    try:
        main()
    except ValueError as ex:
        echo(ex, err=True)
