#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import omnihash
import sys

import click
import pkg_resources


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


##
# CLI
##

@click.command()
@click.argument('file-or-url', nargs=-1)
@click.option('--version', '-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('--as-str', '-s', is_flag=True, default=False,
              help="Hash cmd-line args as strings.")
@click.option('--family', '-f', is_flag=False, default=False, multiple=True,
              help=("Select only algorithm-families having TEXT in their names."
                    "Use it multiple times to select more families."))
@click.option('--x-family', '-x', is_flag=False, default=False, multiple=True,
              help=("Exclude algorithm-families algorithms having TEXT in their names."
                    "Use it multiple times to exclude more families."))
@click.option('--match', '-m', is_flag=False, default=False, help="Match input string.")
@click.option('--json', '-j', is_flag=True, default=False, help="Output result in JSON format.")
@click.pass_context
def main(click_context, file_or_url, version, as_str, family, x_family, match, json):
    """
    Read HASHME file/URL and omni-hash it. Read <stdin> if no args given.
    """
    # Print version and quit
    if version:
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    match = match and match.lower()
    digfacts = omnihash.collect_digester_factories(family, x_family)

    results = []
    if not file_or_url:
        stdin = click.get_binary_stream('stdin')
        bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')
        results.append([omnihash.produce_hashes(None, bytechunks, digfacts, match=match, use_json=json)])
    else:
        hash_many = len(file_or_url) > 1
        for arg in file_or_url:
            result = {}
            data = omnihash.iterate_bytechunks(arg, is_string=as_str, use_json=json, hash_many=hash_many)
            if data:
                length, bytechunks = data
                result = omnihash.produce_hashes(length, bytechunks, digfacts, match=match, use_json=json)
            if result:
                result['NAME'] = arg
                results.append(result)

    if results and json:
        import json

        print(json.dumps(results, indent=4, sort_keys=True))


@click.command()
@click.argument('hashme', nargs=-1)
@click.option('--version', '-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('--as-str', '-s', is_flag=True, default=None,
              help="Hash cmd-line args as strings, even if there are files named like that.")
@click.option('--family', '-f', is_flag=False, default=False, multiple=True,
              help=("Select only algorithm-families having TEXT in their names."
                    "Use it multiple times to select more families."))
@click.option('--x-family', '-x', is_flag=False, default=False, multiple=True,
              help=("Exclude algorithm-families having TEXT in their names."
                    "Use it multiple times to exclude more families."))
@click.option('--match', '-m', is_flag=False, default=False, help="Match input string.")
@click.option('--json', '-j', is_flag=True, default=False, help="Output result in JSON format.")
@click.pass_context
def main_fallback_to_str(click_context, hashme, version, as_str, family, x_family, match, json):
    """
    If HASHME is an existent file or a URL, read and omni-hash it.
    Otherwise, omni-hash HASHME as a string.  Read <stdin> if no args given.
    """

    # Print version and quit
    if version:
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    match = match and match.lower()
    digfacts = omnihash.collect_digester_factories(family, x_family)

    results = []
    if not hashme:
        # If no stdin, just help and quit.
        if not sys.stdin.isatty():
            stdin = click.get_binary_stream('stdin')
            bytechunks = iter(lambda: stdin.read(io.DEFAULT_BUFFER_SIZE), b'')
            if not json:
                click.echo("Hashing " + click.style("standard input", bold=True) + "..", err=True)
            results.append([omnihash.produce_hashes(None, bytechunks, digfacts, match=match, use_json=json)])
        else:
            print(click_context.get_help())
            return
    else:
        hash_many = len(hashme) > 1
        for arg in hashme:
            result = {}
            data = omnihash.iterate_bytechunks(arg, as_str, json, hash_many)
            if data:
                length, bytechunks = data
                result = omnihash.produce_hashes(length, bytechunks, digfacts, match=match, use_json=json)
            if result:
                result['NAME'] = arg
                results.append(result)

    if results and json:
        import json

        print(json.dumps(results, indent=4, sort_keys=True))


##
# Entrypoint
##

if __name__ == '__main__':
    try:
        main()
    except ValueError as ex:
        click.echo(ex, err=True)
