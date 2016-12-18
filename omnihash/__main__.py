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
@click.argument('hashmes', nargs=-1)
@click.option('--version', '-v', is_flag=True, default=False, help="Show version and quit.")
@click.option('--as-str', '-s', is_flag=True, default=False,
              help="Hash cmd-line args as strings, even if there are files named like that.")
@click.option('--family', '-f', is_flag=False, default=False, multiple=True,
              help=("Select a family of algorithms: "
                    "include only algos having TEXT in their names."
                    "Use it multiple times to select more families."))
@click.option('--x-family', '-x', is_flag=False, default=False, multiple=True,
              help=("Exclude a family of algorithms: "
                    "skip algos having TEXT in their names."
                    "Use it multiple times to exclude more families."))
@click.option('--match', '-m', is_flag=False, default=False, help="Match input string.")
@click.option('--json', '-j', is_flag=True, default=False, help="Output result in JSON format.")
@click.pass_context
def main(click_context, hashmes, version, as_str, family, x_family, match, json):
    """
    If there is a file at `hashme`, read and omnihash that.
    Otherwise, assume `hashme` is a string.
    """

    # Print version and quit
    if version:
        version = pkg_resources.require("omnihash")[0].version
        click.echo(version)
        return

    match = match and match.lower()
    digfacts = omnihash.collect_digester_factories(family, x_family)

    results = []
    if not hashmes:
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
        hash_many = len(hashmes) > 1
        for hashme in hashmes:
            result = {}
            data = omnihash.iterate_bytechunks(hashme, as_str, json, hash_many)
            if data:
                length, bytechunks = data
                result = omnihash.produce_hashes(length, bytechunks, digfacts, match=match, use_json=json)
            if result:
                result['NAME'] = hashme
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
